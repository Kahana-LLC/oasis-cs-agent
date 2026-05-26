"""Rule-based key insights focused on churn and dead-user levers."""

from __future__ import annotations

from typing import Any

SEVERITY_ORDER = {"high": 0, "medium": 1, "info": 2}


def _delta_metric(deltas: dict, period: str, key: str) -> dict[str, Any] | None:
    block = deltas.get(period) or {}
    return (block.get("metrics") or {}).get(key)


def _fmt_delta(d: dict[str, Any] | None, *, unit: str = "") -> str:
    if not d:
        return ""
    ac = d.get("abs_change")
    pc = d.get("pct_change")
    if ac is None:
        return ""
    sign = "+" if ac > 0 else ""
    part = f"{sign}{ac}{unit}"
    if pc is not None:
        part += f" ({sign}{pc}% vs prior)"
    return part


def _add_item(
    items: list[dict[str, Any]],
    *,
    severity: str,
    title: str,
    detail: str,
    lever: str,
    metrics: list[str],
    anchor: str,
) -> None:
    items.append(
        {
            "severity": severity,
            "title": title,
            "detail": detail,
            "lever": lever,
            "metrics": metrics,
            "anchor": anchor,
        }
    )


def _goal_gap_insights(
    snapshot: dict[str, Any],
    deltas: dict[str, Any],
    corporate_goals: dict[str, Any],
    period: str,
) -> list[dict[str, Any]]:
    """High-priority insights tied to corporate goals."""
    items: list[dict[str, Any]] = []
    corp = corporate_goals or {}
    launch = corp.get("launch") or {}
    subs = corp.get("subscribers") or {}
    margin = corp.get("gross_margin_pct") or {}
    dau_g = corp.get("dau_multiple") or {}

    if not launch.get("post_launch") and launch.get("days_until", 99) <= 7:
        days = launch.get("days_until", 0)
        lo, hi = launch.get("ph_signup_range", [200, 2000])
        _add_item(
            items,
            severity="high",
            title=f"Product Hunt in {days} days",
            detail=(
                f"Launch May 27 ~3am ET may add {lo}–{hi} users on top of "
                f"{launch.get('waitlist', 176)} waitlist. "
                f"Subscriber goal: {subs.get('target_year_end', 500)} by Dec 31."
            ),
            lever="Maximize 24h activation and limit-hitter → paid conversion before and during launch.",
            metrics=["activation_24h_pct", "premium_conversion_pct"],
            anchor="activation",
        )

    if not subs.get("on_track_month", subs.get("on_track")):
        gap = subs.get("gap", 0)
        month_tgt = subs.get("month_target", subs.get("target", 0))
        year_tgt = subs.get("target_year_end", 500)
        d_sub = _delta_metric(deltas, period, "premium_conversion_pct")
        trend_note = ""
        if d_sub and d_sub.get("direction") in ("down", "flat"):
            trend_note = f" Conversion trend: {_fmt_delta(d_sub, unit=' pp')}."
        _add_item(
            items,
            severity="high",
            title="Subscriber goal gap",
            detail=(
                f"{subs.get('current', 0)} paid subscribers — "
                f"{subs.get('month_label', 'this month')} target {month_tgt} "
                f"({subs.get('gap', 0)} behind). "
                f"Year-end goal: {year_tgt} by Dec 31 "
                f"({subs.get('gap_year_end', 0)} to go).{trend_note}"
            ),
            lever="Improve upgrade path at token limit; resurrect engaged free users.",
            metrics=["premium_conversion_pct", "limit_hitter_conversion_pct"],
            anchor="monetization",
        )

    if margin.get("current") is not None and not margin.get("on_track"):
        _add_item(
            items,
            severity="high",
            title="Gross margin below 80% target",
            detail=(
                f"Current gross margin {margin.get('current')}% vs "
                f"{margin.get('target', 80)}% goal (gap {margin.get('gap_pp')} pp)."
            ),
            lever="Reduce API burn per user and grow paid conversion to improve margin.",
            metrics=["gross_margin_pct", "arpu_net_usd"],
            anchor="monetization",
        )

    dau_status = dau_g.get("status")
    if dau_status == "locked" and not dau_g.get("on_track"):
        _add_item(
            items,
            severity="medium",
            title="DAU below 4.5× launch-week baseline",
            detail=(
                f"Current {dau_g.get('multiple')}× vs baseline {dau_g.get('baseline')} "
                f"(goal {dau_g.get('target_multiple')}×)."
            ),
            lever="Focus resurrection and at-risk WAU recovery to grow DAU.",
            metrics=["dau", "bucket_dead", "flow_Resurrection_Rate"],
            anchor="dau-model",
        )
    elif dau_status in ("pending_baseline", "collecting_baseline"):
        _add_item(
            items,
            severity="info",
            title="DAU growth baseline not locked yet",
            detail="4.5× goal vs launch-week average locks after 7 days post–Product Hunt.",
            lever="Run daily baseline snapshots through launch week.",
            metrics=["dau"],
            anchor="dau-model",
        )

    return items


def _email_provider_capacity_insights(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    """Near-limit alerts for free-tier email providers."""
    items: list[dict[str, Any]] = []
    cap = snapshot.get("email_provider_capacity") or {}
    for prov in cap.get("providers") or []:
        status = prov.get("status")
        if status not in ("near_limit", "at_limit"):
            continue
        errors = prov.get("near_limit_errors") or []
        detail = errors[0]["message"] if errors else f"{prov.get('name')} approaching free-tier cap."
        severity = "high" if status == "at_limit" else "high"
        _add_item(
            items,
            severity=severity,
            title=f"Email provider near limit: {prov.get('name')}",
            detail=detail + " See /email-machine#provider-capacity for capacity panel.",
            lever="Upgrade provider, enable overflow routing, or prune contact lists before PH burst.",
            metrics=["email_provider_capacity"],
            anchor="/email-machine#provider-capacity",
        )
    return items


def _lifecycle_readiness_insights(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    """Bucket × product milestone gaps for email plan levers."""
    items: list[dict[str, Any]] = []
    lr = snapshot.get("lifecycle_readiness") or {}
    by_bucket = lr.get("by_bucket") or {}
    dau = snapshot.get("dau_model") or {}
    bucket_counts = dau.get("bucket_counts") or {}

    dead = by_bucket.get("dead") or {}
    dead_n = dead.get("users") or bucket_counts.get("dead", 0)
    dead_prompt = (dead.get("milestones") or {}).get("first_ai_prompt") or {}
    dead_prompt_pct = dead_prompt.get("pct")

    if dead_n >= 10 and dead_prompt_pct is not None and dead_prompt_pct < 30:
        _add_item(
            items,
            severity="medium",
            title="Most dead users never activated AI",
            detail=(
                f"{dead_n} dead users — only {dead_prompt_pct}% ever sent a first AI prompt. "
                "Resurrection flows should assume low product depth."
            ),
            lever="Prioritize dead-bucket resurrection sequences; pair with browser-import onboarding for re-engaged users.",
            metrics=["bucket_dead"],
            anchor="lifecycle-readiness",
        )

    new_b = by_bucket.get("new") or {}
    new_n = new_b.get("users") or bucket_counts.get("new", 0)
    new_training = (new_b.get("milestones") or {}).get("training_done") or {}
    new_training_pct = new_training.get("pct")

    if new_n >= 3 and new_training_pct is not None and new_training_pct < 25:
        _add_item(
            items,
            severity="info",
            title="New users rarely training the AI assistant",
            detail=(
                f"{new_n} new users — {new_training_pct}% have trained the assistant (feedback_events). "
                "Training is a sticky deep-feature signal before Phase 2 fork."
            ),
            lever="Nudge training in activation CS calendar outreach; highlight 1,000-token reward.",
            metrics=["feedback_submission_rate_pct", "activation_24h_pct"],
            anchor="lifecycle-readiness",
        )

    pending = [m for m in (lr.get("milestones") or []) if m.get("status") == "pending"]
    if pending:
        _add_item(
            items,
            severity="info",
            title="Email send milestones not tracked yet",
            detail=(
                f"{len(pending)} readiness email columns pending — cs_outreach_log could not be loaded. "
                "Product milestones (prompt, limit, training) are live in the matrix below."
            ),
            lever="Verify Supabase service role can read cs_outreach_log.",
            metrics=[],
            anchor="lifecycle-readiness",
        )

    sends = snapshot.get("lifecycle_email_sends") or {}
    cohort = sends.get("cohort") or {}
    if sends.get("outreach_log_available") and cohort.get("users", 0) >= 5:
        by_trigger = {t["dedup_trigger_name"]: t for t in cohort.get("triggers") or []}
        welcome = by_trigger.get("welcome_email") or {}
        welcome_pct = welcome.get("pct_of_cohort")
        if welcome_pct is not None and welcome_pct < 80:
            _add_item(
                items,
                severity="medium",
                title="Low welcome email coverage for recent signups",
                detail=(
                    f"Only {welcome_pct}% of users who signed up in the last "
                    f"{sends.get('new_user_window_days', 30)} days received welcome_email "
                    f"({welcome.get('sent_count', 0)}/{cohort.get('users', 0)})."
                ),
                lever="Check lifecycle-on-signup webhook on users INSERT and Brevo template delivery.",
                metrics=[],
                anchor="lifecycle-email-sends",
            )

    return items


def _lifecycle_delivery_insights(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    """Missed sends, cron staleness, RPC cap warnings."""
    items: list[dict[str, Any]] = []
    delivery = snapshot.get("lifecycle_email_delivery") or {}
    if not delivery.get("outreach_log_available"):
        return items

    cfg = {}
    try:
        import json
        from pathlib import Path

        manifest = Path(__file__).resolve().parents[1] / "public" / "email_sequences.json"
        if manifest.exists():
            data = json.loads(manifest.read_text(encoding="utf-8"))
            cfg = (data.get("launch_config") or {}).get("lifecycle_reporting") or {}
    except Exception:
        pass

    thresholds = cfg.get("delivery_insight_thresholds") or {}
    welcome_min = float(thresholds.get("welcome_min_pct") or 95)
    cron_stale_hours = int(thresholds.get("cron_stale_hours") or 26)

    if delivery.get("any_eligible_now_capped"):
        _add_item(
            items,
            severity="high",
            title="Lifecycle cohort may be truncated at 500 users",
            detail=(
                "At least one trigger shows exactly 500 users due now — daily cron "
                "only processes 500 per trigger. Raise cron limit or run twice during PH spikes."
            ),
            lever="Increase lifecycle-daily-cron limit in pg_cron body; see LIFECYCLE_PH_LAUNCH_MONITORING.md",
            metrics=[],
            anchor="lifecycle-email-delivery",
        )

    missed_total = delivery.get("missed_total") or 0
    if missed_total > 0:
        by_t = delivery.get("missed_by_trigger") or {}
        parts = [f"{k}: {v}" for k, v in by_t.items() if v]
        _add_item(
            items,
            severity="high",
            title="Lifecycle emails missed (overdue, not in cs_outreach_log)",
            detail=(
                f"{missed_total} user(s) in the signup window should have received "
                f"emails but have no log row: {'; '.join(parts)}."
            ),
            lever="Check lifecycle-on-signup webhook, pg_cron job_run_details, and Brevo delivery.",
            metrics=[],
            anchor="lifecycle-email-delivery",
        )

    triggers = delivery.get("triggers") or []
    welcome = next((t for t in triggers if t.get("dedup_trigger_name") == "welcome_email"), {})
    welcome_rate = welcome.get("delivery_rate_pct")
    if welcome_rate is not None and welcome_rate < welcome_min:
        _add_item(
            items,
            severity="high",
            title="Welcome email delivery below target",
            detail=(
                f"Welcome delivery rate is {welcome_rate}% in the last "
                f"{delivery.get('new_user_window_days', 30)}-day signup window "
                f"(target {welcome_min}%)."
            ),
            lever="Verify users INSERT webhook → lifecycle-on-signup and Brevo template 54.",
            metrics=[],
            anchor="lifecycle-email-delivery",
        )

    cron_sent_24h = delivery.get("cron_sent_last_24h") or 0
    cron_eligible = delivery.get("cron_eligible_now") or 0
    if cron_eligible > 0 and cron_sent_24h == 0:
        _add_item(
            items,
            severity="high",
            title="Daily lifecycle cron may not have run recently",
            detail=(
                f"{cron_eligible} users are due for cron emails now but zero cron "
                f"sends logged in the last 24h (stale threshold {cron_stale_hours}h)."
            ),
            lever="Check pg_cron lifecycle-daily-cron job_run_details and Edge function logs.",
            metrics=[],
            anchor="lifecycle-email-delivery",
        )

    return items


def generate_key_insights(
    snapshot: dict[str, Any],
    deltas: dict[str, Any],
    corporate_goals: dict[str, Any] | None = None,
    period: str = "weekly",
) -> dict[str, Any]:
    """Build churn-focused insight cards from snapshot + deltas + goals."""
    dau = snapshot.get("dau_model") or {}
    buckets = dau.get("bucket_counts") or {}
    flow = dau.get("flow_rates_pct") or {}
    total = snapshot.get("total_users") or 1
    dead = buckets.get("dead", 0)
    at_risk_wau = buckets.get("at_risk_wau", 0)
    at_risk_mau = buckets.get("at_risk_mau", 0)
    dead_pct = round(100.0 * dead / total, 1) if total else 0

    items: list[dict[str, Any]] = _goal_gap_insights(
        snapshot, deltas, corporate_goals or {}, period
    )
    items.extend(_email_provider_capacity_insights(snapshot))
    items.extend(_lifecycle_readiness_insights(snapshot))
    items.extend(_lifecycle_delivery_insights(snapshot))
    d_dead = _delta_metric(deltas, period, "bucket_dead")
    d_at_wau = _delta_metric(deltas, period, "bucket_at_risk_wau")
    d_at_mau = _delta_metric(deltas, period, "bucket_at_risk_mau")
    d_churn7 = _delta_metric(deltas, period, "churn_7d_pct")
    d_d7 = _delta_metric(deltas, period, "retention_d7_pct")
    d_wau = _delta_metric(deltas, period, "latest_wau")
    d_activation = _delta_metric(deltas, period, "activation_24h_pct")

    resurrection = flow.get("Resurrection_Rate")
    mau_loss = flow.get("MAU_Loss_Rate")
    nurr = flow.get("NURR")
    one_nurr = flow.get("1-NURR")
    one_curr = flow.get("1-CURR")
    iwaurr = flow.get("iWAURR")

    if d_dead and d_dead.get("significant") and d_dead.get("direction") == "up":
        _add_item(
            items,
            severity="high",
            title="Dead user pool is growing",
            detail=(
                f"{dead} users ({dead_pct}% of base) are in the dead bucket. "
                f"Weekly change: {_fmt_delta(d_dead, unit=' users')}."
            ),
            lever=(
                "Run win-back campaigns; improve Resurrection_Rate vs MAU_Loss_Rate. "
                "Target users before they cross 30 days inactive."
            ),
            metrics=["bucket_dead", "flow_Resurrection_Rate", "flow_MAU_Loss_Rate"],
            anchor="dau-model",
        )
    elif dead_pct >= 50:
        _add_item(
            items,
            severity="high",
            title="Majority of users are dead",
            detail=f"{dead_pct}% of users ({dead}/{total}) have had no activity in 30+ days.",
            lever="Prioritize resurrection email flows and at-risk prevention (iWAURR).",
            metrics=["bucket_dead"],
            anchor="dau-model",
        )

    if d_at_wau and d_at_wau.get("significant") and d_at_wau.get("direction") == "up":
        _add_item(
            items,
            severity="high",
            title="At-risk WAU cohort is expanding",
            detail=(
                f"{at_risk_wau} users were active last week but not today "
                f"({_fmt_delta(d_at_wau, unit=' users')})."
            ),
            lever="Re-engage within 7 days — improve iWAURR before they slide to at-risk MAU or dead.",
            metrics=["bucket_at_risk_wau", "flow_iWAURR"],
            anchor="dau-model",
        )

    if d_at_mau and d_at_mau.get("significant") and d_at_mau.get("direction") == "up":
        _add_item(
            items,
            severity="medium",
            title="At-risk MAU is rising",
            detail=(
                f"{at_risk_mau} users inactive 7+ days but active within 30 "
                f"({_fmt_delta(d_at_mau, unit=' users')})."
            ),
            lever="Use iMAURR-focused nudges; prevent MAU_Loss_Rate into dead.",
            metrics=["bucket_at_risk_mau", "flow_iMAURR", "flow_MAU_Loss_Rate"],
            anchor="dau-model",
        )

    if d_churn7 and d_churn7.get("significant") and d_churn7.get("direction") == "up":
        _add_item(
            items,
            severity="high",
            title="7-day churn is worsening",
            detail=f"More ever-active users are going quiet ({_fmt_delta(d_churn7, unit=' pp')}).",
            lever="Identify last-active cohort; session and email nudges within 48h of drop-off.",
            metrics=["churn_7d_pct"],
            anchor="retention",
        )

    if d_d7 and d_d7.get("significant") and d_d7.get("direction") == "down":
        _add_item(
            items,
            severity="medium",
            title="Day-7 retention is slipping",
            detail=f"Fewer users return on day 7 ({_fmt_delta(d_d7, unit=' pp')}).",
            lever="Strengthen first-week activation and multi-day AI habits.",
            metrics=["retention_d7_pct", "activation_24h_pct"],
            anchor="activation",
        )

    if d_wau and d_wau.get("significant") and d_wau.get("direction") == "down":
        _add_item(
            items,
            severity="medium",
            title="Weekly active users declined",
            detail=f"WAU dropped {_fmt_delta(d_wau, unit=' users')}.",
            lever="Balance top-of-funnel with reactivation of at-risk and dead users.",
            metrics=["latest_wau"],
            anchor="retention",
        )

    if nurr is not None and nurr < 40 and one_nurr is not None and one_nurr > 30:
        _add_item(
            items,
            severity="medium",
            title="New users are not sticking as Current",
            detail=f"NURR {nurr}% vs 1-NURR {one_nurr}% — many new users slip to at-risk WAU.",
            lever="Improve onboarding and day-1/2 return prompts.",
            metrics=["flow_NURR", "flow_1-NURR"],
            anchor="dau-model",
        )

    if one_curr is not None and one_curr > 25:
        _add_item(
            items,
            severity="medium",
            title="Current users are slipping to at-risk",
            detail=f"1-CURR {one_curr}% — habitual users missing days.",
            lever="Habit loops, return triggers, and session reminders.",
            metrics=["flow_1-CURR", "flow_CURR"],
            anchor="dau-model",
        )

    if resurrection is not None and mau_loss is not None and resurrection < mau_loss:
        _add_item(
            items,
            severity="medium",
            title="More users dying than resurrecting",
            detail=f"Resurrection_Rate {resurrection}% vs MAU_Loss_Rate {mau_loss}%.",
            lever="Invest in dead → resurrected campaigns; test win-back offers.",
            metrics=["flow_Resurrection_Rate", "flow_MAU_Loss_Rate"],
            anchor="dau-model",
        )

    if iwaurr is not None and iwaurr < 20 and at_risk_wau > 0:
        _add_item(
            items,
            severity="info",
            title="Low recovery from at-risk WAU",
            detail=f"Only {iwaurr}% of at-risk WAU return to Current today.",
            lever="Test same-day or next-day re-engagement for users who missed one day.",
            metrics=["flow_iWAURR"],
            anchor="dau-model",
        )

    mon = snapshot.get("monetization") or {}
    lhc = mon.get("premium_conversion_among_limit_hitters_pct")
    if lhc is not None and lhc < 50:
        _add_item(
            items,
            severity="info",
            title="Limit-hitters are not converting to paid",
            detail=f"Only {lhc}% of users who hit token limits are on Plus.",
            lever="Improve upgrade UX at limit moment.",
            metrics=["limit_hitter_conversion_pct"],
            anchor="monetization",
        )

    if d_activation and d_activation.get("significant") and d_activation.get("direction") == "down":
        _add_item(
            items,
            severity="medium",
            title="24h activation is down",
            detail=f"Fewer new users prompt quickly ({_fmt_delta(d_activation, unit=' pp')}).",
            lever="Fix first-run experience and time-to-first-prompt.",
            metrics=["activation_24h_pct"],
            anchor="activation",
        )

    if not items:
        _add_item(
            items,
            severity="info",
            title="No major churn shifts detected this period",
            detail=(
                f"Dead users: {dead} ({dead_pct}%). "
                "Keep daily snapshots to unlock trend-based alerts."
            ),
            lever="Continue monitoring at-risk WAU/MAU and resurrection vs MAU loss.",
            metrics=["bucket_dead", "bucket_at_risk_wau"],
            anchor="dau-model",
        )

    items.sort(key=lambda x: SEVERITY_ORDER.get(x["severity"], 9))

    corp = corporate_goals or {}
    subs = corp.get("subscribers") or {}
    if subs and not subs.get("on_track_month", subs.get("on_track")):
        summary_parts_goal = [
            f"Subscribers: {subs.get('current', 0)}/{subs.get('month_target', subs.get('target', 0))} "
            f"this month ({subs.get('target_year_end', 500)} by Dec 31)"
        ]
    else:
        summary_parts_goal = []

    weekly_dead = _fmt_delta(d_dead, unit=" users")
    summary_parts = list(summary_parts_goal)
    if weekly_dead:
        summary_parts.append(f"Dead users changed {weekly_dead} vs last week")
    if dead_pct >= 40:
        summary_parts.append(f"{dead_pct}% of the base is dead")
    if at_risk_wau + at_risk_mau > 0:
        summary_parts.append(
            f"{at_risk_wau + at_risk_mau} users are at-risk (recoverable before 30d dead)"
        )
    summary = (
        ". ".join(summary_parts) + ". Focus on at-risk WAU and resurrection levers."
        if summary_parts
        else "Review DAU buckets and flow rates to prioritize resurrection and at-risk recovery."
    )

    focus: list[str] = []
    if dead_pct >= 30 or (d_dead and d_dead.get("direction") == "up"):
        focus.append("resurrection")
    if at_risk_wau > 0:
        focus.append("at_risk_wau")
    if at_risk_mau > 0:
        focus.append("at_risk_mau")
    if d_activation or (nurr is not None and nurr < 40):
        focus.append("activation")

    return {
        "summary": summary,
        "items": items[:8],
        "focus_areas": focus or ["resurrection", "at_risk_wau"],
        "delta_period_used": period,
    }
