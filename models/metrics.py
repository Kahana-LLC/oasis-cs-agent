from datetime import date
from enum import Enum
from uuid import UUID
from pydantic import BaseModel


class UserSegment(str, Enum):
    healthy = "healthy"
    at_risk = "at_risk"
    high_value = "high_value"
    inactive = "inactive"


class UserMetrics(BaseModel):
    user_id: UUID
    lifecycle_day: int
    active_days_total: int
    active_days_last_7: int
    active_days_last_30: int
    session_count: int
    session_gap: int            # days since last session; lifecycle_day if never had one
    days_since_last_active: int  # days since last usage_date; lifecycle_day if no usage
    last_active_date: date | None
    command_diversity: int       # distinct command_type values seen
    weekly_requests: int         # sum request_count last 7 days
    weekly_requests_prev: int    # sum request_count prior 7 days (for WoW comparison)
    total_commands: int          # total llm_usage rows
    command_type_breakdown: dict[str, int]
    dominant_command_type: str | None
    total_tokens_used: int
    plan_id: str | None
    company_domain: bool
    has_recent_negative_feedback: bool
    segment: UserSegment | None = None
