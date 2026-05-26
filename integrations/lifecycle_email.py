"""Lifecycle email sends via Brevo transactional templates + cs_outreach_log dedup."""

from __future__ import annotations

import json
import os
from typing import Any
from uuid import UUID

from integrations.brevo_phase1 import (
    _brevo_client,
    brevo_api_key,
    first_name_from_user,
    load_manifest,
    lookup_user,
    welcome_greeting_line,
)

WELCOME_TRIGGER = "welcome_email"
ACTIVATION_NUDGE_TRIGGER = "activation_nudge_24h"
ACTIVATION_CS_CALENDAR_TRIGGER = "activation_cs_calendar"
NPS_DAY3_TRIGGER = "nps_day3"
PMF_DAY10_TRIGGER = "pmf_day10"
IMPLEMENTED_TRIGGERS = frozenset({
    WELCOME_TRIGGER,
    ACTIVATION_NUDGE_TRIGGER,
    ACTIVATION_CS_CALENDAR_TRIGGER,
    NPS_DAY3_TRIGGER,
    PMF_DAY10_TRIGGER,
})


def _lifecycle_config() -> dict[str, Any]:
    manifest = load_manifest()
    cfg = manifest.get("launch_config", {}).get("supabase_lifecycle_email") or {}
    if not cfg:
        raise ValueError("launch_config.supabase_lifecycle_email missing from email_sequences.json")
    return cfg


def trigger_spec(trigger_name: str) -> dict[str, Any]:
    cfg = _lifecycle_config()
    for row in cfg.get("triggers") or []:
        if row.get("dedup_trigger_name") == trigger_name:
            return row
    raise ValueError(f"Unknown lifecycle trigger: {trigger_name!r}")


def template_id_for_trigger(trigger_name: str) -> int:
    spec = trigger_spec(trigger_name)
    env_key = spec.get("env_template_id") or ""
    raw = (os.environ.get(env_key) or "").strip() if env_key else ""
    if not raw:
        raise ValueError(
            f"Set {env_key} in .env to the Brevo SMTP template id for "
            f"{spec.get('brevo_template')!r} (run scripts/list_brevo_smtp_templates.py)"
        )
    return int(raw)


def sender_for_lifecycle() -> dict[str, str]:
    email = (
        os.environ.get("LIFECYCLE_SENDER_EMAIL")
        or os.environ.get("FROM_EMAIL")
        or ""
    ).strip()
    name = (
        os.environ.get("LIFECYCLE_SENDER_NAME")
        or os.environ.get("FROM_NAME")
        or "Adam from Oasis"
    ).strip()
    if not email:
        raise ValueError("Set LIFECYCLE_SENDER_EMAIL or FROM_EMAIL in .env (verified Brevo sender)")
    return {"email": email, "name": name}


def send_lifecycle_email(
    *,
    trigger_name: str,
    email: str | None = None,
    user_id: str | None = None,
    dry_run: bool = False,
    force: bool = False,
) -> dict[str, Any]:
    """
    Send one lifecycle email if not already logged in cs_outreach_log.

    Implemented: welcome_email, activation_nudge_24h, activation_cs_calendar, nps_day3, pmf_day10.
    """
    if trigger_name not in IMPLEMENTED_TRIGGERS:
        raise ValueError(
            f"Trigger {trigger_name!r} not implemented yet. "
            f"Available: {', '.join(sorted(IMPLEMENTED_TRIGGERS))}"
        )

    from db.outreach_log import log_outreach, was_triggered

    user = lookup_user(email=email, user_id=user_id)
    spec = trigger_spec(trigger_name)
    template_id = template_id_for_trigger(trigger_name)
    greeting = welcome_greeting_line(user.name)
    first = first_name_from_user(user.name, user.email)
    sender = sender_for_lifecycle()

    if was_triggered(user.user_id, trigger_name) and not force:
        return {
            "skipped": True,
            "reason": "already_sent",
            "user_id": str(user.user_id),
            "email": user.email,
            "trigger_name": trigger_name,
        }

    payload = {
        "trigger_name": trigger_name,
        "sequence_id": spec.get("sequence_id"),
        "brevo_template": spec.get("brevo_template"),
        "template_id": template_id,
        "to": user.email,
        "first_name": first,
        "greeting": greeting,
        "sender": sender,
    }
    if dry_run:
        return {"dry_run": True, **payload}

    if trigger_name in (ACTIVATION_NUDGE_TRIGGER, ACTIVATION_CS_CALENDAR_TRIGGER):
        from db.client import _api_key, _base_url, get_http_client

        headers = {"apikey": _api_key(), "Authorization": f"Bearer {_api_key()}"}
        usage_resp = get_http_client().get(
            f"{_base_url()}/llm_usage",
            headers=headers,
            params={"select": "usage_id", "user_id": f"eq.{user.user_id}", "limit": "1"},
        )
        usage_resp.raise_for_status()
        usage = usage_resp.json()
        if isinstance(usage, list) and usage:
            return {
                "skipped": True,
                "reason": "has_first_prompt",
                "user_id": str(user.user_id),
                "trigger_name": trigger_name,
            }

    if trigger_name == ACTIVATION_CS_CALENDAR_TRIGGER:
        from db.client import _api_key, _base_url, get_http_client

        fb_resp = get_http_client().get(
            f"{_base_url()}/feedback_events",
            headers={"apikey": _api_key(), "Authorization": f"Bearer {_api_key()}"},
            params={"select": "feedback_id", "user_id": f"eq.{user.user_id}", "limit": "1"},
        )
        fb_resp.raise_for_status()
        fb = fb_resp.json()
        if isinstance(fb, list) and fb:
            return {
                "skipped": True,
                "reason": "has_training",
                "user_id": str(user.user_id),
                "trigger_name": trigger_name,
            }

    client = _brevo_client()
    to_name = first if (user.name and user.name.strip()) else "there"
    result = client.transactional_emails.send_transac_email(
        template_id=template_id,
        to=[{"email": user.email, "name": to_name}],
        params={
            "GREETING": greeting,
            "FIRSTNAME": first,
            "first_name": first,
            "EMAIL": user.email,
        },
        sender=sender,
        tags=[trigger_name, spec.get("sequence_id") or "lifecycle"],
    )
    message_id = getattr(result, "message_id", None)
    preview = f"{spec.get('brevo_template')} (template {template_id}) message_id={message_id}"
    log_row = log_outreach(
        user_id=user.user_id,
        trigger_name=trigger_name,
        channel="email",
        message_preview=preview,
        provider="brevo",
    )
    return {
        "sent": True,
        "user_id": str(user.user_id),
        "email": user.email,
        "trigger_name": trigger_name,
        "template_id": template_id,
        "message_id": message_id,
        "outreach_log": log_row,
    }


def send_welcome_email(
    *,
    email: str | None = None,
    user_id: str | None = None,
    dry_run: bool = False,
    force: bool = False,
) -> dict[str, Any]:
    return send_lifecycle_email(
        trigger_name=WELCOME_TRIGGER,
        email=email,
        user_id=user_id,
        dry_run=dry_run,
        force=force,
    )
