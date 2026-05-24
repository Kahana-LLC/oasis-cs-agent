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


def generate_key_insights(
    snapshot: dict[str, Any],
    deltas: dict[str, Any],
    period: str = "weekly",
) -> dict[str, Any]:
    """Build churn-focused insight cards from snapshot + deltas."""
    dau = snapshot.get("dau_model") or {}
    buckets = dau.get("bucket_counts") or {}
    flow = dau.get("flow_rates_pct") or {}
    total = snapshot.get("total_users") or 1
    dead = buckets.get("dead", 0)
    at_risk_wau = buckets.get("at_risk_wau", 0)
    at_risk_mau = buckets.get("at_risk_mau", 0)
    dead_pct = round(100.0 * dead / total, 1) if total else 0

    items: list[dict[str, Any]] = []
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

    weekly_dead = _fmt_delta(d_dead, unit=" users")
    summary_parts = []
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
        "items": items[:6],
        "focus_areas": focus or ["resurrection", "at_risk_wau"],
        "delta_period_used": period,
    }
