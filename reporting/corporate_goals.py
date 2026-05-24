"""Corporate goals and launch context for dashboard progress and tooltips."""

from __future__ import annotations

import calendar
from datetime import date

# Paid subscribers ($20/mo via Stripe user_plans)
PAID_SUBSCRIBER_BASELINE_COUNT = 1
PAID_SUBSCRIBER_TRACKING_START = date(2026, 5, 24)
SUBSCRIBER_TARGET_YEAR_END = 500
SUBSCRIBER_YEAR_END_DATE = date(2026, 12, 31)
SUBSCRIBER_GOAL_START_DATE = date(2026, 5, 24)

# Legacy alias for imports that used SUBSCRIBER_TARGET
SUBSCRIBER_TARGET = SUBSCRIBER_TARGET_YEAR_END

# Gross margin = (revenue - API cost - Supabase) / revenue
GROSS_MARGIN_TARGET_PCT = 80.0
DEFAULT_SUPABASE_MONTHLY_USD = 25.0

# DAU multiple vs average DAU during first 7 days post–Product Hunt
DAU_TARGET_MULTIPLE = 4.5
DAU_BASELINE_WINDOW_DAYS = 7

# Launch context
WAITLIST_COUNT = 176
PRODUCT_HUNT_LAUNCH_DATE = date(2026, 5, 27)
PH_SIGNUP_RANGE = (200, 2000)

_TOTAL_GOAL_DAYS = (SUBSCRIBER_YEAR_END_DATE - SUBSCRIBER_GOAL_START_DATE).days


def _days_to_month_end(year: int, month: int) -> int:
    """Days from SUBSCRIBER_GOAL_START_DATE to end of given month (inclusive)."""
    last_day = calendar.monthrange(year, month)[1]
    eom = date(year, month, last_day)
    if eom < SUBSCRIBER_GOAL_START_DATE:
        return 0
    return (eom - SUBSCRIBER_GOAL_START_DATE).days


def _cumulative_target_at_days(days: int) -> int:
    if _TOTAL_GOAL_DAYS <= 0:
        return SUBSCRIBER_TARGET_YEAR_END
    if days <= 0:
        return PAID_SUBSCRIBER_BASELINE_COUNT
    if days >= _TOTAL_GOAL_DAYS:
        return SUBSCRIBER_TARGET_YEAR_END
    span = SUBSCRIBER_TARGET_YEAR_END - PAID_SUBSCRIBER_BASELINE_COUNT
    return round(PAID_SUBSCRIBER_BASELINE_COUNT + span * days / _TOTAL_GOAL_DAYS)


def subscriber_monthly_targets() -> list[dict[str, int | str]]:
    """End-of-month cumulative subscriber targets May–Dec 2026."""
    rows: list[dict[str, int | str]] = []
    for month in range(SUBSCRIBER_GOAL_START_DATE.month, 13):
        days = _days_to_month_end(2026, month)
        label = date(2026, month, 1).strftime("%B %Y")
        rows.append(
            {
                "month": f"2026-{month:02d}",
                "label": label,
                "cumulative_target": _cumulative_target_at_days(days),
            }
        )
    return rows


MONTHLY_SUBSCRIBER_TARGETS = subscriber_monthly_targets()


def month_target_for_date(today: date) -> dict[str, int | float | str | bool | None]:
    """Current month cumulative target and prorated on-track threshold."""
    month_key = today.strftime("%Y-%m")
    month_row = next(
        (r for r in MONTHLY_SUBSCRIBER_TARGETS if r["month"] == month_key),
        MONTHLY_SUBSCRIBER_TARGETS[-1] if MONTHLY_SUBSCRIBER_TARGETS else None,
    )
    if not month_row:
        return {
            "month": month_key,
            "label": today.strftime("%B %Y"),
            "cumulative_target": SUBSCRIBER_TARGET_YEAR_END,
            "prorated_target": SUBSCRIBER_TARGET_YEAR_END,
            "on_track": False,
        }

    cumulative = int(month_row["cumulative_target"])
    year, month = today.year, today.month
    first_of_month = date(year, month, 1)
    if month_key == SUBSCRIBER_GOAL_START_DATE.strftime("%Y-%m"):
        period_start = SUBSCRIBER_GOAL_START_DATE
    else:
        period_start = first_of_month

    days_in_period = (date(year, month, calendar.monthrange(year, month)[1]) - period_start).days + 1
    days_elapsed = (today - period_start).days + 1
    days_elapsed = max(0, min(days_elapsed, days_in_period))

    prev_month = month - 1
    if month_key == SUBSCRIBER_GOAL_START_DATE.strftime("%Y-%m"):
        start_target = PAID_SUBSCRIBER_BASELINE_COUNT
    elif prev_month >= SUBSCRIBER_GOAL_START_DATE.month:
        prev_days = _days_to_month_end(2026, prev_month)
        start_target = _cumulative_target_at_days(prev_days)
    else:
        start_target = PAID_SUBSCRIBER_BASELINE_COUNT

    if days_in_period <= 0:
        prorated = cumulative
    else:
        prorated = round(start_target + (cumulative - start_target) * days_elapsed / days_in_period)

    return {
        "month": month_key,
        "label": str(month_row["label"]),
        "cumulative_target": cumulative,
        "prorated_target": prorated,
        "days_elapsed_in_month": days_elapsed,
        "days_in_month_period": days_in_period,
    }


def year_end_prorated_target(today: date) -> int:
    """Cumulative subscriber target prorated from May 24 through today."""
    if today <= SUBSCRIBER_GOAL_START_DATE:
        return PAID_SUBSCRIBER_BASELINE_COUNT
    days = (today - SUBSCRIBER_GOAL_START_DATE).days
    return _cumulative_target_at_days(days)
