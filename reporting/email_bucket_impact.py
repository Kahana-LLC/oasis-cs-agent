"""V1: DAU bucket mix for users exposed vs not exposed to lifecycle emails."""

from __future__ import annotations

from datetime import date
from typing import Any

import pandas as pd

from reporting.dau_model import BUCKET_KEYS, BUCKET_LABELS, activity_by_user_from_df, classify_users_as_of
from reporting.lifecycle_email_sends import (
    _cohort_user_ids,
    _pct,
    _users_with_email_triggers,
    load_new_user_window_days,
    load_phase1_triggers,
)


def _bucket_distribution(
    user_ids: list[str],
    buckets: dict[str, str],
) -> dict[str, Any]:
    n = len(user_ids)
    counts: dict[str, int] = {k: 0 for k in BUCKET_KEYS}
    for uid in user_ids:
        b = buckets.get(uid, "dead")
        if b in counts:
            counts[b] += 1
    pcts = {k: _pct(counts[k], n) for k in BUCKET_KEYS}
    return {"users": n, "counts": counts, "pct": pcts}


def compute_email_bucket_impact(
    *,
    users_df: pd.DataFrame,
    activity_df: pd.DataFrame,
    outreach_log: list[dict[str, Any]] | None = None,
    dau_model: dict[str, Any] | None = None,
    today: date | None = None,
    window_days: int | None = None,
) -> dict[str, Any]:
    """Compare today's DAU bucket mix: received email vs did not (signup cohort)."""
    today = today or date.today()
    outreach_log = outreach_log or []
    window_days = window_days if window_days is not None else load_new_user_window_days()

    cohort_ids = _cohort_user_ids(users_df, today=today, window_days=window_days)
    cohort_set = set(cohort_ids)

    activity_by_user = activity_by_user_from_df(activity_df)
    all_uids = users_df["user_id"].astype(str).tolist() if not users_df.empty else []
    buckets = classify_users_as_of(all_uids, activity_by_user, today)

    email_by_trigger = _users_with_email_triggers(outreach_log)

    emails: list[dict[str, Any]] = []
    for t in load_phase1_triggers():
        trigger = str(t.get("dedup_trigger_name") or "")
        exposed = email_by_trigger.get(trigger, set()) & cohort_set
        not_exposed = cohort_set - exposed
        exposed_list = sorted(exposed)
        not_exposed_list = sorted(not_exposed)
        exp_dist = _bucket_distribution(exposed_list, buckets)
        not_dist = _bucket_distribution(not_exposed_list, buckets)
        emails.append(
            {
                "dedup_trigger_name": trigger,
                "label": t.get("brevo_template") or trigger,
                "exposed": exp_dist,
                "not_exposed": not_dist,
                "current_pct_exposed": exp_dist["pct"].get("current"),
                "current_pct_not_exposed": not_dist["pct"].get("current"),
            }
        )

    any_exposed: set[str] = set()
    for t in load_phase1_triggers():
        trigger = str(t.get("dedup_trigger_name") or "")
        any_exposed |= email_by_trigger.get(trigger, set()) & cohort_set
    any_not = cohort_set - any_exposed

    flow_context: dict[str, float | None] = {}
    if dau_model:
        flow_context = {
            k: (dau_model.get("flow_rates_pct") or {}).get(k)
            for k in ("NURR", "CURR", "iWAURR", "Resurrection_Rate")
        }

    return {
        "as_of": str(today),
        "new_user_window_days": window_days,
        "cohort_users": len(cohort_set),
        "bucket_labels": BUCKET_LABELS,
        "methodology": (
            "V1 compares bucket mix today for users who received an email vs those "
            "who did not (within the signup cohort). Not causal; flow rates are population-level."
        ),
        "population_flow_rates_pct": flow_context,
        "any_lifecycle_email": {
            "exposed": _bucket_distribution(sorted(any_exposed), buckets),
            "not_exposed": _bucket_distribution(sorted(any_not), buckets),
        },
        "by_trigger": emails,
    }
