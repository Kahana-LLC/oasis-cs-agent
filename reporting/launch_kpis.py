"""Product Hunt launch KPI catalog and usage-cost forecast."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from models.db import LLMUsage
from reporting.cost_model import total_api_cost_usd

FORECAST_DAYS = 7


def _fmt_pct(v: float | None) -> str:
    return "—" if v is None else f"{v}%"


def _fmt_num(v: float | int | None, suffix: str = "") -> str:
    return "—" if v is None else f"{v}{suffix}"


def compute_usage_cost_forecast(
    usage: list[LLMUsage],
    today: date,
    window_days: int = FORECAST_DAYS,
) -> dict[str, Any]:
    cutoff = today - timedelta(days=window_days - 1)
    recent = [u for u in usage if u.timestamp.date() >= cutoff]
    prompts = len(recent)
    cost = round(total_api_cost_usd(recent), 2)
    daily_prompts = prompts / window_days if window_days else 0
    daily_cost = cost / window_days if window_days else 0
    return {
        "window_days": window_days,
        "window_start": str(cutoff),
        "window_end": str(today),
        "prompts_last_7d": prompts,
        "estimated_cost_last_7d_usd": cost,
        "projected_monthly_prompts": round(daily_prompts * 30),
        "projected_monthly_cost_usd": round(daily_cost * 30, 2),
    }


def compute_launch_kpis(
    *,
    activation: dict[str, Any],
    engagement: dict[str, Any],
    retention: dict[str, Any],
    monetization: dict[str, Any],
    feedback: dict[str, Any],
    dau_model: dict[str, Any],
    usage: list[LLMUsage],
    today: date,
    total_users: int,
) -> dict[str, Any]:
    """Build launch KPI scorecard rows and forecast block."""
    act_rates = activation.get("activation_rate_pct") or {}
    ttf = activation.get("time_to_first_hours") or {}
    churn = retention.get("churn_pct") or {}
    overall = retention.get("overall_retention_pct") or {}
    wau_rows = retention.get("wau_by_week") or []
    latest_wau = wau_rows[-1]["wau"] if wau_rows else None
    wow = wau_rows[-1].get("wow_pct") if wau_rows else None
    conv_vel = monetization.get("conversion_velocity_hours") or {}
    cac = monetization.get("cac_ltv") or {}
    dau_totals = dau_model.get("totals") or {}

    usage_forecast = compute_usage_cost_forecast(usage, today)

    limit_hitter_conv = monetization.get("premium_conversion_among_limit_hitters_pct")

    def row(category: str, metric: str, value: str, status: str = "live") -> dict[str, str]:
        return {"category": category, "metric": metric, "value": value, "status": status}

    kpi_rows: list[dict[str, str]] = [
        # Activation
        row("Activation", "AI activation rate (1h)", _fmt_pct(act_rates.get("1h"))),
        row("Activation", "AI activation rate (24h)", _fmt_pct(act_rates.get("24h"))),
        row("Activation", "AI activation rate (3d)", _fmt_pct(act_rates.get("3d"))),
        row("Activation", "AI activation rate (7d)", _fmt_pct(act_rates.get("7d"))),
        row(
            "Activation",
            "Time to first AI command (median h)",
            _fmt_num(ttf.get("median"), " h"),
        ),
        row(
            "Activation",
            "Time to first AI command (mean h)",
            _fmt_num(ttf.get("mean"), " h"),
        ),
        # Engagement
        row(
            "Engagement",
            "Power users — 10+ prompts day 0",
            _fmt_pct(engagement.get("power_users_day0_pct")),
        ),
        row(
            "Engagement",
            "Power users — 10+ prompts week 0",
            _fmt_pct(engagement.get("power_users_week0_pct")),
        ),
        row(
            "Engagement",
            "Multi-day AI in first 7 days",
            _fmt_pct(engagement.get("multi_day_ai_first_7d_pct")),
        ),
        row(
            "Engagement",
            "Avg prompts / active day (latest cohort)",
            _fmt_num(
                (engagement.get("prompts_per_active_day_by_cohort") or [{}])[-1].get(
                    "avg_prompts_per_active_day"
                )
                if engagement.get("prompts_per_active_day_by_cohort")
                else None
            ),
        ),
        # Retention
        row("Retention", "D1 retention", _fmt_pct(overall.get("D1"))),
        row("Retention", "D3 retention", _fmt_pct(overall.get("D3"))),
        row("Retention", "D7 retention", _fmt_pct(overall.get("D7"))),
        row("Retention", "D14 retention", _fmt_pct(overall.get("D14"))),
        row("Retention", "D30 retention", _fmt_pct(overall.get("D30"))),
        row(
            "Retention",
            "Latest WAU",
            _fmt_num(latest_wau) + (f" ({wow}% WoW)" if wow is not None else ""),
        ),
        row("Retention", "Churn 7d (ever-active)", _fmt_pct(churn.get("churn_7d_pct"))),
        row("Retention", "Churn 14d (ever-active)", _fmt_pct(churn.get("churn_14d_pct"))),
        row("Retention", "Churn 30d (ever-active)", _fmt_pct(churn.get("churn_30d_pct"))),
        row(
            "Retention",
            "Sessions / active user (latest week)",
            _fmt_num(
                (retention.get("session_frequency_by_week") or [{}])[-1].get(
                    "sessions_per_active_user"
                )
                if retention.get("session_frequency_by_week")
                else None
            ),
        ),
        # Monetization
        row(
            "Monetization",
            "Token limit hit rate",
            _fmt_pct(monetization.get("token_limit_hit_rate_pct")),
        ),
        row(
            "Monetization",
            "Median days to first token limit",
            _fmt_num(monetization.get("median_days_to_first_limit"), " d"),
        ),
        row(
            "Monetization",
            "Median hours to first token limit",
            _fmt_num(monetization.get("median_hours_to_first_limit"), " h"),
        ),
        row(
            "Monetization",
            "Premium conversion (all users)",
            _fmt_pct(monetization.get("premium_conversion_pct")),
        ),
        row(
            "Monetization",
            "Premium conversion (limit hitters)",
            _fmt_pct(limit_hitter_conv),
        ),
        row(
            "Monetization",
            "Conversion velocity (median h to upgrade)",
            _fmt_num(conv_vel.get("median"), " h"),
        ),
        row(
            "Monetization",
            "ARPU gross",
            f"${monetization.get('arpu_gross_usd', '—')}",
        ),
        row(
            "Monetization",
            "ARPU net (est. API cost)",
            f"${monetization.get('arpu_net_usd', '—')}",
        ),
        row(
            "Monetization",
            "Est. API cost (all-time model)",
            f"${monetization.get('estimated_api_cost_usd', '—')}",
        ),
        row(
            "Monetization",
            "Projected monthly API cost (7d run-rate)",
            f"${usage_forecast.get('projected_monthly_cost_usd', '—')}",
        ),
        row(
            "Monetization",
            "LTV proxy (12 mo, net ARPU)",
            f"${monetization.get('ltv_proxy_usd', '—')}",
        ),
        row(
            "Monetization",
            "CAC / LTV ratio",
            "Unavailable — no acquisition spend in DB",
            "partial",
        ),
        row(
            "Monetization",
            "Actual Gemini spend (monthly)",
            "Enter in dashboard — AI Studio actuals",
            "manual",
        ),
        # Feedback
        row(
            "Feedback",
            "Feedback submission rate",
            _fmt_pct(feedback.get("submission_rate_pct")),
        ),
        row(
            "Feedback",
            "Median hours to first feedback",
            _fmt_num(feedback.get("median_hours_to_first"), " h"),
        ),
        row(
            "Feedback",
            "Anomalies (<15 min post-signup)",
            _fmt_num(len(feedback.get("anomalies") or [])),
        ),
        row(
            "Feedback",
            "Manual review samples",
            _fmt_num(len(feedback.get("review_samples") or [])),
        ),
        # DAU cross-link
        row("DAU", "DAU (today)", _fmt_num(dau_totals.get("dau"))),
        row("DAU", "WAU (model)", _fmt_num(dau_totals.get("wau"))),
        row("DAU", "MAU (model)", _fmt_num(dau_totals.get("mau"))),
    ]

    headlines = {
        "activation_24h_pct": act_rates.get("24h"),
        "retention_d7_pct": overall.get("D7"),
        "latest_wau": latest_wau,
        "premium_conversion_pct": monetization.get("premium_conversion_pct"),
        "feedback_submission_rate_pct": feedback.get("submission_rate_pct"),
        "arpu_net_usd": monetization.get("arpu_net_usd"),
    }

    return {
        "kpi_rows": kpi_rows,
        "headlines": headlines,
        "usage_cost_forecast": usage_forecast,
        "premium_conversion_among_limit_hitters_pct": limit_hitter_conv,
        "default_supabase_monthly_usd": 25,
    }


def attach_tooltips_to_kpi_rows(
    rows: list[dict[str, str]],
    tooltips: dict[str, str] | None = None,
) -> list[dict[str, str]]:
    """Add plain-English tooltip and metric_key for delta lookup."""
    from reporting.goal_aware_tooltips import tooltip_for_kpi_row_enriched
    from reporting.metric_glossary import kpi_metric_key, tooltip_for_kpi_row

    out: list[dict[str, str]] = []
    for row in rows:
        enriched = dict(row)
        cat = row.get("category", "")
        met = row.get("metric", "")
        key = kpi_metric_key(cat, met)
        if key:
            enriched["metric_key"] = key
        if tooltips:
            enriched["tooltip"] = tooltip_for_kpi_row_enriched(enriched, tooltips)
        else:
            enriched["tooltip"] = tooltip_for_kpi_row(cat, met)
        out.append(enriched)
    return out
