"""Plain-English tooltips for dashboard metrics."""

from __future__ import annotations

from reporting.dau_model import BUCKET_DEFINITIONS, BUCKET_LABELS, FLOW_RATES

METRIC_TOOLTIPS: dict[str, str] = {
    "activation_24h": (
        "Share of all users who sent their first AI prompt within 24 hours of signing up. "
        "Higher means onboarding is working quickly."
    ),
    "retention_d7": (
        "Share of users who came back on day 7 after signup (session or AI usage). "
        "A leading indicator of whether new users stick."
    ),
    "latest_wau": (
        "Users active at least once in the last 7 days (sessions or AI prompts). "
        "Shows near-term engagement momentum."
    ),
    "premium_conversion": (
        "Share of all users on a paid Plus plan or active paid subscription. "
        "Overall monetization health."
    ),
    "feedback_rate": (
        "Share of users who submitted at least one feedback/training event. "
        "Signals product involvement beyond passive use."
    ),
    "arpu_net": (
        "Average revenue per user after subtracting estimated API costs. "
        "Net unit economics per user."
    ),
    "churn_7d": (
        "Among users who were ever active, the share with no return in the last 7 days. "
        "Lower is better — rising churn means more slipping away."
    ),
    "churn_14d": "Ever-active users with no activity in the last 14 days.",
    "churn_30d": "Ever-active users with no activity in the last 30 days.",
    "token_limit_hit_rate": (
        "Share of users who hit the daily AI token cap at least once. "
        "Often signals power users who may upgrade."
    ),
    "limit_hitter_conversion": (
        "Of users who hit token limits, how many are on a paid plan. "
        "Measures whether limits drive upgrades."
    ),
    "median_days_to_first_limit": (
        "Typical days from signup until a user first hits the token cap. "
        "Shorter often means heavy early usage."
    ),
    "median_hours_to_first_limit": "Same as days to first limit, in hours.",
    "conversion_velocity": (
        "Median hours from signup to first premium upgrade among paying users."
    ),
    "dau": "Users engaged today: new, current, reactivated, or resurrected.",
    "wau": "DAU plus users at-risk WAU (active recently but not today).",
    "mau": "WAU plus users at-risk MAU (active 7–29 days ago, inactive lately).",
    "time_to_first_prompt_median": (
        "Median hours from account creation to first AI prompt."
    ),
    "power_users_day0": "Users with 10+ AI prompts on their signup day.",
    "power_users_week0": "Users with 10+ AI prompts in their first 7 days.",
    "multi_day_ai_7d": (
        "Users who used AI on more than one day in their first week."
    ),
}

# DAU bucket tooltips from model definitions
for key, definition in BUCKET_DEFINITIONS.items():
    label = BUCKET_LABELS.get(key, key)
    METRIC_TOOLTIPS[f"bucket_{key}"] = f"{label}: {definition}"

# Flow rate tooltips
for rate_key, _src, _dst, label in FLOW_RATES:
    METRIC_TOOLTIPS[f"flow_{rate_key}"] = (
        f"{label} — average daily % of users making this transition over the last 7 days. "
        "Higher resurrection and iWAURR/iMAURR help win back at-risk and dead users."
    )

# KPI row lookup by category + metric label substring
_KPI_TOOLTIP_RULES: list[tuple[str, str, str]] = [
    ("Activation", "activation rate (1h)", "activation_24h"),
    ("Activation", "activation rate (24h)", "activation_24h"),
    ("Activation", "activation rate (3d)", "activation_24h"),
    ("Activation", "activation rate (7d)", "activation_24h"),
    ("Activation", "Time to first", "time_to_first_prompt_median"),
    ("Retention", "D7 retention", "retention_d7"),
    ("Retention", "D1 retention", "retention_d7"),
    ("Retention", "Churn 7d", "churn_7d"),
    ("Retention", "Churn 14d", "churn_14d"),
    ("Retention", "Churn 30d", "churn_30d"),
    ("Retention", "Weekly active", "latest_wau"),
    ("Monetization", "Token limit hit", "token_limit_hit_rate"),
    ("Monetization", "limit hitters", "limit_hitter_conversion"),
    ("Monetization", "Premium conversion (all", "premium_conversion"),
    ("Monetization", "Conversion velocity", "conversion_velocity"),
    ("Monetization", "ARPU net", "arpu_net"),
    ("Monetization", "days to first token", "median_days_to_first_limit"),
    ("Feedback", "submission rate", "feedback_rate"),
    ("DAU", "DAU", "dau"),
    ("DAU", "WAU", "wau"),
    ("DAU", "MAU", "mau"),
]


def kpi_metric_key(category: str, metric: str) -> str | None:
    """Map Launch KPI row to compact history metric key for deltas."""
    cat = category.strip()
    met = metric.strip().lower()
    for rule_cat, needle, tip_key in _KPI_TOOLTIP_RULES:
        if rule_cat == cat and needle.lower() in met:
            mapping = {
                "activation_24h": "activation_24h_pct",
                "retention_d7": "retention_d7_pct",
                "latest_wau": "latest_wau",
                "premium_conversion": "premium_conversion_pct",
                "feedback_rate": "feedback_submission_rate_pct",
                "arpu_net": "arpu_net_usd",
                "churn_7d": "churn_7d_pct",
                "churn_14d": "churn_14d_pct",
                "churn_30d": "churn_30d_pct",
                "token_limit_hit_rate": "token_limit_hit_rate_pct",
                "limit_hitter_conversion": "limit_hitter_conversion_pct",
                "median_days_to_first_limit": "median_days_to_first_limit",
                "dau": "dau",
                "wau": "wau",
                "mau": "mau",
            }
            return mapping.get(tip_key)
    if cat == "DAU" and "dead" in met:
        return "bucket_dead"
    for rate_key, _s, _d, label in FLOW_RATES:
        if rate_key in metric or label.lower() in met:
            return f"flow_{rate_key}"
    return None


def tooltip_for_kpi_row(category: str, metric: str) -> str:
    """Best-effort tooltip for a Launch KPI table row."""
    cat = category.strip()
    met = metric.strip().lower()
    for rule_cat, needle, tip_key in _KPI_TOOLTIP_RULES:
        if rule_cat == cat and needle.lower() in met:
            return METRIC_TOOLTIPS.get(tip_key, "")
    if cat == "DAU" and "dead" in met:
        return METRIC_TOOLTIPS.get("bucket_dead", "")
    if "→" in metric or "NURR" in metric:
        for rate_key, _s, _d, label in FLOW_RATES:
            if label.lower() in met.lower() or rate_key in metric:
                return METRIC_TOOLTIPS.get(f"flow_{rate_key}", "")
    return (
        f"{category} metric tracked for Product Hunt launch. "
        "See section charts below for trend detail."
    )
