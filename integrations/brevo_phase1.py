"""Brevo Phase 1 enrollment — Supabase user → Oasis Lifecycle list (triggers Oasis Phase 1 automation)."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any
from uuid import UUID

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "public" / "email_sequences.json"


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def phase1_config(manifest: dict[str, Any] | None = None) -> dict[str, Any]:
    manifest = manifest or load_manifest()
    launch = manifest.get("launch_config") or {}
    cfg = launch.get("brevo_phase1") or launch.get("brevo_phase1_test")
    if not cfg:
        raise ValueError(
            "launch_config.brevo_phase1 missing from email_sequences.json "
            "(legacy key brevo_phase1_test was renamed)"
        )
    return cfg


def phase1_test_config(manifest: dict[str, Any] | None = None) -> dict[str, Any]:
    """Deprecated alias for phase1_config."""
    return phase1_config(manifest)


def resolve_list_id(cfg: dict[str, Any]) -> int:
    raw = (
        os.environ.get("BREVO_LIFECYCLE_LIST_ID")
        or os.environ.get("BREVO_PHASE1_QA_LIST_ID")
        or cfg.get("list_id")
    )
    if raw is None or raw == "":
        raise ValueError(
            "Set BREVO_LIFECYCLE_LIST_ID in .env or launch_config.brevo_phase1.list_id "
            "(Brevo → Contacts → Lists → Oasis Lifecycle)"
        )
    return int(raw)


def brevo_api_key() -> str:
    key = (os.environ.get("BREVO_API_KEY") or "").strip()
    if len(key) >= 2 and key[0] == key[-1] and key[0] in "\"'":
        key = key[1:-1].strip()
    if not key:
        raise ValueError("BREVO_API_KEY is not set")
    return key


def diagnose_brevo_api_key() -> dict[str, Any]:
    """Non-secret hints for 401 troubleshooting (do not log the key itself)."""
    raw = os.environ.get("BREVO_API_KEY")
    try:
        key = brevo_api_key() if raw and raw.strip() else ""
    except ValueError:
        key = ""
    mcp = (os.environ.get("BREVO_MCP_TOKEN") or "").strip()
    hints: list[str] = []
    if not key:
        hints.append("BREVO_API_KEY is missing or empty in .env")
    elif not key.startswith("xkeysib-"):
        hints.append(
            "BREVO_API_KEY does not look like a Brevo v3 REST key (expected prefix xkeysib-). "
            "Create one under SMTP & API → API keys — not the MCP-only token."
        )
    if mcp and key and mcp == key:
        hints.append(
            "BREVO_API_KEY matches BREVO_MCP_TOKEN; use a separate v3 API key for scripts."
        )
    return {
        "api_key_set": bool(key),
        "api_key_length": len(key),
        "api_key_looks_like_v3": key.startswith("xkeysib-") if key else False,
        "mcp_token_set": bool(mcp),
        "hints": hints,
    }


def _brevo_client():
    try:
        from brevo import Brevo
    except ImportError as exc:
        raise ImportError(
            "brevo-python is required. Install: pip install brevo-python python-dotenv"
        ) from exc

    return Brevo(api_key=brevo_api_key())


def list_brevo_lists(limit: int = 50) -> list[dict[str, Any]]:
    client = _brevo_client()
    resp = client.contacts.get_lists(limit=limit, offset=0)
    out: list[dict[str, Any]] = []
    for item in resp.lists or []:
        out.append(
            {
                "id": item.id,
                "name": item.name,
                "total_subscribers": item.total_subscribers,
            }
        )
    return out


def find_list_id_by_name(name: str) -> int | None:
    for row in list_brevo_lists():
        if (row.get("name") or "").strip() == name.strip():
            return int(row["id"])
    return None


def first_name_from_user(name: str | None, email: str) -> str:
    if name and name.strip():
        return name.strip().split()[0]
    local = email.split("@", 1)[0]
    return local.replace(".", " ").replace("_", " ").split()[0].title() or "there"


def lookup_user(
    *,
    email: str | None = None,
    user_id: str | None = None,
) -> Any:
    from db.fetch import fetch_all_users

    users = fetch_all_users()
    if user_id:
        uid = UUID(user_id)
        for u in users:
            if u.user_id == uid:
                return u
        raise LookupError(f"No Supabase user with user_id={user_id}")
    if email:
        needle = email.strip().lower()
        matches = [u for u in users if (u.email or "").strip().lower() == needle]
        if not matches:
            raise LookupError(f"No Supabase user with email={email!r}")
        if len(matches) > 1:
            raise LookupError(f"Multiple Supabase users with email={email!r}")
        return matches[0]
    raise ValueError("Provide --email and/or --user-id")


def enroll_contact(
    *,
    email: str,
    first_name: str,
    oasis_user_id: str,
    list_id: int,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Create or update Brevo contact and add to Oasis Lifecycle list (fires list-triggered automation)."""
    payload = {
        "email": email,
        "attributes": {
            "FIRSTNAME": first_name,
            "OASIS_USER_ID": oasis_user_id,
        },
        "listIds": [list_id],
        "updateEnabled": True,
    }
    if dry_run:
        return {"dry_run": True, "payload": payload}

    client = _brevo_client()
    result = client.contacts.create_contact(
        email=email,
        attributes=payload["attributes"],
        list_ids=[list_id],
        update_enabled=True,
    )
    contact_id = getattr(result, "id", None) if result is not None else None
    return {
        "id": contact_id,
        "email": email,
        "list_id": list_id,
    }


def enroll_user_for_phase1(
    *,
    email: str | None = None,
    user_id: str | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    cfg = phase1_config()
    user = lookup_user(email=email, user_id=user_id)
    list_id = resolve_list_id(cfg)
    first = first_name_from_user(user.name, user.email)
    result = enroll_contact(
        email=user.email,
        first_name=first,
        oasis_user_id=str(user.user_id),
        list_id=list_id,
        dry_run=dry_run,
    )
    return {
        "user_id": str(user.user_id),
        "email": user.email,
        "first_name": first,
        "list_id": list_id,
        "list_name": cfg.get("list_name"),
        "automation_name": cfg.get("automation_name"),
        "template_names": cfg.get("template_names"),
        "brevo": result,
    }


def enroll_user_for_phase1_qa(
    *,
    email: str | None = None,
    user_id: str | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Deprecated alias for enroll_user_for_phase1."""
    return enroll_user_for_phase1(email=email, user_id=user_id, dry_run=dry_run)


def verify_phase1_setup() -> dict[str, Any]:
    """Check API key, list id, and that Oasis Lifecycle list exists in Brevo."""
    cfg = phase1_config()
    list_id = resolve_list_id(cfg)
    expected_name = (cfg.get("list_name") or "Oasis Lifecycle").strip()
    lists = list_brevo_lists()
    match = next((row for row in lists if row["id"] == list_id), None)
    issues: list[str] = []
    if not match:
        issues.append(f"List id {list_id} not found in Brevo account")
    elif (match.get("name") or "").strip() != expected_name:
        issues.append(
            f"List id {list_id} is {match.get('name')!r}, expected {expected_name!r}"
        )
    return {
        "ok": not issues,
        "list_id": list_id,
        "list_name": match.get("name") if match else None,
        "automation_name": cfg.get("automation_name"),
        "issues": issues,
        "all_lists": lists,
    }
