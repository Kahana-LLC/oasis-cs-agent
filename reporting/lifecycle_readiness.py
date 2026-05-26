"""Lifecycle readiness milestones by DAU bucket (email plan cross-tab)."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any

import pandas as pd

from models.db import FeedbackEvent, Plan, PlanOverride
from reporting.token_limits import users_who_hit_daily_limit
from reporting.dau_model import BUCKET_KEYS, activity_by_user_from_df, classify_users_as_of

MANIFEST_PATH = Path(__file__).resolve().parents[1] / "public" / "email_sequences.json"

PRODUCT_MILESTONE_IDS = frozenset(
    {"first_ai_prompt", "daily_limit_hit", "training_done"}
)

EMAIL_PENDING_REASON = "cs_outreach_log not deployed"


def load_readiness_milestones() -> list[dict[str, Any]]:
    """Milestone definitions from email_sequences.json phase_1_activation."""
    if not MANIFEST_PATH.exists():
        return []
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    for phase in data.get("funnel_phases") or []:
        if phase.get("id") == "phase_1_activation":
            return list(phase.get("phase_2_readiness_milestones") or [])
    return []


def _milestone_status(milestone: dict[str, Any], outreach_available: bool) -> str:
    if milestone.get("type") == "email":
        return "live" if outreach_available else "pending"
    return "live"


def _users_with_email_triggers(
    outreach_log: list[dict[str, Any]],
) -> dict[str, set[str]]:
    """Map dedup_trigger_name → user_ids who received that email."""
    by_trigger: dict[str, set[str]] = defaultdict(set)
    for row in outreach_log:
        uid = row.get("user_id")
        trigger = row.get("trigger_name")
        if uid is None or not trigger:
            continue
        by_trigger[str(trigger)].add(str(uid))
    return by_trigger


def _pct(count: int, total: int) -> float | None:
    if total <= 0:
        return None
    return round(100.0 * count / total, 1)


def _aggregate_milestones(
    user_ids: list[str],
    buckets: dict[str, str],
    milestone_users: dict[str, set[str]],
    live_milestone_ids: list[str],
) -> dict[str, Any]:
    by_bucket: dict[str, Any] = {}
    totals_counter: Counter[str] = Counter()

    for bucket_key in BUCKET_KEYS:
        bucket_uids = [uid for uid in user_ids if buckets.get(uid) == bucket_key]
        n = len(bucket_uids)
        milestone_stats: dict[str, dict[str, Any]] = {}
        scores: list[int] = []

        for mid in live_milestone_ids:
            met = sum(1 for uid in bucket_uids if uid in milestone_users.get(mid, set()))
            milestone_stats[mid] = {"count": met, "pct": _pct(met, n)}
            totals_counter[mid] += met

        for uid in bucket_uids:
            scores.append(
                sum(1 for mid in live_milestone_ids if uid in milestone_users.get(mid, set()))
            )

        avg_score = round(sum(scores) / len(scores), 2) if scores else 0.0
        by_bucket[bucket_key] = {
            "users": n,
            "milestones": milestone_stats,
            "readiness": {
                "avg_score": avg_score,
                "max_score": len(live_milestone_ids),
            },
        }

    total_users = len(user_ids)
    totals_milestones = {
        mid: {
            "count": totals_counter[mid],
            "pct": _pct(totals_counter[mid], total_users),
        }
        for mid in live_milestone_ids
    }

    all_scores = [
        sum(1 for mid in live_milestone_ids if uid in milestone_users.get(mid, set()))
        for uid in user_ids
    ]
    users_with_any = sum(1 for s in all_scores if s > 0)

    return {
        "by_bucket": by_bucket,
        "totals": {
            "users": total_users,
            "milestones": totals_milestones,
            "users_with_any_product_milestone": users_with_any,
            "pct_with_any_product_milestone": _pct(users_with_any, total_users),
            "avg_readiness_score": round(sum(all_scores) / total_users, 2)
            if total_users
            else 0.0,
            "max_score": len(live_milestone_ids),
        },
    }


def compute_lifecycle_readiness_by_bucket(
    *,
    users_df: pd.DataFrame,
    activity_df: pd.DataFrame,
    usage_df: pd.DataFrame,
    daily_df: pd.DataFrame,
    feedback: list[FeedbackEvent],
    plans: list[Plan],
    overrides: list[PlanOverride],
    today: date | None = None,
    outreach_log: list[dict[str, Any]] | None = None,
    outreach_log_available: bool = False,
) -> dict[str, Any]:
    """Cross-tab Phase 1 readiness milestones × DAU bucket."""
    today = today or date.today()
    outreach_log = outreach_log or []
    outreach_available = outreach_log_available

    raw_milestones = load_readiness_milestones()
    milestone_meta: list[dict[str, Any]] = []
    for m in raw_milestones:
        status = _milestone_status(m, outreach_available)
        entry: dict[str, Any] = {
            "id": m.get("id"),
            "label": m.get("label"),
            "type": m.get("type"),
            "status": status,
        }
        if m.get("type") == "email":
            entry["dedup_trigger_name"] = m.get("dedup_trigger_name")
        else:
            entry["source_table"] = m.get("source_table")
        if status == "pending":
            entry["pending_reason"] = EMAIL_PENDING_REASON
        milestone_meta.append(entry)

    live_milestone_ids = [m["id"] for m in milestone_meta if m.get("status") == "live"]

    user_ids = users_df["user_id"].astype(str).tolist() if not users_df.empty else []
    activity_by_user = activity_by_user_from_df(activity_df)
    buckets = classify_users_as_of(user_ids, activity_by_user, today)

    first_prompt_users: set[str] = set()
    if not usage_df.empty:
        first_prompt_users = set(
            usage_df.groupby("user_id").size().index.astype(str).tolist()
        )

    limit_hit_users, *_rest = users_who_hit_daily_limit(
        users_df, daily_df, plans, overrides
    )

    training_users: set[str] = set()
    if feedback:
        training_users = {str(f.user_id) for f in feedback if f.user_id}

    email_by_trigger = _users_with_email_triggers(outreach_log)
    milestone_users: dict[str, set[str]] = {
        "first_ai_prompt": first_prompt_users,
        "daily_limit_hit": limit_hit_users,
        "training_done": training_users,
    }
    for m in raw_milestones:
        if m.get("type") != "email":
            continue
        mid = m.get("id")
        trigger = m.get("dedup_trigger_name")
        if mid and trigger and outreach_available:
            milestone_users[mid] = email_by_trigger.get(trigger, set())

    agg = _aggregate_milestones(user_ids, buckets, milestone_users, live_milestone_ids)

    return {
        "as_of": str(today),
        "milestones": milestone_meta,
        "product_milestone_count": sum(
            1 for m in milestone_meta if m.get("id") in PRODUCT_MILESTONE_IDS
        ),
        **agg,
    }
