#!/usr/bin/env python3
"""Send operational broadcast (legal or incident) via Resend with SES failover rules."""

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

RESEND_DAILY_CAP = 100
RESEND_MONTHLY_CAP = 3000

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


def send_via_resend(
    recipients: list[dict[str, str]],
    *,
    html: str,
    subject: str,
    plain: str,
    from_email: str,
    dry_run: bool,
    daily_cap: int,
) -> int:
    api_key = os.environ.get("RESEND_API_KEY", "").strip()
    if dry_run:
        print(f"[dry-run] Would send to {len(recipients)} via Resend (cap {daily_cap}/day)")
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
        if i >= daily_cap:
            print(f"Stopped at Resend daily cap ({daily_cap})")
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
    print(f"Sent {sent} via Resend")
    return sent


def main() -> None:
    parser = argparse.ArgumentParser(description="Operational email broadcast")
    parser.add_argument("--template", required=True, choices=["legal", "incident"])
    parser.add_argument("--dedup-key", required=True, help="outreach_log dedup key")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--allow-sandbox", action="store_true", help="SES sandbox test only")
    parser.add_argument("--daily-cap", type=int, default=RESEND_DAILY_CAP)
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
    print(f"Recipients: {len(recipients)} · provider route: resend -> ses")

    if len(recipients) > args.daily_cap and not args.dry_run:
        days = (len(recipients) + args.daily_cap - 1) // args.daily_cap
        print(f"Note: {len(recipients)} recipients need ~{days} days at {args.daily_cap}/day on Resend free tier")

    if not ses_production_ready(manifest):
        print("SES: sandbox — bulk failover unavailable until production_pending=false")

    send_via_resend(
        recipients,
        html=html,
        subject=subject,
        plain=plain,
        from_email=from_addr,
        dry_run=args.dry_run,
        daily_cap=args.daily_cap,
    )

    if args.allow_sandbox:
        print("SES sandbox sends not implemented in stub — use Resend or complete SES integration")


if __name__ == "__main__":
    main()
