from models.metrics import UserMetrics, UserSegment


def classify_segment(m: UserMetrics) -> UserSegment | None:
    """Return the first matching segment in priority order, or None for very new users."""

    # Priority 1: High-Value
    if m.active_days_last_7 >= 5 and m.session_count >= 8 and m.company_domain:
        return UserSegment.high_value

    # Priority 2: Healthy
    if m.active_days_last_7 >= 3 and m.days_since_last_active <= 7:
        return UserSegment.healthy

    # Priority 3: At-Risk — has used the product but is drifting or complained
    if m.active_days_total > 0 and (
        m.days_since_last_active > 7 or m.has_recent_negative_feedback
    ):
        return UserSegment.at_risk

    # Priority 4: Inactive
    if (
        (14 <= m.lifecycle_day <= 60 and m.session_gap > 14)
        or (m.lifecycle_day > 60 and m.session_gap > 21)
        or m.active_days_total == 0
    ):
        return UserSegment.inactive

    # Users in days 1–13 with some activity but below healthy thresholds
    return None
