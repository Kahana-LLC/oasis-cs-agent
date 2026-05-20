from datetime import datetime, date
from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator


class User(BaseModel):
    model_config = ConfigDict(extra="ignore")

    user_id: UUID
    email: str
    name: str | None = None
    created_at: datetime
    status: str | None = None
    plan_id: str | None = None


class Session(BaseModel):
    model_config = ConfigDict(extra="ignore")

    session_id: UUID
    user_id: UUID
    started_at: datetime
    ended_at: datetime | None = None


class LLMUsage(BaseModel):
    model_config = ConfigDict(extra="ignore")

    usage_id: UUID
    user_id: UUID
    timestamp: datetime
    command_type: str | None = None
    total_tokens: int | None = None
    success: bool | None = None


class LLMDailyUsage(BaseModel):
    model_config = ConfigDict(extra="ignore")

    user_id: UUID
    usage_date: date
    request_count: int = 0
    total_tokens: int = 0


class FeedbackEvent(BaseModel):
    model_config = ConfigDict(extra="ignore")

    feedback_id: UUID
    user_id: UUID
    negative_rating: bool | None = None
    reported_at: datetime

    @field_validator("reported_at", mode="before")
    @classmethod
    def strip_tz(cls, v: str) -> str:
        # reported_at is timestamptz — strip offset so datetime() parses it
        if isinstance(v, str) and ("+" in v or v.endswith("Z")):
            return v.split("+")[0].rstrip("Z")
        return v
