"""Corporate goals and launch context for dashboard progress and tooltips."""

from __future__ import annotations

from datetime import date

# Paid Plus subscribers (premium_users in monetization)
SUBSCRIBER_TARGET = 461

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
