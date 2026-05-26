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
        fetch_cs_outreach_log,
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

    outreach_log: list[dict] = []
    outreach_log_available = False
    try:
        outreach_log = fetch_cs_outreach_log()
        outreach_log_available = True
    except Exception as exc:
        log.warning("cs_outreach_log fetch skipped: %s", exc)

    log.info(
        "counts: users=%d sessions=%d usage=%d daily=%d feedback=%d payments=%d outreach=%d",
        len(users),
        len(sessions),
        len(usage),
        len(daily),
        len(feedback),
        len(payments),
        len(outreach_log),
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
        outreach_log=outreach_log,
        outreach_log_available=outreach_log_available,
        today=today,
    )


def build_snapshot_dict(
    today: date | None = None,
    *,
    persist_history: bool = True,
) -> dict[str, Any]:
    """Return baseline snapshot as JSON-serializable dict with deltas and insights."""
    data = build_snapshot(today=today).to_dict()
    try:
        from reporting.snapshot_history import enrich_snapshot_with_history

        enrich_snapshot_with_history(data, persist=persist_history)
    except Exception as exc:
        log.warning("snapshot history enrichment skipped: %s", exc)
        data.setdefault("deltas", {})
        data.setdefault(
            "key_insights",
            {"summary": "", "items": [], "focus_areas": []},
        )
        data.setdefault("metric_tooltips", {})
        data.setdefault("corporate_goals", {})
        data.setdefault(
            "email_provider_capacity",
            {"providers": [], "any_near_limit": False},
        )
    return data
