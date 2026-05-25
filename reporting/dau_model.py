"""Daily Active Users model — bucket sizes and flow rates (diagram definitions)."""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import date, timedelta
from typing import Any

import pandas as pd

FLOW_WINDOW_DAYS = 7

BUCKET_KEYS = (
    "new",
    "current",
    "reactivated",
    "resurrected",
    "at_risk_wau",
    "at_risk_mau",
    "dead",
)

BUCKET_LABELS: dict[str, str] = {
    "new": "New users",
    "current": "Current users",
    "reactivated": "Reactivated users",
    "resurrected": "Resurrected users",
    "at_risk_wau": "At-risk WAU",
    "at_risk_mau": "At-risk MAU",
    "dead": "Dead users",
}

BUCKET_DEFINITIONS: dict[str, str] = {
    "new": "First day of engagement ever",
    "current": "Active today and at least one other day in the prior 7 days",
    "reactivated": "First day back after 7–29 days away",
    "resurrected": "First day back after 30+ days away",
    "at_risk_wau": "Inactive today, active on at least one of the prior 6 days",
    "at_risk_mau": "Inactive today and prior 6 days, active 7–29 days ago",
    "dead": "No activity in the last 30 days",
}

FLOW_RATES: list[tuple[str, str, str, str]] = [
    ("NURR", "new", "current", "New → Current"),
    ("1-NURR", "new", "at_risk_wau", "New → At-risk WAU"),
    ("CURR", "current", "current", "Current → Current"),
    ("1-CURR", "current", "at_risk_wau", "Current → At-risk WAU"),
    ("RURR", "reactivated", "current", "Reactivated → Current"),
    ("1-RURR", "reactivated", "at_risk_wau", "Reactivated → At-risk WAU"),
    ("SURR", "resurrected", "current", "Resurrected → Current"),
    ("1-SURR", "resurrected", "at_risk_wau", "Resurrected → At-risk WAU"),
    ("iWAURR", "at_risk_wau", "current", "At-risk WAU → Current"),
    ("WAU_Loss_Rate", "at_risk_wau", "at_risk_mau", "At-risk WAU → At-risk MAU"),
    ("iMAURR", "at_risk_mau", "reactivated", "At-risk MAU → Reactivated"),
    ("MAU_Loss_Rate", "at_risk_mau", "dead", "At-risk MAU → Dead"),
    ("Resurrection_Rate", "dead", "resurrected", "Dead → Resurrected"),
]


def classify_user_bucket(activity_dates: set[date], as_of: date) -> str:
    """Classify one user into exactly one bucket on as_of (diagram rules)."""
    active_today = as_of in activity_dates

    if active_today:
        if not activity_dates:
            return "dead"
        first_ever = min(activity_dates)
        if as_of == first_ever:
            return "new"

        prev_dates = [d for d in activity_dates if d < as_of]
        if not prev_dates:
            return "new"

        last_prev = max(prev_dates)
        gap = (as_of - last_prev).days

        if gap >= 30:
            return "resurrected"
        if 7 <= gap <= 29:
            return "reactivated"

        prior_7 = {as_of - timedelta(days=i) for i in range(1, 8)}
        if prior_7 & activity_dates:
            return "current"

        # Active today after a short gap; prior activity falls within the WAU window.
        return "current"

    prior_6 = {as_of - timedelta(days=i) for i in range(1, 7)}
    if prior_6 & activity_dates:
        return "at_risk_wau"

    days_7_29 = {as_of - timedelta(days=i) for i in range(7, 30)}
    if days_7_29 & activity_dates:
        return "at_risk_mau"

    return "dead"


def _activity_by_user(activity_df: pd.DataFrame) -> dict[str, set[date]]:
    by_user: dict[str, set[date]] = defaultdict(set)
    if activity_df.empty:
        return by_user
    for row in activity_df.itertuples(index=False):
        d = row.activity_date
        if isinstance(d, pd.Timestamp):
            d = d.date()
        by_user[str(row.user_id)].add(d)
    return by_user


def _classify_all(
    user_ids: list[str], activity_by_user: dict[str, set[date]], as_of: date
) -> dict[str, str]:
    return {
        uid: classify_user_bucket(activity_by_user.get(uid, set()), as_of)
        for uid in user_ids
    }


def classify_users_as_of(
    user_ids: list[str], activity_by_user: dict[str, set[date]], as_of: date
) -> dict[str, str]:
    """Public alias for per-user DAU bucket assignment on as_of."""
    return _classify_all(user_ids, activity_by_user, as_of)


def activity_by_user_from_df(activity_df: pd.DataFrame) -> dict[str, set[date]]:
    """Build user_id → activity date set from sessions ∪ llm_usage activity frame."""
    return _activity_by_user(activity_df)


def _compute_flow_rates(
    user_ids: list[str],
    activity_by_user: dict[str, set[date]],
    as_of: date,
    window_days: int,
) -> dict[str, float | None]:
    """Average daily transition rates over the last window_days days."""
    daily_rates: dict[str, list[float]] = defaultdict(list)

    for offset in range(window_days):
        curr_day = as_of - timedelta(days=offset)
        prev_day = curr_day - timedelta(days=1)
        prev_buckets = _classify_all(user_ids, activity_by_user, prev_day)
        curr_buckets = _classify_all(user_ids, activity_by_user, curr_day)

        source_counts: Counter[str] = Counter()
        transition_counts: Counter[tuple[str, str]] = Counter()
        for uid in user_ids:
            src = prev_buckets[uid]
            dst = curr_buckets[uid]
            source_counts[src] += 1
            transition_counts[(src, dst)] += 1

        for rate_key, src, dst, _label in FLOW_RATES:
            denom = source_counts[src]
            if denom == 0:
                continue
            daily_rates[rate_key].append(100.0 * transition_counts[(src, dst)] / denom)

    result: dict[str, float | None] = {}
    for rate_key, _src, _dst, _label in FLOW_RATES:
        vals = daily_rates.get(rate_key, [])
        result[rate_key] = round(sum(vals) / len(vals), 1) if vals else None
    return result


def compute_dau_model(
    users_df: pd.DataFrame,
    activity_df: pd.DataFrame,
    as_of: date | None = None,
    flow_window_days: int = FLOW_WINDOW_DAYS,
) -> dict[str, Any]:
    """Compute bucket counts and flow rates for the DAU model."""
    as_of = as_of or date.today()
    user_ids = users_df["user_id"].astype(str).tolist() if not users_df.empty else []
    activity_by_user = _activity_by_user(activity_df)

    buckets = _classify_all(user_ids, activity_by_user, as_of)
    counts = Counter(buckets.values())
    bucket_counts = {k: int(counts.get(k, 0)) for k in BUCKET_KEYS}

    dau = (
        bucket_counts["new"]
        + bucket_counts["current"]
        + bucket_counts["reactivated"]
        + bucket_counts["resurrected"]
    )
    wau = dau + bucket_counts["at_risk_wau"]
    mau = wau + bucket_counts["at_risk_mau"]
    total = len(user_ids)

    flow_rates_pct = _compute_flow_rates(
        user_ids, activity_by_user, as_of, flow_window_days
    )

    flow_rate_rows = [
        {
            "rate": rate_key,
            "transition": label,
            "pct": flow_rates_pct.get(rate_key),
        }
        for rate_key, _src, _dst, label in FLOW_RATES
    ]

    bucket_rows = [
        {
            "bucket": BUCKET_LABELS[k],
            "key": k,
            "users": bucket_counts[k],
            "pct_of_total": round(100.0 * bucket_counts[k] / total, 1) if total else 0.0,
        }
        for k in BUCKET_KEYS
    ]

    return {
        "as_of": str(as_of),
        "bucket_counts": bucket_counts,
        "bucket_rows": bucket_rows,
        "totals": {
            "dau": dau,
            "wau": wau,
            "mau": mau,
            "total_users": total,
        },
        "flow_rates_pct": flow_rates_pct,
        "flow_rate_rows": flow_rate_rows,
        "flow_window_days": flow_window_days,
        "definitions": BUCKET_DEFINITIONS,
    }
