"""Compute KPI deltas vs prior daily snapshots."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

# Significance thresholds (tune as needed)
PP_THRESHOLD = 3.0  # percentage points for rate metrics
REL_PCT_THRESHOLD = 15.0  # relative % change
COUNT_ABS_THRESHOLD = 5
COUNT_REL_THRESHOLD = 10.0
FLOW_PP_THRESHOLD = 5.0

RATE_METRICS = frozenset(
    {
        "activation_24h_pct",
        "retention_d7_pct",
        "premium_conversion_pct",
        "feedback_submission_rate_pct",
        "churn_7d_pct",
        "churn_14d_pct",
        "churn_30d_pct",
        "token_limit_hit_rate_pct",
        "limit_hitter_conversion_pct",
    }
)
FLOW_PREFIX = "flow_"
BUCKET_PREFIX = "bucket_"


def _direction(abs_change: float | None) -> str:
    if abs_change is None or abs_change == 0:
        return "flat"
    return "up" if abs_change > 0 else "down"


def _is_significant(metric_key: str, current: float, prior: float, abs_change: float) -> bool:
    if metric_key in RATE_METRICS:
        rel = abs(abs_change / prior * 100) if prior else 0
        return abs(abs_change) >= PP_THRESHOLD or rel >= REL_PCT_THRESHOLD
    if metric_key.startswith(FLOW_PREFIX):
        return abs(abs_change) >= FLOW_PP_THRESHOLD
    if metric_key.startswith(BUCKET_PREFIX) or metric_key in (
        "dau",
        "wau",
        "mau",
        "latest_wau",
        "total_users",
        "active_users",
    ):
        rel = abs(abs_change / prior * 100) if prior else 0
        return abs(abs_change) >= COUNT_ABS_THRESHOLD or rel >= COUNT_REL_THRESHOLD
    if metric_key == "arpu_net_usd":
        rel = abs(abs_change / prior * 100) if prior else 0
        return abs(abs_change) >= 0.25 or rel >= REL_PCT_THRESHOLD
    return abs(abs_change) >= 1


def compute_deltas(
    current: dict[str, Any],
    prior: dict[str, Any] | None,
) -> dict[str, dict[str, Any]]:
    """Per-metric delta objects for all keys in current."""
    if not prior:
        return {}
    metrics_out: dict[str, dict[str, Any]] = {}
    for key, cur_val in current.items():
        if cur_val is None:
            continue
        prev_val = prior.get(key)
        if prev_val is None:
            continue
        try:
            cur_f = float(cur_val)
            prev_f = float(prev_val)
        except (TypeError, ValueError):
            continue
        abs_change = round(cur_f - prev_f, 2)
        pct_change = (
            round(100.0 * abs_change / prev_f, 1) if prev_f != 0 else None
        )
        metrics_out[key] = {
            "current": cur_f,
            "prior": prev_f,
            "abs_change": abs_change,
            "pct_change": pct_change,
            "direction": _direction(abs_change),
            "significant": _is_significant(key, cur_f, prev_f, abs_change),
        }
    return metrics_out


def build_period_delta(
    period: str,
    current: dict[str, Any],
    prior: dict[str, Any] | None,
    today: date,
    offset_days: int,
) -> dict[str, Any]:
    as_of = today - timedelta(days=offset_days)
    available = prior is not None
    return {
        "available": available,
        "as_of": str(as_of) if available else None,
        "label": f"vs {offset_days}d ago",
        "metrics": compute_deltas(current, prior) if available else {},
    }


def build_all_period_deltas(
    current: dict[str, Any],
    priors: dict[str, dict[str, Any] | None],
    today: date,
) -> dict[str, Any]:
    from reporting.snapshot_history import HISTORY_OFFSETS

    return {
        period: build_period_delta(
            period,
            current,
            priors.get(period),
            today,
            HISTORY_OFFSETS[period],
        )
        for period in ("daily", "weekly", "monthly")
    }
