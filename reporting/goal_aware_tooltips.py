"""Build 3-part tooltips: meaning, trend, and corporate goal context."""

from __future__ import annotations

from typing import Any

from reporting.corporate_goals import (
    DAU_TARGET_MULTIPLE,
    GROSS_MARGIN_TARGET_PCT,
    PH_SIGNUP_RANGE,
    SUBSCRIBER_TARGET,
    WAITLIST_COUNT,
)
from reporting.goal_progress import trend_phrase
from reporting.metric_glossary import METRIC_TOOLTIPS, kpi_metric_key, tooltip_for_kpi_row


def _section(title: str, body: str) -> str:
    if not body:
        return ""
    return f"{title}: {body}"


def _goal_subscribers(corp: dict[str, Any]) -> str:
    s = corp.get("subscribers") or {}
    cur = s.get("current", 0)
    tgt = s.get("target", SUBSCRIBER_TARGET)
    gap = s.get("gap", 0)
    pct = s.get("pct_of_goal", 0)
    return (
        f"Goal: {tgt} paid subscribers. You have {cur} ({pct}% of goal). "
        f"Gap: {gap} subscribers to reach target."
    )


def _goal_margin(corp: dict[str, Any]) -> str:
    m = corp.get("gross_margin_pct") or {}
    cur = m.get("current")
    tgt = m.get("target", GROSS_MARGIN_TARGET_PCT)
    if cur is None:
        return f"Goal: {tgt}% gross margin (revenue minus API and Supabase costs). No revenue yet to compute margin."
    gap = m.get("gap_pp")
    on = "on track" if m.get("on_track") else "below target"
    return f"Goal: {tgt}% gross margin. Current: {cur}% ({on}). Gap: {gap} pp to target."


def _goal_dau(corp: dict[str, Any]) -> str:
    d = corp.get("dau_multiple") or {}
    status = d.get("status", "pending_baseline")
    tgt = d.get("target_multiple", DAU_TARGET_MULTIPLE)
    if status == "pending_baseline" or status == "collecting_baseline":
        return (
            f"Goal: {tgt}× DAU vs your Product Hunt launch-week average. "
            "Baseline locks automatically after the first 7 days post-launch."
        )
    if status == "pre_launch":
        return (
            f"Goal: {tgt}× DAU vs launch-week baseline (set after PH launch). "
            "Focus on activation before May 27 influx."
        )
    mult = d.get("multiple")
    base = d.get("baseline")
    cur = d.get("current_dau")
    if mult is not None:
        on = "on track" if d.get("on_track") else "below target"
        return (
            f"Goal: {tgt}× DAU vs launch week (baseline {base}). "
            f"Current: {cur} DAU ({mult}×, {on})."
        )
    return f"Goal: {tgt}× DAU growth vs launch-week baseline."


def _goal_launch_context(corp: dict[str, Any]) -> str:
    launch = corp.get("launch") or {}
    lo, hi = PH_SIGNUP_RANGE
    days = launch.get("days_until", 0)
    if not launch.get("post_launch"):
        return (
            f"Context: {WAITLIST_COUNT} on waitlist. Product Hunt launch may add "
            f"{lo}–{hi} signups in ~{days} days — activation and conversion drive the "
            f"{SUBSCRIBER_TARGET} subscriber goal."
        )
    return (
        f"Context: Post–Product Hunt launch; expect {lo}–{hi} new users alongside "
        f"{WAITLIST_COUNT} waitlist. Scale DAU and conversion to hit {SUBSCRIBER_TARGET} subscribers."
    )


def _goals_for_metric(metric_key: str, corp: dict[str, Any]) -> str:
    if metric_key in (
        "premium_conversion_pct",
        "limit_hitter_conversion_pct",
        "premium_users",
    ):
        return _goal_subscribers(corp)
    if metric_key in (
        "arpu_net_usd",
        "arpu_gross_usd",
        "gross_margin_pct",
        "estimated_api_cost_usd",
        "token_limit_hit_rate_pct",
    ):
        return _goal_margin(corp) + " " + _goal_subscribers(corp)
    if metric_key.startswith("bucket_") or metric_key.startswith("flow_"):
        return _goal_dau(corp) + " Reducing dead/at-risk users supports DAU and subscriber goals."
    if metric_key in ("dau", "wau", "mau", "latest_wau"):
        return _goal_dau(corp)
    if metric_key in ("activation_24h_pct", "retention_d7_pct"):
        return _goal_launch_context(corp) + " " + _goal_subscribers(corp)
    if metric_key.startswith("churn_"):
        return _goal_dau(corp) + " Lower churn protects DAU and path to " + str(SUBSCRIBER_TARGET) + " subscribers."
    return _goal_launch_context(corp)


_TOOLTIP_ALIASES: dict[str, str] = {
    "premium_conversion_pct": "premium_conversion",
    "activation_24h_pct": "activation_24h",
    "retention_d7_pct": "retention_d7",
    "feedback_submission_rate_pct": "feedback_rate",
    "limit_hitter_conversion_pct": "limit_hitter_conversion",
    "token_limit_hit_rate_pct": "token_limit_hit_rate",
    "churn_7d_pct": "churn_7d",
    "churn_14d_pct": "churn_14d",
    "churn_30d_pct": "churn_30d",
}


def build_tooltip(
    metric_key: str,
    snapshot: dict[str, Any],
    deltas: dict[str, Any],
    corporate_goals: dict[str, Any],
    period: str = "weekly",
) -> str:
    meaning = METRIC_TOOLTIPS.get(metric_key) or METRIC_TOOLTIPS.get(
        _TOOLTIP_ALIASES.get(metric_key, ""), ""
    )
    trend = trend_phrase(metric_key, deltas, period)
    goals = _goals_for_metric(metric_key, corporate_goals)
    parts = [
        _section("What it means", meaning),
        _section("Trend", trend),
        _section("Goals", goals),
    ]
    return "\n\n".join(p for p in parts if p)


def build_all_tooltips(
    snapshot: dict[str, Any],
    deltas: dict[str, Any],
    corporate_goals: dict[str, Any],
    period: str = "weekly",
) -> dict[str, str]:
    """Full tooltip map for all glossary keys plus monetization gross_margin."""
    keys = set(METRIC_TOOLTIPS.keys()) | {
        "premium_users",
        "gross_margin_pct",
        "total_users",
        "activation_24h_pct",
        "retention_d7_pct",
        "premium_conversion_pct",
        "limit_hitter_conversion_pct",
        "token_limit_hit_rate_pct",
        "churn_7d_pct",
        "churn_14d_pct",
        "churn_30d_pct",
        "latest_wau",
        "feedback_submission_rate_pct",
    }
    return {
        k: build_tooltip(k, snapshot, deltas, corporate_goals, period)
        for k in keys
    }


def tooltip_for_kpi_row_enriched(
    row: dict[str, str],
    tooltips: dict[str, str],
) -> str:
    key = row.get("metric_key") or kpi_metric_key(
        row.get("category", ""), row.get("metric", "")
    )
    if key and key in tooltips:
        return tooltips[key]
    return tooltip_for_kpi_row(row.get("category", ""), row.get("metric", ""))
