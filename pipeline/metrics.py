from datetime import date, timedelta

from models.db import User, Session, LLMUsage, LLMDailyUsage, FeedbackEvent
from models.metrics import UserMetrics

_CONSUMER_DOMAINS = {
    "gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "hotmail.co.uk",
    "icloud.com", "protonmail.com", "protonmail.ch", "me.com", "mac.com",
    "live.com", "live.co.uk", "yahoo.co.uk", "googlemail.com", "msn.com",
}


def _is_company_domain(email: str) -> bool:
    domain = email.rsplit("@", 1)[-1].lower()
    return domain not in _CONSUMER_DOMAINS


def compute_metrics(
    user: User,
    sessions: list[Session],
    usage: list[LLMUsage],
    daily_usage: list[LLMDailyUsage],
    feedback: list[FeedbackEvent],
    today: date,
) -> UserMetrics:
    uid = user.user_id

    # --- lifecycle ---
    lifecycle_day = max(0, (today - user.created_at.date()).days)

    # --- sessions ---
    user_sessions = [s for s in sessions if s.user_id == uid]
    session_count = len(user_sessions)
    if user_sessions:
        last_session_date = max(s.started_at.date() for s in user_sessions)
        session_gap = (today - last_session_date).days
    else:
        session_gap = lifecycle_day

    # --- daily usage ---
    user_daily = [d for d in daily_usage if d.user_id == uid]

    cutoff_7 = today - timedelta(days=7)
    cutoff_14 = today - timedelta(days=14)
    cutoff_30 = today - timedelta(days=30)

    active_days_total = len(user_daily)
    active_days_last_7 = sum(1 for d in user_daily if d.usage_date >= cutoff_7)
    active_days_last_30 = sum(1 for d in user_daily if d.usage_date >= cutoff_30)

    if user_daily:
        last_active_date = max(d.usage_date for d in user_daily)
        days_since_last_active = (today - last_active_date).days
    else:
        last_active_date = None
        days_since_last_active = lifecycle_day

    weekly_requests = sum(
        d.request_count for d in user_daily if d.usage_date >= cutoff_7
    )
    weekly_requests_prev = sum(
        d.request_count for d in user_daily
        if cutoff_14 <= d.usage_date < cutoff_7
    )

    # --- llm_usage ---
    user_usage = [u for u in usage if u.user_id == uid]
    total_commands = len(user_usage)

    breakdown: dict[str, int] = {}
    for u in user_usage:
        if u.command_type:
            breakdown[u.command_type] = breakdown.get(u.command_type, 0) + 1

    command_diversity = len(breakdown)
    dominant_command_type = max(breakdown, key=lambda k: breakdown[k]) if breakdown else None
    total_tokens_used = sum(u.total_tokens or 0 for u in user_usage)

    # --- feedback ---
    has_recent_negative_feedback = any(
        f.negative_rating is True and f.reported_at.date() >= cutoff_7
        for f in feedback
        if f.user_id == uid
    )

    return UserMetrics(
        user_id=uid,
        lifecycle_day=lifecycle_day,
        active_days_total=active_days_total,
        active_days_last_7=active_days_last_7,
        active_days_last_30=active_days_last_30,
        session_count=session_count,
        session_gap=session_gap,
        days_since_last_active=days_since_last_active,
        last_active_date=last_active_date,
        command_diversity=command_diversity,
        weekly_requests=weekly_requests,
        weekly_requests_prev=weekly_requests_prev,
        total_commands=total_commands,
        command_type_breakdown=breakdown,
        dominant_command_type=dominant_command_type,
        total_tokens_used=total_tokens_used,
        plan_id=user.plan_id,
        company_domain=_is_company_domain(user.email),
        has_recent_negative_feedback=has_recent_negative_feedback,
    )
