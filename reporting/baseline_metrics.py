"""Aggregate baseline metrics for the Oasis activation & engagement report."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timedelta
from typing import Any
import pandas as pd

from models.db import (
    FeedbackEvent,
    LLMDailyUsage,
    LLMUsage,
    Payment,
    Plan,
    PlanOverride,
    Session,
    User,
    UserPlan,
)
from reporting.cost_model import total_api_cost_usd
from reporting.dau_model import compute_dau_model
from reporting.launch_kpis import compute_launch_kpis

RETENTION_DAYS = (1, 3, 7, 14, 30)
ACTIVATION_WINDOWS_HOURS = {"1h": 1, "24h": 24, "3d": 72, "7d": 168}
FEEDBACK_ANOMALY_MINUTES = 15
LTV_ASSUMED_MONTHS = 12


@dataclass
class BaselineSnapshot:
    generated_at: str
    snapshot_date: str
    total_users: int
    active_users: int
    limitations: list[str]

    activation: dict[str, Any]
    engagement: dict[str, Any]
    retention: dict[str, Any]
    monetization: dict[str, Any]
    feedback: dict[str, Any]
    dau_model: dict[str, Any] = field(default_factory=dict)
    launch_kpis: dict[str, Any] = field(default_factory=dict)
    deltas: dict[str, Any] = field(default_factory=dict)
    key_insights: dict[str, Any] = field(default_factory=dict)
    metric_tooltips: dict[str, str] = field(default_factory=dict)
    validation: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _to_naive_ts(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series).dt.tz_localize(None)


def _users_df(users: list[User]) -> pd.DataFrame:
    df = pd.DataFrame(
        [
            {
                "user_id": str(u.user_id),
                "created_at": u.created_at,
                "signup_date": u.created_at.date(),
                "plan_id": u.plan_id or "Free",
                "status": u.status or "active",
            }
            for u in users
        ]
    )
    if df.empty:
        return df
    df["created_at"] = _to_naive_ts(df["created_at"])
    df["signup_week"] = df["created_at"].dt.to_period("W").astype(str)
    return df


def _usage_df(usage: list[LLMUsage]) -> pd.DataFrame:
    if not usage:
        return pd.DataFrame(columns=["user_id", "timestamp", "activity_date"])
    df = pd.DataFrame(
        [
            {
                "user_id": str(u.user_id),
                "timestamp": u.timestamp,
                "activity_date": u.timestamp.date(),
            }
            for u in usage
        ]
    )
    df["timestamp"] = _to_naive_ts(df["timestamp"])
    return df


def _sessions_df(sessions: list[Session]) -> pd.DataFrame:
    if not sessions:
        return pd.DataFrame(columns=["user_id", "started_at", "activity_date"])
    df = pd.DataFrame(
        [
            {
                "user_id": str(s.user_id),
                "started_at": s.started_at,
                "activity_date": s.started_at.date(),
            }
            for s in sessions
        ]
    )
    df["started_at"] = _to_naive_ts(df["started_at"])
    return df


def _daily_df(daily: list[LLMDailyUsage]) -> pd.DataFrame:
    if not daily:
        return pd.DataFrame(columns=["user_id", "usage_date", "request_count", "total_tokens"])
    return pd.DataFrame(
        [
            {
                "user_id": str(d.user_id),
                "usage_date": d.usage_date,
                "request_count": d.request_count,
                "total_tokens": d.total_tokens,
            }
            for d in daily
        ]
    )


def _first_prompts(usage_df: pd.DataFrame) -> pd.DataFrame:
    if usage_df.empty:
        return pd.DataFrame(columns=["user_id", "first_prompt_at"])
    return (
        usage_df.groupby("user_id")["timestamp"]
        .min()
        .reset_index()
        .rename(columns={"timestamp": "first_prompt_at"})
    )


def _activity_days(usage_df: pd.DataFrame, sessions_df: pd.DataFrame) -> pd.DataFrame:
    parts = []
    if not usage_df.empty:
        parts.append(usage_df[["user_id", "activity_date"]])
    if not sessions_df.empty:
        parts.append(sessions_df[["user_id", "activity_date"]])
    if not parts:
        return pd.DataFrame(columns=["user_id", "activity_date"])
    return pd.concat(parts).drop_duplicates()


def _user_active_on_day_n(
    users_df: pd.DataFrame, activity: pd.DataFrame, n: int
) -> pd.Series:
    """Return boolean Series indexed like users_df: active on signup_date + n."""
    if users_df.empty or activity.empty:
        return pd.Series(False, index=users_df.index)

    merged = users_df[["user_id", "signup_date"]].merge(
        activity, on="user_id", how="left"
    )
    merged["lifecycle_day"] = (
        pd.to_datetime(merged["activity_date"]) - pd.to_datetime(merged["signup_date"])
    ).dt.days
    active_n = merged.loc[merged["lifecycle_day"] == n, "user_id"].unique()
    return users_df["user_id"].isin(active_n)


def _compute_activation(users_df: pd.DataFrame, first_prompts: pd.DataFrame) -> dict[str, Any]:
    total = len(users_df)
    merged = users_df.merge(first_prompts, on="user_id", how="left")
    with_prompt = merged["first_prompt_at"].notna().sum()

    hours = (
        (merged["first_prompt_at"] - merged["created_at"]).dt.total_seconds() / 3600
    )
    hours_valid = hours.dropna()

    rates: dict[str, float | None] = {}
    for label, max_h in ACTIVATION_WINDOWS_HOURS.items():
        if total == 0:
            rates[label] = None
        else:
            rates[label] = round(
                100.0 * (hours_valid <= max_h).sum() / total, 1
            )

    return {
        "total_users": total,
        "users_with_first_prompt": int(with_prompt),
        "activation_rate_pct": rates,
        "time_to_first_hours": {
            "median": round(float(hours_valid.median()), 2) if len(hours_valid) else None,
            "mean": round(float(hours_valid.mean()), 2) if len(hours_valid) else None,
        },
    }


def _compute_engagement(
    users_df: pd.DataFrame,
    usage_df: pd.DataFrame,
    daily_df: pd.DataFrame,
    today: date,
) -> dict[str, Any]:
    total = len(users_df)
    if total == 0:
        return {
            "prompts_per_active_day_by_cohort": [],
            "power_users_day0_pct": None,
            "power_users_week0_pct": None,
            "multi_day_ai_first_7d_pct": None,
        }

    # Active days from usage or daily aggregates
    active_from_usage = (
        usage_df.groupby(["user_id", "activity_date"]).size().reset_index(name="n")
        if not usage_df.empty
        else pd.DataFrame(columns=["user_id", "activity_date", "n"])
    )
    active_from_daily = (
        daily_df.loc[daily_df["request_count"] > 0, ["user_id", "usage_date"]]
        .rename(columns={"usage_date": "activity_date"})
        if not daily_df.empty
        else pd.DataFrame(columns=["user_id", "activity_date"])
    )
    active_days = pd.concat(
        [
            active_from_usage[["user_id", "activity_date"]],
            active_from_daily,
        ]
    ).drop_duplicates()

    prompt_counts = (
        usage_df.groupby("user_id").size().reset_index(name="total_prompts")
        if not usage_df.empty
        else pd.DataFrame(columns=["user_id", "total_prompts"])
    )
    active_day_counts = (
        active_days.groupby("user_id").size().reset_index(name="active_days")
        if not active_days.empty
        else pd.DataFrame(columns=["user_id", "active_days"])
    )

    cohort = users_df.merge(prompt_counts, on="user_id", how="left").merge(
        active_day_counts, on="user_id", how="left"
    )
    cohort["total_prompts"] = cohort["total_prompts"].fillna(0)
    cohort["active_days"] = cohort["active_days"].fillna(0)
    cohort["prompts_per_active_day"] = cohort.apply(
        lambda r: round(r["total_prompts"] / r["active_days"], 2)
        if r["active_days"] > 0
        else 0.0,
        axis=1,
    )

    by_week = (
        cohort.groupby("signup_week")["prompts_per_active_day"]
        .mean()
        .round(2)
        .reset_index()
    )
    cohort_rows = [
        {"cohort": row["signup_week"], "avg_prompts_per_active_day": row["prompts_per_active_day"]}
        for _, row in by_week.iterrows()
    ]

    def _prompts_in_window(user_row: pd.Series, days: int) -> int:
        uid = user_row["user_id"]
        created = user_row["created_at"]
        end = created + timedelta(days=days)
        if usage_df.empty:
            return 0
        mask = (usage_df["user_id"] == uid) & (usage_df["timestamp"] >= created) & (
            usage_df["timestamp"] < end
        )
        return int(mask.sum())

    day0_counts = users_df.apply(lambda r: _prompts_in_window(r, 1), axis=1)
    week0_counts = users_df.apply(lambda r: _prompts_in_window(r, 7), axis=1)

    power_day0 = round(100.0 * (day0_counts >= 10).sum() / total, 1)
    power_week0 = round(100.0 * (week0_counts >= 10).sum() / total, 1)

    # Multi-day AI in first 7 days
    if not active_days.empty:
        first7 = users_df.merge(active_days, on="user_id")
        first7["days_since_signup"] = (
            pd.to_datetime(first7["activity_date"]) - pd.to_datetime(first7["signup_date"])
        ).dt.days
        first7 = first7.loc[first7["days_since_signup"].between(0, 6)]
        multi_day = (
            first7.groupby("user_id")["activity_date"].nunique().reset_index(name="distinct_days")
        )
        multi_pct = round(
            100.0 * (multi_day["distinct_days"] >= 2).sum() / total, 1
        )
    else:
        multi_pct = 0.0

    return {
        "prompts_per_active_day_by_cohort": cohort_rows,
        "power_users_day0_pct": power_day0,
        "power_users_week0_pct": power_week0,
        "multi_day_ai_first_7d_pct": multi_pct,
    }


def _compute_retention(
    users_df: pd.DataFrame,
    activity: pd.DataFrame,
    sessions_df: pd.DataFrame,
    today: date,
) -> dict[str, Any]:
    total = len(users_df)
    overall: dict[str, float | None] = {}
    for n in RETENTION_DAYS:
        eligible = users_df[
            (pd.to_datetime(today) - users_df["created_at"]).dt.days >= n
        ]
        if len(eligible) == 0:
            overall[f"D{n}"] = None
            continue
        active = _user_active_on_day_n(eligible, activity, n)
        overall[f"D{n}"] = round(100.0 * active.sum() / len(eligible), 1)

    # Cohort heatmap by signup week
    cohort_matrix: list[dict[str, Any]] = []
    for week, group in users_df.groupby("signup_week"):
        row: dict[str, Any] = {"cohort": week}
        for n in RETENTION_DAYS:
            eligible = group[
                (pd.to_datetime(today) - group["created_at"]).dt.days >= n
            ]
            if len(eligible) == 0:
                row[f"D{n}"] = None
            else:
                active = _user_active_on_day_n(eligible, activity, n)
                row[f"D{n}"] = round(100.0 * active.sum() / len(eligible), 1)
        cohort_matrix.append(row)

    # WAU last 12 weeks
    wau_rows: list[dict[str, Any]] = []
    if not activity.empty:
        activity = activity.copy()
        activity["week"] = pd.to_datetime(activity["activity_date"]).dt.to_period("W")
        for week in sorted(activity["week"].unique())[-12:]:
            week_start = week.start_time.date()
            week_end = week.end_time.date()
            users_in_week = activity.loc[activity["week"] == week, "user_id"].nunique()
            wau_rows.append(
                {
                    "week": str(week),
                    "week_start": str(week_start),
                    "wau": int(users_in_week),
                }
            )
        for i in range(1, len(wau_rows)):
            prev = wau_rows[i - 1]["wau"]
            cur = wau_rows[i]["wau"]
            wau_rows[i]["wow_pct"] = (
                round(100.0 * (cur - prev) / prev, 1) if prev > 0 else None
            )
        if wau_rows:
            wau_rows[0]["wow_pct"] = None

    # Churn among ever-active users
    ever_active_ids: set[str] = set()
    if not activity.empty:
        ever_active_ids.update(activity["user_id"].unique())

    churn: dict[str, float | None] = {}
    if ever_active_ids:
        last_activity: dict[str, date] = {}
        for uid in ever_active_ids:
            dates = activity.loc[activity["user_id"] == uid, "activity_date"]
            last_activity[uid] = max(dates) if len(dates) else today
        for days in (7, 14, 30):
            cutoff = today - timedelta(days=days)
            churned = sum(1 for d in last_activity.values() if d < cutoff)
            churn[f"churn_{days}d_pct"] = round(
                100.0 * churned / len(last_activity), 1
            )
    else:
        for days in (7, 14, 30):
            churn[f"churn_{days}d_pct"] = None

    # Session frequency per active user per week (last 8 weeks)
    session_freq: list[dict[str, Any]] = []
    if not sessions_df.empty:
        sdf = sessions_df.copy()
        sdf["week"] = pd.to_datetime(sdf["activity_date"]).dt.to_period("W")
        for week in sorted(sdf["week"].unique())[-8:]:
            wk = sdf.loc[sdf["week"] == week]
            active_users = wk["user_id"].nunique()
            sessions_count = len(wk)
            session_freq.append(
                {
                    "week": str(week),
                    "sessions_per_active_user": round(
                        sessions_count / active_users, 2
                    )
                    if active_users
                    else 0,
                }
            )

    return {
        "overall_retention_pct": overall,
        "cohort_retention": cohort_matrix,
        "wau_by_week": wau_rows,
        "churn_pct": churn,
        "session_frequency_by_week": session_freq,
    }


def _effective_daily_limits(
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


def _compute_monetization(
    users_df: pd.DataFrame,
    daily_df: pd.DataFrame,
    plans: list[Plan],
    overrides: list[PlanOverride],
    payments: list[Payment],
    user_plans: list[UserPlan],
    usage: list[LLMUsage],
    today: date,
) -> dict[str, Any]:
    total_users = len(users_df)
    limits = _effective_daily_limits(users_df, plans, overrides)

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

    # Premium: users.plan_id Plus or active user_plans
    plus_from_users = set(
        users_df.loc[users_df["plan_id"] == "Plus", "user_id"].tolist()
    )
    plus_from_subs: dict[str, datetime] = {}
    for up in user_plans:
        if up.user_id and (up.is_active is None or up.is_active):
            plus_from_subs[str(up.user_id)] = up.start_date

    premium_users = plus_from_users | set(plus_from_subs.keys())
    conversion_pct = (
        round(100.0 * len(premium_users) / total_users, 1) if total_users else None
    )

    limit_hitter_premium = limit_hit_users & premium_users
    limit_hitter_conv_pct = (
        round(100.0 * len(limit_hitter_premium) / len(limit_hit_users), 1)
        if limit_hit_users
        else None
    )

    median_days_limit = (
        int(pd.Series(first_limit_days).median()) if first_limit_days else None
    )
    median_hours_limit = (
        round(float(median_days_limit) * 24, 1) if median_days_limit is not None else None
    )

    velocities_hours: list[float] = []
    for uid in premium_users:
        created = users_df.loc[users_df["user_id"] == uid, "created_at"]
        if created.empty:
            continue
        start = plus_from_subs.get(uid)
        if start:
            delta = (pd.Timestamp(start) - created.iloc[0]).total_seconds() / 3600
            velocities_hours.append(delta)

    successful = [p for p in payments if p.status == "success"]
    gross_revenue = sum(p.amount for p in successful)
    api_cost = total_api_cost_usd(usage)
    arpu_gross = round(gross_revenue / total_users, 2) if total_users else 0
    arpu_net = round((gross_revenue - api_cost) / total_users, 2) if total_users else 0

    ltv_proxy = round(arpu_net * LTV_ASSUMED_MONTHS, 2)

    lifecycle_buckets = [
        {"lifecycle_day": k, "hit_count": v}
        for k, v in sorted(hits_by_lifecycle.items())
    ]

    return {
        "token_limit_hit_rate_pct": limit_hit_rate,
        "users_hit_limit": len(limit_hit_users),
        "limit_hit_days": limit_hit_days,
        "limit_hits_by_lifecycle_day": lifecycle_buckets,
        "median_days_to_first_limit": median_days_limit,
        "median_hours_to_first_limit": median_hours_limit,
        "premium_conversion_among_limit_hitters_pct": limit_hitter_conv_pct,
        "premium_conversion_pct": conversion_pct,
        "premium_users": len(premium_users),
        "conversion_velocity_hours": {
            "median": round(float(pd.Series(velocities_hours).median()), 1)
            if velocities_hours
            else None,
            "mean": round(float(pd.Series(velocities_hours).mean()), 1)
            if velocities_hours
            else None,
        },
        "arpu_gross_usd": arpu_gross,
        "arpu_net_usd": arpu_net,
        "total_revenue_usd": round(gross_revenue, 2),
        "estimated_api_cost_usd": round(api_cost, 2),
        "ltv_proxy_usd": ltv_proxy,
        "cac_ltv": {
            "cac_available": False,
            "ltv_proxy_usd": ltv_proxy,
            "note": "user_acquisition and events tables empty — provide marketing spend externally",
        },
    }


def _compute_feedback(
    users_df: pd.DataFrame,
    feedback: list[FeedbackEvent],
) -> dict[str, Any]:
    total = len(users_df)
    if not feedback:
        return {
            "submission_rate_pct": 0.0,
            "median_hours_to_first": None,
            "distribution": [],
            "anomalies": [],
            "review_samples": [],
        }

    fdf = pd.DataFrame(
        [
            {
                "feedback_id": str(f.feedback_id),
                "user_id": str(f.user_id),
                "reported_at": f.reported_at,
                "negative_rating": f.negative_rating,
                "category": f.category or "uncategorized",
            }
            for f in feedback
        ]
    )
    fdf["reported_at"] = _to_naive_ts(fdf["reported_at"])

    submitters = fdf["user_id"].nunique()
    submission_rate = round(100.0 * submitters / total, 1) if total else 0.0

    first_fb = fdf.groupby("user_id")["reported_at"].min().reset_index()
    merged = users_df.merge(first_fb, on="user_id", how="inner")
    hours = (merged["reported_at"] - merged["created_at"]).dt.total_seconds() / 3600
    median_hours = round(float(hours.median()), 2) if len(hours) else None

    counts = fdf.groupby("user_id").size()
    buckets = {"0": 0, "1": 0, "2-5": 0, "6-10": 0, "10+": 0}
    buckets["0"] = total - submitters
    for c in counts:
        if c == 1:
            buckets["1"] += 1
        elif c <= 5:
            buckets["2-5"] += 1
        elif c <= 10:
            buckets["6-10"] += 1
        else:
            buckets["10+"] += 1

    distribution = [{"bucket": k, "users": v} for k, v in buckets.items()]

    merged_anom = users_df.merge(first_fb, on="user_id", how="inner")
    merged_anom["minutes"] = (
        merged_anom["reported_at"] - merged_anom["created_at"]
    ).dt.total_seconds() / 60
    anomalies = merged_anom.loc[
        merged_anom["minutes"] < FEEDBACK_ANOMALY_MINUTES,
        ["user_id", "minutes"],
    ]
    anomaly_rows = [
        {"user_id": r["user_id"], "minutes_after_signup": round(r["minutes"], 1)}
        for _, r in anomalies.iterrows()
    ]

    # Stratified samples for manual review
    samples: list[dict[str, Any]] = []
    fast_ids = set(anomalies["user_id"]) if len(anomalies) else set()
    fast = fdf.loc[fdf["user_id"].isin(fast_ids)].head(3)
    for _, r in fast.iterrows():
        samples.append(
            {
                "feedback_id": r["feedback_id"],
                "category": r["category"],
                "negative_rating": r["negative_rating"],
                "reported_at": str(r["reported_at"]),
                "tag": "fast_submitter",
            }
        )
    for cat in fdf["category"].dropna().unique()[:5]:
        row = fdf.loc[fdf["category"] == cat].iloc[0]
        if row["feedback_id"] not in {s["feedback_id"] for s in samples}:
            samples.append(
                {
                    "feedback_id": row["feedback_id"],
                    "category": row["category"],
                    "negative_rating": row["negative_rating"],
                    "reported_at": str(row["reported_at"]),
                    "tag": "by_category",
                }
            )
        if len(samples) >= 10:
            break
    samples = samples[:10]

    return {
        "submission_rate_pct": submission_rate,
        "median_hours_to_first": median_hours,
        "distribution": distribution,
        "anomalies": anomaly_rows,
        "review_samples": samples,
    }


def compute_baseline_snapshot(
    users: list[User],
    sessions: list[Session],
    usage: list[LLMUsage],
    daily: list[LLMDailyUsage],
    feedback: list[FeedbackEvent],
    plans: list[Plan],
    overrides: list[PlanOverride],
    payments: list[Payment],
    user_plans: list[UserPlan],
    today: date | None = None,
) -> BaselineSnapshot:
    today = today or date.today()
    users_df = _users_df(users)
    usage_df = _usage_df(usage)
    sessions_df = _sessions_df(sessions)
    daily_df = _daily_df(daily)
    activity = _activity_days(usage_df, sessions_df)
    first_prompts = _first_prompts(usage_df)

    active_count = int((users_df["status"] == "active").sum()) if not users_df.empty else 0

    activation = _compute_activation(users_df, first_prompts)
    engagement = _compute_engagement(users_df, usage_df, daily_df, today)
    retention = _compute_retention(users_df, activity, sessions_df, today)
    monetization = _compute_monetization(
        users_df, daily_df, plans, overrides, payments, user_plans, usage, today
    )
    feedback_metrics = _compute_feedback(users_df, feedback)
    dau_model = compute_dau_model(users_df, activity, today)
    launch_kpis = compute_launch_kpis(
        activation=activation,
        engagement=engagement,
        retention=retention,
        monetization=monetization,
        feedback=feedback_metrics,
        dau_model=dau_model,
        usage=usage,
        today=today,
        total_users=len(users_df),
    )

    validation = {
        "payments_success_count": len([p for p in payments if p.status == "success"]),
        "payments_revenue_usd": round(
            sum(p.amount for p in payments if p.status == "success"), 2
        ),
        "limit_hit_days": monetization.get("limit_hit_days"),
        "plus_users": monetization.get("premium_users"),
    }

    limitations = [
        f"Small sample size ({len(users)} users) — percentages are directional.",
        "First AI command inferred from llm_usage.timestamp (no first_command_at column).",
        "Token limits inferred from llm_daily_usage vs plan limits, not UX events.",
        "NULL plan_id treated as Free (121/122 users historically).",
        "CAC unavailable — user_acquisition and events tables empty.",
        "Feedback quality requires manual review of sampled rows.",
        "DAU buckets use sessions ∪ llm_usage; flow rates are 7-day average daily transitions.",
    ]

    return BaselineSnapshot(
        generated_at=datetime.utcnow().isoformat() + "Z",
        snapshot_date=str(today),
        total_users=len(users_df),
        active_users=active_count,
        limitations=limitations,
        activation=activation,
        engagement=engagement,
        retention=retention,
        monetization=monetization,
        feedback=feedback_metrics,
        dau_model=dau_model,
        launch_kpis=launch_kpis,
        validation=validation,
    )
