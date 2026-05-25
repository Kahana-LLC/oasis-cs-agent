#!/usr/bin/env python3
"""Sync Oasis product milestones (first prompt, training) to Brevo contact attributes.

Use after a test user activates in Oasis so conditional automation steps see updated flags.

  .venv/bin/python scripts/sync_brevo_contact_attributes.py --email you@example.com
"""

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
    parser = argparse.ArgumentParser(
        description="Sync HAS_FIRST_PROMPT / HAS_TRAINING from Supabase to Brevo."
    )
    parser.add_argument("--email", required=True, help="Contact email in Brevo and Supabase")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    try:
        from integrations.brevo_phase1 import sync_contact_activation_attributes

        out = sync_contact_activation_attributes(email=args.email, dry_run=args.dry_run)
    except (LookupError, ValueError, ImportError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Brevo API error: {exc}", file=sys.stderr)
        return 2

    if out.get("dry_run"):
        print("Dry run — would set Brevo attributes:")
    else:
        print(f"Updated {out['email']}:")
    print(json.dumps(out.get("attributes") or out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
