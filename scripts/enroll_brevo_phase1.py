#!/usr/bin/env python3
"""Enroll an Oasis Supabase user in Brevo Oasis Lifecycle list (Oasis Phase 1 automation).

Run with the project venv (system python3 may lack brevo-python):

  .venv/bin/python scripts/enroll_brevo_phase1.py --list-lists
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
        description="Add Oasis user to Brevo Oasis Lifecycle list (triggers Oasis Phase 1)."
    )
    parser.add_argument("--email", help="Supabase user email")
    parser.add_argument("--user-id", help="Supabase user UUID")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Resolve user and print payload without calling Brevo",
    )
    parser.add_argument(
        "--list-lists",
        action="store_true",
        help="Print Brevo contact lists (to find Oasis Lifecycle list_id)",
    )
    parser.add_argument(
        "--print-config",
        action="store_true",
        help="Print launch_config.brevo_phase1 from manifest",
    )
    args = parser.parse_args()

    if args.print_config:
        from integrations.brevo_phase1 import load_manifest, phase1_config

        print(json.dumps(phase1_config(load_manifest()), indent=2))
        return 0

    if args.list_lists:
        from integrations.brevo_phase1 import list_brevo_lists, phase1_config

        cfg = phase1_config()
        print(f"Looking for list: {cfg.get('list_name')!r}\n")
        for row in list_brevo_lists():
            mark = " <-- lifecycle" if row["name"] == cfg.get("list_name") else ""
            print(f"  {row['id']:>6}  {row['name']}  ({row.get('total_subscribers', 0)} contacts){mark}")
        return 0

    if not args.email and not args.user_id:
        parser.error("Provide --email and/or --user-id (or use --list-lists / --print-config)")

    try:
        from integrations.brevo_phase1 import enroll_user_for_phase1

        out = enroll_user_for_phase1(
            email=args.email,
            user_id=args.user_id,
            dry_run=args.dry_run,
        )
    except (LookupError, ValueError, ImportError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Brevo API error: {exc}", file=sys.stderr)
        return 2

    if out.get("brevo", {}).get("dry_run"):
        print("Dry run — would enroll:")
        print(json.dumps(out, indent=2, default=str))
        return 0

    brevo = out.get("brevo") or {}
    attrs = out.get("activation_attributes") or {}
    print(f"Enrolled {out['email']} (user_id={out['user_id']})")
    print(f"  List: {out.get('list_name')} (id={out['list_id']})")
    print(f"  Automation: {out.get('automation_name')}")
    print(f"  Brevo contact id: {brevo.get('id')}")
    print(
        f"  Attributes: HAS_FIRST_PROMPT={attrs.get('HAS_FIRST_PROMPT')}, "
        f"HAS_TRAINING={attrs.get('HAS_TRAINING')}"
    )
    print(
        "  Production timing: welcome now; nudge ~1d if stuck; CS ~d3 if stuck; NPS ~d3; PMF ~d10."
    )
    print("  After first prompt in Oasis: scripts/sync_brevo_contact_attributes.py --email ...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
