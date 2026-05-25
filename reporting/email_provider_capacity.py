"""Estimate free-tier email provider usage and near-limit status from snapshot data."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "public" / "email_sequences.json"

CADENCE_SENDS: dict[str, int] = {
    "one-time": 1,
    "one-time-broadcast": 1,
    "drip-2-4": 3,
    "one-time-plus-d7": 2,
    "campaign-2-touch": 2,
    "one-time-plus-d14": 2,
}

DEFAULT_NEAR_LIMIT = {
    "contacts_pct": 0.8,
    "sends_monthly_pct": 0.8,
    "sends_daily_pct": 0.8,
    "runway_months_min": 2,
}

FALLBACK_PROVIDER_IDS = frozenset({"mailerlite", "omnisend", "brevo", "loops"})
OPERATIONAL_PROVIDER_IDS = frozenset({"resend", "ses"})


def _load_manifest(path: Path | None = None) -> dict[str, Any]:
    p = path or MANIFEST_PATH
    return json.loads(p.read_text(encoding="utf-8"))


def _eligible_cohort(
    buckets: list[str],
    *,
    bucket_counts: dict[str, int],
    monetization: dict[str, Any],
    corporate_goals: dict[str, Any],
    total_users: int = 0,
) -> int:
    total = 0
    launch = (corporate_goals or {}).get("launch") or {}
    for key in buckets or []:
        if key == "operational_all":
            total += total_users
        elif key in bucket_counts:
            total += int(bucket_counts.get(key) or 0)
        elif key == "paid":
            total += int(monetization.get("paid_subscribers") or 0)
        elif key == "limit_hitter":
            total += int(monetization.get("users_hit_limit") or 0)
        elif key == "cancelled_paid":
            total += int(monetization.get("cancelled_paid_subscribers") or 0)
        elif key == "waitlist":
            total += int(launch.get("waitlist") or 0)
    return total


def _touch_count(seq: dict[str, Any], manifest: dict[str, Any]) -> int:
    touches = seq.get("touches")
    if touches:
        return len(touches)
    cadence_map = manifest.get("cadence_touch_counts") or CADENCE_SENDS
    return cadence_map.get(seq.get("cadence") or "one-time", 1)


def _projected_sends_for_provider(
    provider_id: str,
    sequences: list[dict[str, Any]],
    manifest: dict[str, Any],
    *,
    bucket_counts: dict[str, int],
    monetization: dict[str, Any],
    corporate_goals: dict[str, Any],
    total_users: int = 0,
) -> float:
    monthly = 0.0
    for seq in sequences:
        if seq.get("provider_id") != provider_id:
            continue
        if seq.get("funnel_phase") == "operational":
            continue
        sends_per_user = _touch_count(seq, manifest)
        eligible = _eligible_cohort(
            seq.get("buckets") or [],
            bucket_counts=bucket_counts,
            monetization=monetization,
            corporate_goals=corporate_goals,
            total_users=total_users,
        )
        monthly += eligible * sends_per_user
    return monthly


def _consumer_domains(manifest: dict[str, Any]) -> set[str]:
    lc = manifest.get("launch_config") or {}
    domains = lc.get("consumer_email_domains")
    if domains:
        return {d.lower() for d in domains}
    return {
        "gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "hotmail.co.uk",
        "icloud.com", "protonmail.com", "protonmail.ch", "me.com", "mac.com",
        "live.com", "live.co.uk", "yahoo.co.uk", "googlemail.com", "msn.com",
    }


def _company_email_users(total_users: int, manifest: dict[str, Any]) -> int:
    lc = manifest.get("launch_config") or {}
    pct = float(lc.get("company_email_pct") or 0.15)
    return round(total_users * pct)


def _pool_aggregate(
    provider_rows: list[dict[str, Any]],
    providers: list[dict[str, Any]],
) -> dict[str, Any]:
    pool_ids = [
        p["id"]
        for p in providers
        if p["id"] in FALLBACK_PROVIDER_IDS and p.get("status") != "deprecated"
    ]
    send_used = 0.0
    send_cap = 0.0
    contact_used = 0
    contact_cap = 0
    for row in provider_rows:
        if row["id"] not in pool_ids:
            continue
        send_used += float(row.get("monthly_sends_projected") or 0)
        prov = next((p for p in providers if p["id"] == row["id"]), None)
        lim = (prov or {}).get("free_limits") or {}
        mo = lim.get("marketing_emails_per_month") or lim.get("emails_per_month")
        if not mo and lim.get("emails_per_day"):
            mo = lim["emails_per_day"] * 30
        if mo:
            send_cap += mo
        if lim.get("contacts"):
            contact_cap += lim["contacts"]
            contact_used += int(row.get("contacts_used") or 0)
    return {
        "send_used": round(send_used, 1),
        "send_cap": round(send_cap, 1),
        "contact_used": contact_used,
        "contact_cap": contact_cap,
        "provider_count": len(pool_ids),
    }


def _operational_blast_sends_per_month(
    sequences: list[dict[str, Any]],
    *,
    total_users: int,
    blasts_per_month: float = 0.25,
) -> float:
    """Rough capacity: fraction of userbase × active operational sequences (manual blasts)."""
    op_count = sum(1 for s in sequences if s.get("funnel_phase") == "operational")
    if not op_count:
        return 0.0
    return total_users * blasts_per_month * op_count


def _operational_pool_aggregate(
    provider_rows: list[dict[str, Any]],
    manifest: dict[str, Any],
    *,
    sequences: list[dict[str, Any]] | None = None,
    total_users: int = 0,
) -> dict[str, Any]:
    """Resend + SES (+ Brevo emergency) — legal/incident lane."""
    pool = manifest.get("operational_pool") or {}
    pool_ids = pool.get("provider_ids") or list(OPERATIONAL_PROVIDER_IDS)
    sequences = sequences or manifest.get("sequences") or []
    send_used = _operational_blast_sends_per_month(sequences, total_users=total_users)
    send_cap = 0.0
    daily_cap = 0.0
    daily_used = send_used / 30.0
    for row in provider_rows:
        if row["id"] not in pool_ids:
            continue
        prov = next((p for p in manifest.get("providers") or [] if p["id"] == row["id"]), None)
        lim = (prov or {}).get("free_limits") or {}
        mo = lim.get("emails_per_month")
        if mo:
            send_cap += mo
        if lim.get("emails_per_day"):
            daily_cap += lim["emails_per_day"]
    agg = pool.get("aggregate_free_limits") or {}
    if agg.get("sends_per_month"):
        send_cap = max(send_cap, agg["sends_per_month"])
    if agg.get("sends_per_day"):
        daily_cap = max(daily_cap, agg["sends_per_day"])
    return {
        "send_used": round(send_used, 1),
        "send_cap": round(send_cap, 1),
        "daily_used": round(daily_used, 1),
        "daily_cap": round(daily_cap, 1),
        "provider_count": len(pool_ids),
        "primary_provider_id": pool.get("primary_provider_id", "resend"),
    }


def _contact_usage(
    provider_id: str,
    *,
    total_users: int,
    monetization: dict[str, Any],
    manifest: dict[str, Any],
    bucket_counts: dict[str, int],
) -> int:
    if provider_id == "beehiiv":
        return total_users
    if provider_id == "omnisend":
        return 0
    if provider_id == "hubspot":
        paid = int(monetization.get("paid_subscribers") or 0)
        return _company_email_users(total_users, manifest) + paid
    if provider_id == "emailoctopus":
        ar = int(bucket_counts.get("at_risk_wau") or 0) + int(bucket_counts.get("at_risk_mau") or 0)
        dead = int(bucket_counts.get("dead") or 0)
        ret = int(bucket_counts.get("reactivated") or 0) + int(bucket_counts.get("resurrected") or 0)
        return ar + dead + ret
    if provider_id == "mailerlite":
        return min(500, max(0, total_users - 2000)) if total_users > 2000 else 0
    if provider_id == "mailgun":
        return int(monetization.get("paid_subscribers") or 0) + int(
            monetization.get("cancelled_paid_subscribers") or 0
        )
    if provider_id == "brevo":
        return min(total_users, total_users)
    if provider_id in OPERATIONAL_PROVIDER_IDS:
        return total_users
    if provider_id == "loops":
        return min(1000, max(0, total_users - 2000)) if total_users > 2000 else min(total_users, 200)
    return int(total_users)


def _metric_row(
    key: str,
    used: float,
    limit: float | None,
    threshold_pct: float,
) -> dict[str, Any] | None:
    if limit is None or limit <= 0:
        return None
    pct = used / limit
    near = pct >= threshold_pct
    at = pct >= 1.0
    return {
        "key": key,
        "used": round(used, 1) if isinstance(used, float) else int(used),
        "limit": int(limit),
        "pct": round(pct, 3),
        "near_limit": near and not at,
        "at_limit": at,
    }


def _runway_months(monthly_sends: float, monthly_limit: float | None) -> float | None:
    if monthly_limit is None or monthly_limit <= 0 or monthly_sends <= 0:
        return None
    return round(monthly_limit / monthly_sends, 2)


def _provider_status(
    metrics: list[dict[str, Any]],
    runway: float | None,
    runway_min: float,
) -> str:
    if any(m.get("at_limit") for m in metrics):
        return "at_limit"
    if any(m.get("near_limit") for m in metrics):
        return "near_limit"
    if runway is not None and runway < runway_min:
        return "near_limit"
    return "ok"


def _near_limit_errors(
    provider_name: str,
    metrics: list[dict[str, Any]],
    runway: float | None,
    runway_min: float,
) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    labels = {
        "contacts": "contacts",
        "sends_monthly": "monthly sends",
        "sends_daily": "daily sends",
    }
    for m in metrics:
        if not (m.get("near_limit") or m.get("at_limit")):
            continue
        label = labels.get(m["key"], m["key"])
        pct_display = round(100 * m["pct"])
        code = f"NEAR_LIMIT_{m['key'].upper()}"
        if m.get("at_limit"):
            code = code.replace("NEAR_", "AT_")
        errors.append(
            {
                "code": code,
                "message": (
                    f"{provider_name} {label} at {pct_display}% of "
                    f"{m['limit']:,} cap ({m['used']:,} used)"
                ),
            }
        )
    if runway is not None and runway < runway_min:
        errors.append(
            {
                "code": "NEAR_LIMIT_RUNWAY",
                "message": (
                    f"{provider_name} send runway {runway} months "
                    f"(upgrade when < {runway_min} months)"
                ),
            }
        )
    return errors


def compute_email_provider_capacity(
    snapshot: dict[str, Any],
    manifest: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return provider capacity block for baseline snapshot JSON."""
    manifest = manifest or _load_manifest()
    providers = manifest.get("providers") or []
    sequences = manifest.get("sequences") or []

    dau = snapshot.get("dau_model") or {}
    bucket_counts = dau.get("bucket_counts") or {}
    monetization = snapshot.get("monetization") or {}
    corporate_goals = snapshot.get("corporate_goals") or {}
    total_users = int(snapshot.get("total_users") or 0)
    as_of = dau.get("as_of") or snapshot.get("snapshot_date")

    provider_rows: list[dict[str, Any]] = []
    any_near_limit = False

    for prov in providers:
        if prov.get("status") == "deprecated":
            continue
        pid = prov["id"]
        name = prov.get("name") or pid
        limits = prov.get("free_limits") or {}
        thresholds = {**DEFAULT_NEAR_LIMIT, **(prov.get("near_limit") or {})}

        contacts_used = _contact_usage(
            pid,
            total_users=total_users,
            monetization=monetization,
            manifest=manifest,
            bucket_counts=bucket_counts,
        )
        monthly_sends = _projected_sends_for_provider(
            pid,
            sequences,
            manifest,
            bucket_counts=bucket_counts,
            monetization=monetization,
            corporate_goals=corporate_goals,
            total_users=total_users,
        )
        daily_sends = monthly_sends / 30.0

        metrics: list[dict[str, Any]] = []
        if limits.get("contacts") is not None:
            row = _metric_row(
                "contacts",
                contacts_used,
                limits["contacts"],
                thresholds["contacts_pct"],
            )
            if row:
                metrics.append(row)

        monthly_limit = limits.get("marketing_emails_per_month") or limits.get("emails_per_month")
        if monthly_limit is not None:
            row = _metric_row(
                "sends_monthly",
                monthly_sends,
                monthly_limit,
                thresholds["sends_monthly_pct"],
            )
            if row:
                metrics.append(row)

        if limits.get("emails_per_day") is not None:
            row = _metric_row(
                "sends_daily",
                daily_sends,
                limits["emails_per_day"],
                thresholds["sends_daily_pct"],
            )
            if row:
                metrics.append(row)

        runway = _runway_months(monthly_sends, monthly_limit)
        status = _provider_status(metrics, runway, thresholds["runway_months_min"])
        if prov.get("implementation_status") == "blocked_sandbox":
            status = "blocked_sandbox"
        errors = _near_limit_errors(
            name, metrics, runway, thresholds["runway_months_min"]
        )

        if status in ("near_limit", "at_limit"):
            any_near_limit = True

        provider_rows.append(
            {
                "id": pid,
                "name": name,
                "funnel_role": prov.get("funnel_role"),
                "status": status,
                "contacts_used": contacts_used,
                "contacts_limit": limits.get("contacts"),
                "monthly_sends_projected": round(monthly_sends, 1),
                "monthly_sends_limit": monthly_limit,
                "daily_sends_projected": round(daily_sends, 1),
                "daily_sends_limit": limits.get("emails_per_day"),
                "runway_months": runway,
                "metrics": metrics,
                "near_limit_errors": errors,
            }
        )

    pool = _pool_aggregate(provider_rows, providers)
    op_pool = _operational_pool_aggregate(
        provider_rows, manifest, sequences=sequences, total_users=total_users
    )
    ses_prov = next((p for p in providers if p["id"] == "ses"), None)
    ses_sandbox = bool(ses_prov and ses_prov.get("production_pending"))

    return {
        "as_of": as_of,
        "providers": provider_rows,
        "pool_aggregate": pool,
        "operational_pool_aggregate": op_pool,
        "ses_sandbox": ses_sandbox,
        "any_near_limit": any_near_limit,
        "estimation_note": (
            "v1 estimates: Beehiiv Phase 1 contacts; EmailOctopus Phase 2 conversion; "
            "fallback pool = MailerLite + OmniSend + Brevo + Loops; "
            "operational pool = Resend + SES (legal/incident); HubSpot = paid + company email."
        ),
    }
