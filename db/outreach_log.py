"""cs_outreach_log — dedup gate for lifecycle and CS agent sends."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from db.client import get_http_client, _api_key, _base_url
from urllib.parse import quote


def _table_url() -> str:
    return f"{_base_url()}/{quote('cs_outreach_log', safe='')}"


def _headers(*, prefer: str | None = None) -> dict[str, str]:
    h = {
        "apikey": _api_key(),
        "Authorization": f"Bearer {_api_key()}",
        "Content-Type": "application/json",
    }
    if prefer:
        h["Prefer"] = prefer
    return h


def was_triggered(user_id: UUID | str, trigger_name: str) -> bool:
    """True if this user already received trigger_name."""
    uid = str(user_id)
    client = get_http_client()
    resp = client.get(
        _table_url(),
        headers=_headers(),
        params={
            "select": "id",
            "user_id": f"eq.{uid}",
            "trigger_name": f"eq.{trigger_name}",
            "limit": "1",
        },
    )
    if resp.status_code == 404:
        raise RuntimeError(
            "Table cs_outreach_log not found — run supabase/migrations/20260525140000_cs_outreach_log.sql"
        )
    resp.raise_for_status()
    rows = resp.json()
    return bool(rows)


def log_outreach(
    *,
    user_id: UUID | str,
    trigger_name: str,
    channel: str = "email",
    message_preview: str | None = None,
    provider: str = "brevo",
) -> dict[str, Any]:
    """Insert dedup row after a successful send."""
    body = {
        "user_id": str(user_id),
        "trigger_name": trigger_name,
        "channel": channel,
        "message_preview": message_preview,
        "provider": provider,
    }
    client = get_http_client()
    resp = client.post(
        _table_url(),
        headers=_headers(prefer="return=representation"),
        json=body,
    )
    if resp.status_code == 409:
        return {"duplicate": True, "trigger_name": trigger_name, "user_id": str(user_id)}
    resp.raise_for_status()
    rows = resp.json()
    return rows[0] if isinstance(rows, list) and rows else body
