"""Corporate goal progress and trend phrases for tooltips."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from reporting.corporate_goals import (
    DAU_TARGET_MULTIPLE,
    DEFAULT_SUPABASE_MONTHLY_USD,
    GROSS_MARGIN_TARGET_PCT,
    PH_SIGNUP_RANGE,
    PRODUCT_HUNT_LAUNCH_DATE,
    SUBSCRIBER_TARGET,
    WAITLIST_COUNT,
)

# Metrics where an increase is bad for the business
HIGHER_IS_WORSE = frozenset(
    {
        "churn_7d_pct",
        "churn_14d_pct",
        "churn_30d_pct",
        "bucket_dead",
        "bucket_at_risk_wau",
        "bucket_at_risk_mau",
        "flow_1-NURR",
        "flow_1-CURR",
        "flow_WAU_Loss_Rate",
        "flow_MAU_Loss_Rate",
        "estimated_api_cost_usd",
    }
)


def compute_gross_margin_pct(
    revenue: float,
    api_cost: float,
    supabase_monthly: float = DEFAULT_SUPABASE_MONTHLY_USD,
) -> float | None:
    if revenue <= 0:
        return None
    return round(100.0 * (revenue - api_cost - supabase_monthly) / revenue, 1)


def trend_phrase(
    metric_key: str,
    deltas: dict[str, Any],
    period: str = "weekly",
) -> str:
    """Plain-English trend from delta block."""
    block = deltas.get(period) or {}
    if not block.get("available"):
        return "Not enough daily snapshot history yet to show a trend."

    d = (block.get("metrics") or {}).get(metric_key)
    if not d or d.get("abs_change") is None:
        return "No change recorded vs the comparison period."

    label = block.get("label", "vs prior period")
    ac = d["abs_change"]
    pc = d.get("pct_change")
    worse = metric_key in HIGHER_IS_WORSE
    direction = d.get("direction", "flat")

    if direction == "flat":
        return f"Flat {label}."

    is_rate = "_pct" in metric_key or metric_key.startswith("flow_")
    suffix = " pp" if is_rate else ""
    sign_word = "Up" if ac > 0 else "Down"
    val = f"{sign_word} {abs(ac)}{suffix}"
    if pc is not None and not metric_key.startswith("flow_"):
        val += f" ({abs(pc)}% relative)"

    if worse:
        if direction == "up":
            qual = " — unfavorable for growth goals."
        elif direction == "down":
            qual = " — favorable for growth goals."
        else:
            qual = ""
    else:
        if direction == "up":
            qual = " — favorable for growth goals."
        elif direction == "down":
            qual = " — may slow progress toward goals."
        else:
            qual = ""

    sig = " (significant shift)" if d.get("significant") else ""
    return f"{val} {label}{sig}{qual}"


def compute_goal_progress(
    snapshot: dict[str, Any],
    deltas: dict[str, Any],
    state: dict[str, Any],
    *,
    today: date | None = None,
) -> dict[str, Any]:
    """Build corporate_goals block for API/UI."""
    today = today or date.fromisoformat(snapshot["snapshot_date"])
    mon = snapshot.get("monetization") or {}
    dau_totals = (snapshot.get("dau_model") or {}).get("totals") or {}

    premium_users = mon.get("premium_users") or 0
    sub_pct = (
        round(100.0 * premium_users / SUBSCRIBER_TARGET, 1) if SUBSCRIBER_TARGET else 0
    )
    sub_gap = max(0, SUBSCRIBER_TARGET - premium_users)

    revenue = mon.get("total_revenue_usd") or 0
    api_cost = mon.get("estimated_api_cost_usd") or 0
    margin = mon.get("gross_margin_pct")
    if margin is None:
        margin = compute_gross_margin_pct(revenue, api_cost)
    margin_gap = (
        round(GROSS_MARGIN_TARGET_PCT - margin, 1) if margin is not None else None
    )

    current_dau = dau_totals.get("dau")
    baseline = state.get("dau_yoy_baseline")
    dau_multiple = None
    dau_status = "pending_baseline"
    if baseline and baseline > 0 and current_dau is not None:
        dau_multiple = round(float(current_dau) / float(baseline), 2)
        dau_status = "locked"
    elif today < PRODUCT_HUNT_LAUNCH_DATE:
        dau_status = "pre_launch"
    elif today < PRODUCT_HUNT_LAUNCH_DATE + timedelta(days=7):
        dau_status = "collecting_baseline"

    days_until = (PRODUCT_HUNT_LAUNCH_DATE - today).days
    post_launch = today >= PRODUCT_HUNT_LAUNCH_DATE

    return {
        "subscribers": {
            "current": premium_users,
            "target": SUBSCRIBER_TARGET,
            "pct_of_goal": sub_pct,
            "gap": sub_gap,
            "on_track": premium_users >= SUBSCRIBER_TARGET,
        },
        "gross_margin_pct": {
            "current": margin,
            "target": GROSS_MARGIN_TARGET_PCT,
            "gap_pp": margin_gap,
            "on_track": margin is not None and margin >= GROSS_MARGIN_TARGET_PCT,
        },
        "dau_multiple": {
            "current_dau": current_dau,
            "baseline": baseline,
            "multiple": dau_multiple,
            "target_multiple": DAU_TARGET_MULTIPLE,
            "on_track": dau_multiple is not None and dau_multiple >= DAU_TARGET_MULTIPLE,
            "status": dau_status,
        },
        "launch": {
            "date": str(PRODUCT_HUNT_LAUNCH_DATE),
            "days_until": days_until if not post_launch else 0,
            "days_since": (today - PRODUCT_HUNT_LAUNCH_DATE).days if post_launch else 0,
            "post_launch": post_launch,
            "waitlist": WAITLIST_COUNT,
            "ph_signup_range": list(PH_SIGNUP_RANGE),
        },
    }
