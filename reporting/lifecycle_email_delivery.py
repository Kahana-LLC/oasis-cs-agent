"""Phase 1 lifecycle email delivery: eligible vs sent vs missed (PH monitoring)."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import pandas as pd

from reporting.lifecycle_email_sends import (
    _cohort_user_ids,
    _parse_sent_at,
    _pct,
    _users_with_email_triggers,
    load_new_user_window_days,
    load_phase1_triggers,
)

MANIFEST_PATH = Path(__file__).resolve().parents[1] / "public" / "email_sequences.json"
RPC_LIMIT = 500

TRIGGER_RPC: dict[str, str] = {
    "activation_nudge_24h": "lifecycle_cohort_activation_nudge_24h",
    "activation_cs_calendar": "lifecycle_cohort_activation_cs_calendar",
    "nps_day3": "lifecycle_cohort_nps_day3",
    "pmf_day10": "lifecycle_cohort_pmf_day10",
}


def load_lifecycle_reporting_config() -> dict[str, Any]:
    if not MANIFEST_PATH.exists():
        return {}
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return (data.get("launch_config") or {}).get("lifecycle_reporting") or {}


def _active_with_email_mask(users_df: pd.DataFrame) -> pd.Series:
    if users_df.empty:
        return pd.Series(dtype=bool)
    email_ok = users_df["email"].fillna("").astype(str).str.strip() != ""
    return (users_df["status"] == "active") & email_ok


def _signup_age_days(users_df: pd.DataFrame, today: date) -> pd.Series:
    created = pd.to_datetime(users_df["created_at"]).dt.tz_localize(None)
    return (pd.Timestamp(today) - created).dt.days


def _missed_welcome(
    users_df: pd.DataFrame,
    sent_by_trigger: dict[str, set[str]],
    *,
    today: date,
    miss_hours: int,
    window_days: int,
) -> int:
    if users_df.empty:
        return 0
    cutoff = today - timedelta(days=window_days)
    miss_before = datetime.combine(today, datetime.min.time()) - timedelta(hours=miss_hours)
    created = pd.to_datetime(users_df["created_at"]).dt.tz_localize(None)
    sent = sent_by_trigger.get("welcome_email", set())
    mask = (
        _active_with_email_mask(users_df)
        & (created.dt.date >= cutoff)
        & (created < miss_before)
        & (~users_df["user_id"].astype(str).isin(sent))
    )
    return int(mask.sum())


def _missed_nudge(
    users_df: pd.DataFrame,
    usage_user_ids: set[str],
    sent_by_trigger: dict[str, set[str]],
    *,
    today: date,
    window_days: int,
    overdue_after_hours: int = 48,
) -> int:
    if users_df.empty:
        return 0
    cutoff = today - timedelta(days=window_days)
    overdue_before = datetime.combine(today, datetime.min.time()) - timedelta(
        hours=overdue_after_hours
    )
    created = pd.to_datetime(users_df["created_at"]).dt.tz_localize(None)
    sent = sent_by_trigger.get("activation_nudge_24h", set())
    mask = (
        _active_with_email_mask(users_df)
        & (created.dt.date >= cutoff)
        & (created < overdue_before)
        & (~users_df["user_id"].astype(str).isin(usage_user_ids))
        & (~users_df["user_id"].astype(str).isin(sent))
    )
    return int(mask.sum())


def _missed_cs_calendar(
    users_df: pd.DataFrame,
    usage_user_ids: set[str],
    training_user_ids: set[str],
    sent_by_trigger: dict[str, set[str]],
    *,
    today: date,
    window_days: int,
    overdue_after_days: int = 6,
) -> int:
    if users_df.empty:
        return 0
    cutoff = today - timedelta(days=window_days)
    overdue_before = datetime.combine(today, datetime.min.time()) - timedelta(
        days=overdue_after_days
    )
    created = pd.to_datetime(users_df["created_at"]).dt.tz_localize(None)
    sent = sent_by_trigger.get("activation_cs_calendar", set())
    mask = (
        _active_with_email_mask(users_df)
        & (created.dt.date >= cutoff)
        & (created < overdue_before)
        & (~users_df["user_id"].astype(str).isin(usage_user_ids))
        & (~users_df["user_id"].astype(str).isin(training_user_ids))
        & (~users_df["user_id"].astype(str).isin(sent))
    )
    return int(mask.sum())


def _missed_past_window(
    users_df: pd.DataFrame,
    sent_by_trigger: dict[str, set[str]],
    trigger_name: str,
    *,
    today: date,
    window_days: int,
    overdue_after_days: int,
) -> int:
    """NPS / PMF: active signup in window, past send window, no log row."""
    if users_df.empty:
        return 0
    cutoff = today - timedelta(days=window_days)
    overdue_before = datetime.combine(today, datetime.min.time()) - timedelta(
        days=overdue_after_days
    )
    created = pd.to_datetime(users_df["created_at"]).dt.tz_localize(None)
    sent = sent_by_trigger.get(trigger_name, set())
    mask = (
        _active_with_email_mask(users_df)
        & (created.dt.date >= cutoff)
        & (created < overdue_before)
        & (~users_df["user_id"].astype(str).isin(sent))
    )
    return int(mask.sum())


def _fetch_eligible_now(
    rpc_fetcher: Any | None,
) -> dict[str, dict[str, Any]]:
    """rpc_fetcher: callable(rpc_name) -> list[dict] or None if unavailable."""
    out: dict[str, dict[str, Any]] = {}
    if rpc_fetcher is None:
        return out
    for trigger, rpc_name in TRIGGER_RPC.items():
        try:
            rows = rpc_fetcher(rpc_name)
            count = len(rows)
            out[trigger] = {
                "eligible_now": count,
                "eligible_now_capped": count >= RPC_LIMIT,
            }
        except Exception as exc:
            out[trigger] = {
                "eligible_now": None,
                "eligible_now_capped": False,
                "rpc_error": str(exc),
            }
    return out


def _send_stats_by_trigger(
    outreach_log: list[dict[str, Any]],
    cohort_set: set[str],
) -> dict[str, dict[str, Any]]:
    by_trigger = _users_with_email_triggers(outreach_log)
    last_sent: dict[str, datetime | None] = {}
    sent_24h: Counter[str] = defaultdict(int)
    sent_7d: Counter[str] = defaultdict(int)
    now = datetime.utcnow()
    cut_24h = now - timedelta(hours=24)
    cut_7d = now - timedelta(days=7)

    for row in outreach_log:
        trigger = str(row.get("trigger_name") or "")
        if not trigger:
            continue
        sent_at = _parse_sent_at(row.get("sent_at"))
        if sent_at is not None:
            if trigger not in last_sent or sent_at > (last_sent[trigger] or sent_at):
                last_sent[trigger] = sent_at
            if sent_at >= cut_24h:
                sent_24h[trigger] += 1
            if sent_at >= cut_7d:
                sent_7d[trigger] += 1

    stats: dict[str, dict[str, Any]] = {}
    for trigger, uids in by_trigger.items():
        in_cohort = uids & cohort_set
        stats[trigger] = {
            "sent_all_time": len(uids),
            "sent_in_window": len(in_cohort),
            "sent_last_24h": sent_24h.get(trigger, 0),
            "sent_last_7d": sent_7d.get(trigger, 0),
            "last_sent_at": last_sent.get(trigger).isoformat() if last_sent.get(trigger) else None,
        }
    return stats


def compute_lifecycle_email_delivery(
    *,
    users_df: pd.DataFrame,
    usage_df: pd.DataFrame,
    feedback_user_ids: set[str],
    outreach_log: list[dict[str, Any]] | None = None,
    outreach_log_available: bool = False,
    rpc_fetcher: Any | None = None,
    today: date | None = None,
    window_days: int | None = None,
) -> dict[str, Any]:
    """Eligible vs sent vs missed-overdue per Phase 1 trigger."""
    today = today or date.today()
    outreach_log = outreach_log or []
    cfg = load_lifecycle_reporting_config()
    window_days = window_days if window_days is not None else load_new_user_window_days()
    welcome_miss_hours = int(cfg.get("welcome_miss_hours") or 2)

    cohort_ids = _cohort_user_ids(users_df, today=today, window_days=window_days)
    cohort_set = set(cohort_ids)

    usage_user_ids: set[str] = set()
    if not usage_df.empty:
        usage_user_ids = set(usage_df["user_id"].astype(str).tolist())

    sent_by_trigger = _users_with_email_triggers(outreach_log)
    send_stats = _send_stats_by_trigger(outreach_log, cohort_set)
    eligible_now_map = _fetch_eligible_now(rpc_fetcher)

    missed_map = {
        "welcome_email": _missed_welcome(
            users_df,
            sent_by_trigger,
            today=today,
            miss_hours=welcome_miss_hours,
            window_days=window_days,
        ),
        "activation_nudge_24h": _missed_nudge(
            users_df,
            usage_user_ids,
            sent_by_trigger,
            today=today,
            window_days=window_days,
        ),
        "activation_cs_calendar": _missed_cs_calendar(
            users_df,
            usage_user_ids,
            feedback_user_ids,
            sent_by_trigger,
            today=today,
            window_days=window_days,
        ),
        "nps_day3": _missed_past_window(
            users_df,
            sent_by_trigger,
            "nps_day3",
            today=today,
            window_days=window_days,
            overdue_after_days=6,
        ),
        "pmf_day10": _missed_past_window(
            users_df,
            sent_by_trigger,
            "pmf_day10",
            today=today,
            window_days=window_days,
            overdue_after_days=13,
        ),
    }

    triggers_out: list[dict[str, Any]] = []
    any_capped = False
    for t in load_phase1_triggers():
        name = str(t.get("dedup_trigger_name") or "")
        ss = send_stats.get(name, {})
        en = eligible_now_map.get(name, {})
        if en.get("eligible_now_capped"):
            any_capped = True
        missed = missed_map.get(name, 0)
        sent_win = ss.get("sent_in_window", 0)
        denom = sent_win + missed
        triggers_out.append(
            {
                "dedup_trigger_name": name,
                "sequence_id": t.get("sequence_id"),
                "label": t.get("brevo_template") or name,
                "channel": t.get("channel"),
                "when": t.get("when"),
                "eligible_now": en.get("eligible_now"),
                "eligible_now_capped": en.get("eligible_now_capped", False),
                "rpc_error": en.get("rpc_error"),
                "sent_all_time": ss.get("sent_all_time", 0),
                "sent_in_window": sent_win,
                "sent_last_24h": ss.get("sent_last_24h", 0),
                "sent_last_7d": ss.get("sent_last_7d", 0),
                "last_sent_at": ss.get("last_sent_at"),
                "missed_overdue": missed,
                "delivery_rate_pct": _pct(sent_win, denom) if denom > 0 else None,
            }
        )

    missed_total = sum(missed_map.values())
    cron_triggers = [t for t in triggers_out if t.get("channel") == "cron"]
    cron_sent_24h = sum(t.get("sent_last_24h") or 0 for t in cron_triggers)
    cron_eligible = sum(
        (t.get("eligible_now") or 0) for t in cron_triggers if t.get("eligible_now") is not None
    )

    return {
        "as_of": str(today),
        "outreach_log_available": outreach_log_available,
        "rpc_available": rpc_fetcher is not None,
        "new_user_window_days": window_days,
        "welcome_miss_hours": welcome_miss_hours,
        "cohort_users": len(cohort_set),
        "any_eligible_now_capped": any_capped,
        "missed_total": missed_total,
        "missed_by_trigger": missed_map,
        "cron_sent_last_24h": cron_sent_24h,
        "cron_eligible_now": cron_eligible,
        "triggers": triggers_out,
    }
