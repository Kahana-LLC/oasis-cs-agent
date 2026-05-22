from __future__ import annotations

from .client import get_client
from models.db import (
    User,
    Session,
    LLMUsage,
    LLMDailyUsage,
    FeedbackEvent,
    Plan,
    PlanOverride,
    Payment,
    UserPlan,
)

_PAGE_SIZE = 1000


def _paginate(table: str, filters: dict | None = None) -> list[dict]:
    """Fetch all rows from a table, paginating through PostgREST's 1000-row limit."""
    client = get_client()
    rows: list[dict] = []
    start = 0

    while True:
        query = client.table(table).select("*").range(start, start + _PAGE_SIZE - 1)
        if filters:
            for col, val in filters.items():
                query = query.eq(col, val)
        batch = query.execute().data
        rows.extend(batch)
        if len(batch) < _PAGE_SIZE:
            break
        start += _PAGE_SIZE

    return rows


def fetch_users() -> list[User]:
    return [User(**row) for row in _paginate("users", {"status": "active"})]


def fetch_all_users() -> list[User]:
    return [User(**row) for row in _paginate("users")]


def fetch_sessions() -> list[Session]:
    return [Session(**row) for row in _paginate("sessions")]


def fetch_usage() -> list[LLMUsage]:
    rows = [r for r in _paginate("llm_usage") if r.get("user_id") is not None]
    return [LLMUsage(**row) for row in rows]


def fetch_daily_usage() -> list[LLMDailyUsage]:
    return [LLMDailyUsage(**row) for row in _paginate("llm_daily_usage")]


def fetch_feedback() -> list[FeedbackEvent]:
    rows = [r for r in _paginate("feedback_events") if r.get("user_id") is not None]
    return [FeedbackEvent(**row) for row in rows]


def fetch_plans() -> list[Plan]:
    return [Plan(**row) for row in _paginate("plan")]


def fetch_plan_overrides() -> list[PlanOverride]:
    return [PlanOverride(**row) for row in _paginate("plan_override")]


def fetch_payments() -> list[Payment]:
    rows = [r for r in _paginate("payments") if r.get("user_id") is not None]
    return [Payment(**row) for row in rows]


def fetch_user_plans() -> list[UserPlan]:
    rows = [r for r in _paginate("user_plans") if r.get("user_id") is not None]
    return [UserPlan(**row) for row in rows]
