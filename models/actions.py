from typing import Literal
from uuid import UUID
from pydantic import BaseModel


class TriggerResult(BaseModel):
    trigger_name: str
    channel: Literal["email", "in_app", "alert"]


class EmailContent(BaseModel):
    subject: str
    body: str  # plain text, under 150 words


class OutreachLogEntry(BaseModel):
    user_id: UUID
    trigger_name: str
    channel: str
    message_preview: str | None = None
