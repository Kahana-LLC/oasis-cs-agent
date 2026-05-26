"""Phase 1 lifecycle email send coverage from cs_outreach_log."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import pandas as pd

from reporting.dau_model import activity_by_user_from_df, classify_users_as_of

_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATHS = (
    _ROOT / "reporting" / "email_sequences.json",
    _ROOT / "public" / "email_sequences.json",
)
DEFAULT_NEW_USER_WINDOW_DAYS = 30
RECENT_SENDS_DAYS = 7


def _load_manifest() -> dict[str, Any]:
    for path in MANIFEST_PATHS:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    return {}


def load_supabase_lifecycle_triggers() -> list[dict[str, Any]]:
    """All shipped Supabase Edge triggers from launch_config.supabase_lifecycle_email."""
    data = _load_manifest()
    plan = (data.get("launch_config") or {}).get("supabase_lifecycle_email") or {}
    triggers = list(plan.get("triggers") or [])
    if triggers:
        return triggers
    sequences = data.get("sequences") or []
    built: list[dict[str, Any]] = []
    for seq in sequences:
        if seq.get("deployed_via") != "supabase_edge":
            continue
        if seq.get("implementation_status") != "shipped":
            continue
        for touch in seq.get("touches") or []:
            name = touch.get("dedup_trigger_name")
            if not name:
                continue
            built.append(
                {
                    "dedup_trigger_name": name,
                    "sequence_id": seq.get("id"),
                    "brevo_template": touch.get("brevo_template") or seq.get("name"),
                    "channel": touch.get("channel") or "cron",
                    "implementation_status": "shipped",
                }
            )
    return built


def load_phase1_triggers() -> list[dict[str, Any]]:
    """Backward-compatible alias for load_supabase_lifecycle_triggers."""
    return load_supabase_lifecycle_triggers()


def load_new_user_window_days() -> int:
    data = _load_manifest()
    reporting = (data.get("launch_config") or {}).get("lifecycle_reporting") or {}
    raw = reporting.get("new_user_window_days")
    if raw is None:
        return DEFAULT_NEW_USER_WINDOW_DAYS
    try:
        return max(1, int(raw))
    except (TypeError, ValueError):
        return DEFAULT_NEW_USER_WINDOW_DAYS


def _pct(count: int, total: int) -> float | None:
    if total <= 0:
        return None
    return round(100.0 * count / total, 1)


def _parse_sent_at(value: Any) -> datetime | None:
    if value is None:
        return None
    try:
        ts = pd.Timestamp(value)
        if pd.isna(ts):
            return None
        return ts.to_pydatetime().replace(tzinfo=None)
    except (TypeError, ValueError):
        return None


def _users_with_email_triggers(
    outreach_log: list[dict[str, Any]],
) -> dict[str, set[str]]:
    by_trigger: dict[str, set[str]] = defaultdict(set)
    for row in outreach_log:
        uid = row.get("user_id")
        trigger = row.get("trigger_name")
        if uid is None or not trigger:
            continue
        by_trigger[str(trigger)].add(str(uid))
    return by_trigger


def _cohort_user_ids(
    users_df: pd.DataFrame,
    *,
    today: date,
    window_days: int,
) -> list[str]:
    if users_df.empty:
        return []
    cutoff = today - timedelta(days=window_days)
    created = pd.to_datetime(users_df["created_at"]).dt.tz_localize(None)
    mask = (users_df["status"] == "active") & (created.dt.date >= cutoff)
    return users_df.loc[mask, "user_id"].astype(str).tolist()


def compute_lifecycle_email_sends(
    *,
    users_df: pd.DataFrame,
    activity_df: pd.DataFrame,
    outreach_log: list[dict[str, Any]] | None = None,
    outreach_log_available: bool = False,
    today: date | None = None,
    window_days: int | None = None,
) -> dict[str, Any]:
    """Send counts per Phase 1 trigger for recent signups."""
    today = today or date.today()
    outreach_log = outreach_log or []
    window_days = window_days if window_days is not None else load_new_user_window_days()
    triggers = load_supabase_lifecycle_triggers()

    cohort_ids = _cohort_user_ids(users_df, today=today, window_days=window_days)
    cohort_set = set(cohort_ids)
    cohort_n = len(cohort_set)

    activity_by_user = activity_by_user_from_df(activity_df)
    all_user_ids = users_df["user_id"].astype(str).tolist() if not users_df.empty else []
    buckets = classify_users_as_of(all_user_ids, activity_by_user, today)
    new_bucket_ids = [uid for uid in cohort_ids if buckets.get(uid) == "new"]
    new_bucket_set = set(new_bucket_ids)
    new_bucket_n = len(new_bucket_set)

    email_by_trigger = _users_with_email_triggers(outreach_log)

    def stats_for(user_set: set[str]) -> list[dict[str, Any]]:
        n = len(user_set)
        rows: list[dict[str, Any]] = []
        for t in triggers:
            trigger_name = str(t.get("dedup_trigger_name") or "")
            sent_uids = email_by_trigger.get(trigger_name, set()) & user_set
            sent_count = len(sent_uids)
            rows.append(
                {
                    "dedup_trigger_name": trigger_name,
                    "sequence_id": t.get("sequence_id"),
                    "label": t.get("brevo_template") or trigger_name,
                    "brevo_template": t.get("brevo_template"),
                    "channel": t.get("channel"),
                    "when": t.get("when"),
                    "sent_count": sent_count,
                    "pct_of_cohort": _pct(sent_count, n),
                }
            )
        return rows

    cohort_triggers = stats_for(cohort_set)
    new_bucket_triggers = stats_for(new_bucket_set)

    users_with_any = set()
    for row in cohort_triggers:
        trigger_name = row["dedup_trigger_name"]
        users_with_any |= email_by_trigger.get(trigger_name, set()) & cohort_set

    users_with_all_five = cohort_set.copy()
    for t in triggers:
        trigger_name = str(t.get("dedup_trigger_name") or "")
        users_with_all_five &= email_by_trigger.get(trigger_name, set())

    recent_cutoff = datetime.combine(today, datetime.min.time()) - timedelta(
        days=RECENT_SENDS_DAYS
    )
    recent_by_trigger: Counter[str] = Counter()
    for row in outreach_log:
        trigger = row.get("trigger_name")
        if not trigger:
            continue
        sent = _parse_sent_at(row.get("sent_at"))
        if sent is not None and sent >= recent_cutoff:
            recent_by_trigger[str(trigger)] += 1

    return {
        "as_of": str(today),
        "outreach_log_available": outreach_log_available,
        "outreach_log_row_count": len(outreach_log),
        "new_user_window_days": window_days,
        "cohort": {
            "label": f"Active signups last {window_days} days",
            "users": cohort_n,
            "triggers": cohort_triggers,
            "users_with_any_lifecycle_email": len(users_with_any),
            "pct_with_any_lifecycle_email": _pct(len(users_with_any), cohort_n),
            "users_with_all_five": len(users_with_all_five),
            "pct_with_all_five": _pct(len(users_with_all_five), cohort_n),
        },
        "new_bucket": {
            "label": "DAU bucket: new (within cohort window)",
            "users": new_bucket_n,
            "triggers": new_bucket_triggers,
        },
        "recent_sends_7d": [
            {"trigger_name": k, "count": v}
            for k, v in sorted(recent_by_trigger.items(), key=lambda x: (-x[1], x[0]))
        ],
    }
