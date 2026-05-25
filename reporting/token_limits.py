"""Daily token limit hit detection (shared by monetization + lifecycle readiness)."""

from __future__ import annotations

import pandas as pd

from models.db import Plan, PlanOverride


def effective_daily_limits(
    users_df: pd.DataFrame,
    plans: list[Plan],
    overrides: list[PlanOverride],
) -> dict[str, int]:
    plan_limits = {p.plan_id: p.limit_daily or 100_000 for p in plans}
    default = plan_limits.get("Free", 100_000)
    override_map = {
        str(o.user_id): o.limit_daily_override
        for o in overrides
        if o.limit_daily_override is not None
    }
    limits: dict[str, int] = {}
    for _, row in users_df.iterrows():
        uid = row["user_id"]
        if uid in override_map:
            limits[uid] = override_map[uid]
        else:
            limits[uid] = plan_limits.get(row["plan_id"], default)
    return limits


def users_who_hit_daily_limit(
    users_df: pd.DataFrame,
    daily_df: pd.DataFrame,
    plans: list[Plan],
    overrides: list[PlanOverride],
) -> tuple[set[str], int, list[int], dict[int, int], float, int]:
    """Users who ever hit daily token cap; also limit_hit_days and rate inputs."""
    total_users = len(users_df)
    limits = effective_daily_limits(users_df, plans, overrides)
    limit_hit_users: set[str] = set()
    limit_hit_days = 0
    first_limit_days: list[int] = []
    hits_by_lifecycle: dict[int, int] = {}

    if not daily_df.empty and total_users > 0:
        signup_map = users_df.set_index("user_id")["signup_date"].to_dict()
        for _, row in daily_df.iterrows():
            uid = row["user_id"]
            limit = limits.get(uid, 100_000)
            if row["total_tokens"] >= limit:
                limit_hit_days += 1
                limit_hit_users.add(uid)
                sd = signup_map.get(uid)
                if sd:
                    lifecycle = (row["usage_date"] - sd).days
                    hits_by_lifecycle[lifecycle] = hits_by_lifecycle.get(lifecycle, 0) + 1
                    first_limit_days.append(lifecycle)

        users_with_daily = daily_df["user_id"].nunique()
        limit_hit_rate = round(
            100.0 * len(limit_hit_users) / users_with_daily, 1
        ) if users_with_daily else 0.0
    else:
        limit_hit_rate = 0.0
        users_with_daily = 0

    return (
        limit_hit_users,
        limit_hit_days,
        first_limit_days,
        hits_by_lifecycle,
        limit_hit_rate,
        users_with_daily,
    )
