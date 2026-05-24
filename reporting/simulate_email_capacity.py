"""Post-launch email provider capacity simulation — mirrors /email-machine scenario planner."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "public" / "email_sequences.json"
BASELINE_PATH = ROOT / "public" / "baseline_snapshot.json"

CADENCE = {
    "one-time": 1,
    "drip-2-4": 3,
    "one-time-plus-d7": 2,
    "campaign-2-touch": 2,
    "one-time-plus-d14": 2,
}

FAILURE_PRIORITY = {"launch_peak": 0, "daily": 1, "monthly": 2, "contacts": 3}


@dataclass
class SimContext:
    new_users_day: int
    new_users_month: int
    mode: str
    signup_vol: int
    total_users: int
    paid_subs: int
    limit_hitters: int
    cancelled_paid: int
    bucket_counts: dict[str, int]
    launch_audience: int
    activation_pct: float
    pmf_pct: float
    dead_cap: int
    active_rules: list[str] = field(default_factory=list)
    launch_days: int = 3
    agent_reserve: int = 50


def _compute_daily_peaks(ctx: SimContext) -> dict[str, float]:
    nps_daily_peak = round((ctx.new_users_month / 30) * 1.5)
    peaks: dict[str, float] = {}
    peaks["brevo"] = (
        ctx.new_users_day
        + round(ctx.new_users_day * (1 - ctx.activation_pct))
        + nps_daily_peak
        + (ctx.launch_audience / 2 / ctx.launch_days if ctx.mode == "launch_week" else 0)
        + ctx.agent_reserve
    )
    peaks["mailgun"] = max(
        round((ctx.new_users_month * ctx.pmf_pct) / 30),
        round(ctx.new_users_day * ctx.pmf_pct / 5),
    )
    peaks["hubspot"] = (
        0
        if "ph_week_brevo_primary" in ctx.active_rules
        else ctx.new_users_day + round(ctx.new_users_day * (1 - ctx.activation_pct))
    )
    return peaks


def _load_manifest(path: Path | None = None) -> dict[str, Any]:
    return json.loads((path or MANIFEST_PATH).read_text(encoding="utf-8"))


def _baseline(snapshot: dict[str, Any] | None) -> dict[str, Any]:
    snap = snapshot or json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    dau = snap.get("dau_model") or {}
    return {
        "total_users": int(snap.get("total_users") or 122),
        "bucket_counts": dict(
            dau.get("bucket_counts")
            or {
                "new": 0,
                "current": 0,
                "reactivated": 0,
                "resurrected": 1,
                "at_risk_wau": 16,
                "at_risk_mau": 10,
                "dead": 95,
            }
        ),
        "monetization": dict(
            snap.get("monetization")
            or {"paid_subscribers": 1, "users_hit_limit": 1, "cancelled_paid_subscribers": 0}
        ),
    }


def project_buckets(total_users: int, new_monthly: int) -> dict[str, int]:
    dau = max(1, round(total_users * 0.08))
    at_risk_wau = max(1, round(dau * 0.94))
    at_risk_mau = max(1, round(total_users * 0.08))
    dead = max(0, total_users - dau - at_risk_wau - at_risk_mau - 2)
    return {
        "new": min(max(1, new_monthly // 30), 5),
        "current": max(0, dau - 2),
        "reactivated": 1,
        "resurrected": 1,
        "at_risk_wau": at_risk_wau,
        "at_risk_mau": at_risk_mau,
        "dead": dead,
    }


def _seq_eligible(seq: dict[str, Any], ctx: SimContext) -> tuple[float, int]:
    cadence = CADENCE.get(seq.get("cadence") or "one-time", 1)
    eligible = 0
    for b in seq.get("buckets") or []:
        if b in ctx.bucket_counts:
            eligible += ctx.bucket_counts[b]
        elif b == "paid":
            eligible += ctx.paid_subs
        elif b == "limit_hitter":
            eligible += ctx.limit_hitters
        elif b == "cancelled_paid":
            eligible += ctx.cancelled_paid
        elif b == "waitlist":
            eligible += ctx.launch_audience

    sid = seq["id"]
    if sid in ("welcome", "nps_day3"):
        eligible = ctx.signup_vol
    elif sid == "pmf_day10":
        eligible = round(ctx.signup_vol * ctx.pmf_pct)
    elif sid == "activation_nudge":
        eligible = round(ctx.signup_vol * (1 - ctx.activation_pct))
    elif sid == "dead_resurrection":
        eligible = min(ctx.bucket_counts.get("dead", 0), ctx.dead_cap)
    elif sid in ("ph_teaser", "ph_launch"):
        eligible = ctx.launch_audience if ctx.mode == "launch_week" else 0

    return eligible * cadence, eligible


def _provider_contacts(
    pid: str,
    ctx: SimContext,
    limits: dict[str, dict[str, Any]],
) -> int:
    signup_vol = ctx.signup_vol
    if pid == "omnisend":
        if "omnisend_to_brevo" in ctx.active_rules:
            return 0
        return ctx.paid_subs
    if pid == "hubspot":
        if "ph_week_brevo_primary" in ctx.active_rules:
            return 0
        return signup_vol
    if pid == "mailgun":
        return round(signup_vol * ctx.pmf_pct)
    if pid == "emailoctopus":
        ar = ctx.bucket_counts.get("at_risk_wau", 0) + ctx.bucket_counts.get("at_risk_mau", 0)
        dead = min(ctx.bucket_counts.get("dead", 0), ctx.dead_cap)
        ret = ctx.bucket_counts.get("reactivated", 0) + ctx.bucket_counts.get("resurrected", 0)
        return ar + dead + ret
    if pid == "mailerlite":
        cap = limits.get("emailoctopus", {}).get("contacts", 2500)
        eo_used = _provider_contacts("emailoctopus", ctx, limits)
        if eo_used > cap * 0.8:
            return min(500, round((eo_used - cap * 0.8) * 0.5))
        return 0
    if pid == "brevo":
        base = signup_vol + ctx.limit_hitters + ctx.cancelled_paid + ctx.paid_subs
        if ctx.mode == "launch_week":
            base += ctx.launch_audience
        base += signup_vol + round(signup_vol * ctx.pmf_pct)
        return min(ctx.total_users, base)
    return ctx.total_users


def _effective_provider(seq: dict[str, Any], active_rules: list[str]) -> str:
    pid = seq["provider_id"]
    if "ph_week_brevo_primary" in active_rules and seq["id"] in ("welcome", "activation_nudge"):
        return "brevo"
    if "omnisend_to_brevo" in active_rules and seq["id"] in ("upgrade_thank_you", "cancelled_winback"):
        return "brevo"
    return pid


def simulate_scenario(
    manifest: dict[str, Any],
    *,
    new_users_per_day_max: int | None = None,
    new_users_per_month_max: int | None = None,
    mode: str = "launch_week",
    paid_override: int | None = None,
    snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return scenario simulation matching email-machine.js simulateCapacity()."""
    lc = manifest.get("launch_config") or {}
    base = _baseline(snapshot)
    new_users_day = int(
        new_users_per_day_max if new_users_per_day_max is not None else lc.get("default_new_users_per_day_max") or 7
    )
    new_users_month = int(
        new_users_per_month_max
        if new_users_per_month_max is not None
        else lc.get("default_new_users_per_month_max")
        or 200
    )
    launch_audience = int(lc.get("launch_brevo_audience") or 222)
    launch_days = int(lc.get("launch_window_days") or 3)
    activation_pct = float(lc.get("activation_24h_pct") or 0.32)
    pmf_pct = float(lc.get("pmf_wau_eligible_pct") or 0.40)
    paid_conversion = float(lc.get("paid_conversion_pct") or 0.015)
    agent_reserve = int(lc.get("agent_brevo_daily_reserve") or 50)

    signup_vol = new_users_month
    total_users = base["total_users"] + new_users_month
    auto_paid = max(
        int(base["monetization"].get("paid_subscribers") or 0),
        round(total_users * paid_conversion),
    )
    paid_subs = paid_override if paid_override is not None else auto_paid
    bucket_counts = project_buckets(total_users, new_users_month)

    active_rules: list[str] = []
    if mode == "launch_week" or new_users_month >= 1:
        active_rules.append("ph_week_brevo_primary")
    if paid_subs >= 1:
        active_rules.append("omnisend_to_brevo")

    brevo_prov = next((p for p in manifest.get("providers") or [] if p["id"] == "brevo"), None)
    brevo_starter_limits = (brevo_prov or {}).get("paid_tier", {}).get("limits")

    ctx = SimContext(
        new_users_day=new_users_day,
        new_users_month=new_users_month,
        mode=mode,
        signup_vol=signup_vol,
        total_users=total_users,
        paid_subs=paid_subs,
        limit_hitters=max(
            int(base["monetization"].get("users_hit_limit") or 0),
            round(new_users_month * 0.05),
        ),
        cancelled_paid=int(base["monetization"].get("cancelled_paid_subscribers") or 0),
        bucket_counts=bucket_counts,
        launch_audience=launch_audience,
        activation_pct=activation_pct,
        pmf_pct=pmf_pct,
        dead_cap=20,
        active_rules=active_rules,
        launch_days=launch_days,
        agent_reserve=agent_reserve,
    )

    limits = {p["id"]: p.get("free_limits") or {} for p in manifest.get("providers") or []}
    eo_contacts = _provider_contacts("emailoctopus", ctx, limits)
    if eo_contacts > 2000:
        active_rules.append("emailoctopus_cap")
        ctx.dead_cap = 10
    ctx.active_rules = active_rules

    by_provider: dict[str, float] = {}
    for seq in manifest.get("sequences") or []:
        sends, _ = _seq_eligible(seq, ctx)
        if sends <= 0:
            continue
        pid = _effective_provider(seq, active_rules)
        by_provider[pid] = by_provider.get(pid, 0) + sends
        if seq.get("provider_overflow_id") and new_users_month >= 600:
            ov = seq["provider_overflow_id"]
            by_provider[ov] = by_provider.get(ov, 0) + sends * 0.15

    daily_peaks = _compute_daily_peaks(ctx)
    if daily_peaks.get("brevo", 0) > 240:
        active_rules.append("brevo_daily_overflow")
        pmf_seq = next((s for s in manifest.get("sequences") or [] if s["id"] == "pmf_day10"), None)
        if pmf_seq:
            pmf_sends, _ = _seq_eligible(pmf_seq, ctx)
            by_provider["brevo"] = max(0, by_provider.get("brevo", 0) - pmf_sends)
            by_provider["mailgun"] = by_provider.get("mailgun", 0) + pmf_sends
    ctx.active_rules = active_rules

    brevo_prov = next((p for p in manifest.get("providers") or [] if p["id"] == "brevo"), None)
    brevo_free = (brevo_prov or {}).get("free_limits") or {}
    brevo_starter_limits = (brevo_prov or {}).get("paid_tier", {}).get("limits")
    brevo_contacts_est = _provider_contacts("brevo", ctx, limits)
    use_brevo_starter = (
        paid_subs >= 1
        or daily_peaks.get("brevo", 0) > brevo_free.get("emails_per_day", float("inf"))
        or brevo_contacts_est > brevo_free.get("contacts", float("inf"))
    )

    failures: list[dict[str, Any]] = []
    provider_rows: list[dict[str, Any]] = []

    for prov in manifest.get("providers") or []:
        pid = prov["id"]
        if pid == "brevo" and use_brevo_starter and brevo_starter_limits:
            lim = dict(brevo_starter_limits)
        else:
            lim = limits.get(pid, {})
        monthly = by_provider.get(pid, 0)
        daily_avg = monthly / 30
        contacts = _provider_contacts(pid, ctx, limits)
        metrics: list[dict[str, Any]] = []

        mo_lim = lim.get("marketing_emails_per_month") or lim.get("emails_per_month")
        if mo_lim:
            pct = monthly / mo_lim
            metrics.append({"key": "monthly", "used": monthly, "limit": mo_lim, "pct": pct})
            if pct >= 1:
                failures.append(
                    {"provider": pid, "name": prov["name"], "type": "monthly", "used": monthly, "limit": mo_lim}
                )

        day_lim = lim.get("emails_per_day")
        if day_lim:
            peak = daily_peaks.get(pid, daily_avg)
            use_peak = pid in daily_peaks and daily_peaks[pid] > daily_avg
            daily_used = peak if use_peak else daily_avg
            pct = daily_used / day_lim
            ftype = "launch_peak" if use_peak else "daily"
            metrics.append({"key": ftype, "used": daily_used, "limit": day_lim, "pct": pct})
            if pct >= 1:
                failures.append(
                    {
                        "provider": pid,
                        "name": prov["name"],
                        "type": ftype,
                        "used": daily_used,
                        "limit": day_lim,
                    }
                )

        contact_lim = lim.get("contacts")
        if contact_lim:
            pct = contacts / contact_lim
            metrics.append({"key": "contacts", "used": contacts, "limit": contact_lim, "pct": pct})
            if pct >= 1:
                failures.append(
                    {
                        "provider": pid,
                        "name": prov["name"],
                        "type": "contacts",
                        "used": contacts,
                        "limit": contact_lim,
                    }
                )

        worst = max(metrics, key=lambda m: m["pct"]) if metrics else None
        worst_pct = worst["pct"] if worst else 0
        status = "at_limit" if worst_pct >= 1 else "near_limit" if worst_pct >= 0.8 else "ok"
        provider_rows.append(
            {
                "id": pid,
                "name": prov["name"],
                "monthly_sends": round(monthly),
                "contacts": contacts,
                "status": status,
                "worst_pct": round(worst_pct, 3) if worst else 0,
            }
        )

    failures.sort(
        key=lambda f: (
            FAILURE_PRIORITY.get(f["type"], 9),
            -(f["used"] / f["limit"]) if f["limit"] else 0,
        )
    )

    triggered_cliffs: list[str] = []
    for cliff in manifest.get("capacity_cliffs") or []:
        cid = cliff["id"]
        fire = False
        if cid == "brevo_launch_peak":
            fire = daily_peaks.get("brevo", 0) > 240
        elif cid == "brevo_contacts":
            brevo_row = next((p for p in provider_rows if p["id"] == "brevo"), None)
            fire = bool(brevo_row and brevo_row["contacts"] > 1600)
        elif cid == "hubspot_defer_ph":
            fire = mode == "launch_week" or new_users_month > 400 or new_users_day * 7 > 400
        elif cid == "omnisend_200":
            fire = paid_subs >= 1
        elif cid == "mailgun_pmf_primary":
            fire = new_users_month > 80 or new_users_day * 7 > 80
        elif cid == "emailoctopus_2000":
            fire = eo_contacts > 2000
        elif cid == "mailerlite_overflow":
            fire = "emailoctopus_cap" in active_rules
        elif cid == "brevo_starter_monthly":
            brevo_row = next((p for p in provider_rows if p["id"] == "brevo"), None)
            fire = use_brevo_starter and bool(brevo_row and brevo_row.get("monthly_sends", 0) > 16000)
        elif cid == "brevo_agent":
            fire = daily_peaks.get("brevo", 0) > 250
        if fire:
            triggered_cliffs.append(cid)

    return {
        "new_users_per_day_max": new_users_day,
        "new_users_per_month_max": new_users_month,
        "mode": mode,
        "paid_subs": paid_subs,
        "auto_paid": auto_paid,
        "total_users": total_users,
        "providers": provider_rows,
        "first_stall": failures[0] if failures else None,
        "active_rules": active_rules,
        "triggered_cliffs": triggered_cliffs,
        "daily_peaks": daily_peaks,
    }


def main() -> None:
    manifest = _load_manifest()
    presets = manifest.get("scenario_presets") or []
    snapshot = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))

    print("EMAIL CAPACITY SIMULATION (Python — mirrors /email-machine scenario planner)")
    print(f"Launch audience: {manifest.get('launch_config', {}).get('launch_brevo_audience', 222)} Brevo recipients\n")

    for preset in presets:
        paid = preset.get("paid_override")
        result = simulate_scenario(
            manifest,
            new_users_per_day_max=int(preset.get("new_users_per_day_max") or 0),
            new_users_per_month_max=int(preset.get("new_users_per_month_max") or 0),
            mode=str(preset.get("mode") or "launch_week"),
            paid_override=int(paid) if paid is not None else None,
            snapshot=snapshot,
        )
        stall = result["first_stall"]
        stall_msg = (
            f"FIRST STALL: {stall['name']} — {stall['type']} ({stall['used']:,.0f}/{stall['limit']:,.0f})"
            if stall
            else "No hard stall"
        )
        print(
            f"── {preset.get('label')} "
            f"(day={result['new_users_per_day_max']}, mo={result['new_users_per_month_max']}, mode={result['mode']})"
        )
        print(f"   {stall_msg}")
        if result["active_rules"]:
            print(f"   Rules: {', '.join(result['active_rules'])}")
        if result["triggered_cliffs"]:
            print(f"   Cliffs: {', '.join(result['triggered_cliffs'])}")
        for p in result["providers"]:
            if p["monthly_sends"] > 20 or p["worst_pct"] >= 0.5:
                print(
                    f"   {p['id']:12} {p['monthly_sends']:>6,} sends/mo  "
                    f"{p['contacts']:>5,} contacts  {p['worst_pct']*100:.0f}% worst"
                )
        print()


if __name__ == "__main__":
    main()
