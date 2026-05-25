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
)

WELCOME_TRIGGER = "welcome_email"
IMPLEMENTED_TRIGGERS = frozenset({WELCOME_TRIGGER})


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

    Currently implemented: welcome_email only.
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
        "sender": sender,
    }
    if dry_run:
        return {"dry_run": True, **payload}

    client = _brevo_client()
    result = client.transactional_emails.send_transac_email(
        template_id=template_id,
        to=[{"email": user.email, "name": first}],
        params={"FIRSTNAME": first, "first_name": first},
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
