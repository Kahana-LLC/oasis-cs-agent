#!/usr/bin/env python3
"""Send a lifecycle email via Brevo template + cs_outreach_log dedup (welcome first)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _load_env() -> None:
    try:
        from dotenv import load_dotenv

        load_dotenv(ROOT / ".env")
    except ImportError:
        pass


def main() -> int:
    _load_env()
    parser = argparse.ArgumentParser(description="Send lifecycle email (welcome implemented).")
    parser.add_argument(
        "--trigger",
        default="welcome_email",
        help="dedup_trigger_name (default: welcome_email)",
    )
    parser.add_argument("--email", help="Supabase user email")
    parser.add_argument("--user-id", help="Supabase user UUID")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Send even if cs_outreach_log already has this trigger (use carefully)",
    )
    args = parser.parse_args()

    if not args.email and not args.user_id:
        parser.error("Provide --email and/or --user-id")

    try:
        from integrations.lifecycle_email import send_lifecycle_email

        out = send_lifecycle_email(
            trigger_name=args.trigger,
            email=args.email,
            user_id=args.user_id,
            dry_run=args.dry_run,
            force=args.force,
        )
    except (LookupError, ValueError, ImportError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Brevo/Supabase error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(out, indent=2, default=str))
    if out.get("skipped"):
        print("\nAlready sent — use --force to resend or delete row from cs_outreach_log.", file=sys.stderr)
        return 0
    if out.get("dry_run"):
        print("\nDry run OK — remove --dry-run to send.", file=sys.stderr)
        return 0
    if out.get("sent"):
        print(f"\nSent {out.get('trigger_name')} to {out.get('email')}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
