#!/usr/bin/env python3
"""Send operational broadcast (legal or incident) — SES primary, Resend Pro backup when SES not ready."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "public" / "email_sequences.json"
CONTACTS_CSV = ROOT / "data" / "operational_contacts.csv"

# Lifecycle free tier (do not use for full-list operational blasts)
RESEND_FREE_DAILY_CAP = 100
RESEND_FREE_MONTHLY_CAP = 3000

TEMPLATE_MAP = {
    "legal": "legal_notice",
    "incident": "incident_notice",
}


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def sequence_for_template(template: str) -> dict:
    seq_id = TEMPLATE_MAP.get(template)
    if not seq_id:
        raise SystemExit(f"Unknown template {template!r}; use legal or incident")
    for seq in load_manifest().get("sequences") or []:
        if seq.get("id") == seq_id:
            return seq
    raise SystemExit(f"Sequence {seq_id} not in email_sequences.json")


def load_html(seq: dict) -> tuple[str, str, str]:
    preview = seq.get("preview") or {}
    rel = preview.get("source")
    if not rel:
        raise SystemExit("Sequence missing preview.source")
    path = ROOT / str(rel)
    html = path.read_text(encoding="utf-8")
    subject = str(preview.get("subject") or seq.get("name") or "Oasis notice")
    plain_rel = preview.get("plain_text_source")
    plain = ""
    if plain_rel:
        plain_path = ROOT / str(plain_rel)
        if plain_path.is_file():
            plain = plain_path.read_text(encoding="utf-8")
    return html, subject, plain


def substitute_merge(text: str, first_name: str, email: str) -> str:
    out = text
    out = re.sub(r"\{\{\s*contact\.FIRSTNAME\s*\}\}", first_name, out, flags=re.I)
    out = re.sub(r"\{\{\s*contact\.EMAIL\s*\}\}", email, out, flags=re.I)
    out = re.sub(r"\{\{\s*mirror\s*\}\}", "", out, flags=re.I)
    out = re.sub(r"\{\{\s*unsubscribe\s*\}\}", "#", out, flags=re.I)
    return out


def load_recipients(csv_path: Path) -> list[dict[str, str]]:
    if not csv_path.is_file():
        raise SystemExit(f"Missing {csv_path} — run: python reporting/sync_operational_contacts.py")
    with csv_path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def ses_production_ready(manifest: dict) -> bool:
    ses = next((p for p in manifest.get("providers") or [] if p.get("id") == "ses"), None)
    return bool(ses and not ses.get("production_pending"))


def operational_resend_limits(manifest: dict) -> tuple[int | None, int | None]:
    """Return (daily_cap, monthly_cap) for operational Resend backup. daily_cap None = no daily limit."""
    pool = manifest.get("operational_pool") or {}
    member = (pool.get("member_limits") or {}).get("resend") or {}
    resend = next((p for p in manifest.get("providers") or [] if p.get("id") == "resend"), None)
    op_tier = (resend or {}).get("operational_tier") or {}
    tier_limits = op_tier.get("limits") or {}
    monthly = member.get("emails_per_month") or tier_limits.get("emails_per_month") or 50_000
    daily = member.get("emails_per_day")
    if daily is None and "emails_per_day" not in member:
        daily = None
    return daily, int(monthly)


def send_via_resend(
    recipients: list[dict[str, str]],
    *,
    html: str,
    subject: str,
    plain: str,
    from_email: str,
    dry_run: bool,
    daily_cap: int | None,
    monthly_cap: int,
) -> int:
    api_key = os.environ.get("RESEND_API_KEY", "").strip()
    if dry_run:
        cap_desc = f"{monthly_cap}/mo" if daily_cap is None else f"{daily_cap}/day · {monthly_cap}/mo"
        print(f"[dry-run] Would send to {len(recipients)} via Resend Pro backup ({cap_desc})")
        return 0
    if not api_key:
        raise SystemExit("RESEND_API_KEY required for send")

    try:
        import resend  # type: ignore
    except ImportError:
        raise SystemExit("Install resend: uv add resend") from None

    resend.api_key = api_key
    sent = 0
    for i, row in enumerate(recipients):
        if daily_cap is not None and i >= daily_cap:
            print(f"Stopped at Resend daily cap ({daily_cap})")
            break
        if sent >= monthly_cap:
            print(f"Stopped at Resend monthly cap ({monthly_cap})")
            break
        email = row["email"]
        first = row.get("first_name") or "there"
        body_html = substitute_merge(html, first, email)
        body_plain = substitute_merge(plain, first, email) if plain else None
        payload: dict = {
            "from": from_email,
            "to": [email],
            "subject": subject,
            "html": body_html,
        }
        if body_plain:
            payload["text"] = body_plain
        resend.Emails.send(payload)
        sent += 1
    print(f"Sent {sent} via Resend (operational backup)")
    return sent


def main() -> None:
    parser = argparse.ArgumentParser(description="Operational email broadcast")
    parser.add_argument("--template", required=True, choices=["legal", "incident"])
    parser.add_argument("--dedup-key", required=True, help="outreach_log dedup key")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--require-ses",
        action="store_true",
        help="Refuse to send unless SES production is approved (no Resend backup)",
    )
    parser.add_argument(
        "--free-tier-resend",
        action="store_true",
        help="Use Resend free-tier caps (100/day) — not for full-list legal/outage",
    )
    parser.add_argument("--contacts", type=Path, default=CONTACTS_CSV)
    args = parser.parse_args()

    manifest = load_manifest()
    seq = sequence_for_template(args.template)
    html, subject, plain = load_html(seq)
    recipients = load_recipients(args.contacts)

    from_email = os.environ.get("FROM_EMAIL", "").strip()
    from_name = os.environ.get("FROM_NAME", "Adam from Oasis").strip()
    if from_email and from_name:
        from_addr = f"{from_name} <{from_email}>"
    elif from_email:
        from_addr = from_email
    else:
        from_addr = "Adam from Oasis <hello@kahana.co>"

    print(f"Template: {args.template} · dedup: {args.dedup_key}")
    ses_ready = ses_production_ready(manifest)
    op_daily, op_monthly = operational_resend_limits(manifest)
    if args.free_tier_resend:
        op_daily, op_monthly = RESEND_FREE_DAILY_CAP, RESEND_FREE_MONTHLY_CAP

    print(f"Recipients: {len(recipients)}")

    if ses_ready and not args.free_tier_resend:
        print("Route: Amazon SES (primary)")
        if args.dry_run:
            print("[dry-run] Would send via SES when send_via_ses() is implemented")
        else:
            raise SystemExit(
                "SES production is approved but send_via_ses() is not implemented yet. "
                "Use --dry-run or send via Resend backup (omit --require-ses)."
            )
        return

    if args.require_ses:
        raise SystemExit(
            "SES is not production-ready (--require-ses). Request AWS production access "
            "or send via Resend Pro backup (default)."
        )

    daily_cap = op_daily
    monthly_cap = op_monthly
    print(
        "Route: Resend Pro backup (SES sandbox / not production-ready) — "
        f"cap: {monthly_cap:,}/mo"
        + (f" · {daily_cap}/day" if daily_cap else " · no daily cap")
    )
    if not args.free_tier_resend and len(recipients) > monthly_cap and not args.dry_run:
        raise SystemExit(
            f"{len(recipients)} recipients exceeds operational monthly cap {monthly_cap}. "
            "Upgrade Resend plan or wait for SES production."
        )

    send_via_resend(
        recipients,
        html=html,
        subject=subject,
        plain=plain,
        from_email=from_addr,
        dry_run=args.dry_run,
        daily_cap=daily_cap,
        monthly_cap=monthly_cap,
    )


if __name__ == "__main__":
    main()
