"""Fetch Supabase data and compute baseline snapshot (shared by CLI and Vercel API)."""

from __future__ import annotations

import logging
from datetime import date
from typing import Any

from reporting.baseline_metrics import BaselineSnapshot, compute_baseline_snapshot

log = logging.getLogger(__name__)


def build_snapshot(today: date | None = None) -> BaselineSnapshot:
    """Pull all baseline inputs from Supabase and return the snapshot."""
    from db.fetch import (
        fetch_all_users,
        fetch_daily_usage,
        fetch_feedback,
        fetch_payments,
        fetch_plan_overrides,
        fetch_plans,
        fetch_sessions,
        fetch_usage,
        fetch_user_plans,
    )

    if today is None:
        today = date.today()

    log.info("fetching data...")
    users = fetch_all_users()
    sessions = fetch_sessions()
    usage = fetch_usage()
    daily = fetch_daily_usage()
    feedback = fetch_feedback()
    plans = fetch_plans()
    overrides = fetch_plan_overrides()
    payments = fetch_payments()
    user_plans = fetch_user_plans()

    log.info(
        "counts: users=%d sessions=%d usage=%d daily=%d feedback=%d payments=%d",
        len(users),
        len(sessions),
        len(usage),
        len(daily),
        len(feedback),
        len(payments),
    )

    return compute_baseline_snapshot(
        users=users,
        sessions=sessions,
        usage=usage,
        daily=daily,
        feedback=feedback,
        plans=plans,
        overrides=overrides,
        payments=payments,
        user_plans=user_plans,
        today=today,
    )


def build_snapshot_dict(today: date | None = None) -> dict[str, Any]:
    """Return baseline snapshot as JSON-serializable dict."""
    return build_snapshot(today=today).to_dict()
