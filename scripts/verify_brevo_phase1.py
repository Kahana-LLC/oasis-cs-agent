#!/usr/bin/env python3
"""Verify Brevo API key, Oasis Lifecycle list id, and print Phase 1 automation checklist."""

from __future__ import annotations

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


CHECKLIST = """
--- Brevo UI: Oasis Phase 1 (do this if not built yet) ---

1. Automation → Create workflow
   Name: Oasis Phase 1
   Trigger: Contact added to list → Oasis Lifecycle
   Status: INACTIVE until template test sends pass

2. Steps (1-minute waits for first test):
   T+0  Send email → template: Oasis Welcome
   Wait 1 minute
   Send email → template: Oasis Activation Nudge
   Wait 1 minute
   Send email → template: Oasis Activation CS Calendar
   Wait 1 minute
   Send email → template: Oasis NPS
   Wait 1 minute
   Send email → template: Oasis PMF

3. Each send step: From name = Adam from Oasis, pick matching template.

4. Manual test: send each template to yourself from Brevo before activating.

5. Activate workflow, then enroll a test user:
   .venv/bin/python scripts/enroll_brevo_phase1.py --email YOUR@gmail.com

6. Re-test: remove contact from list (or delete contact) before re-enrolling.

Production timing (later): Welcome immediate, Nudge D1, CS D2-3, NPS D3, PMF D10.
See docs/BREVO_PHASE1_TEST_SETUP.md
"""


def main() -> int:
    _load_env()
    try:
        from integrations.brevo_phase1 import phase1_config, verify_phase1_setup
    except ImportError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        print("Install: .venv/bin/pip install brevo-python python-dotenv", file=sys.stderr)
        return 1

    from integrations.brevo_phase1 import diagnose_brevo_api_key

    cfg = phase1_config()
    print(f"Phase 1 config: list={cfg.get('list_name')!r}, automation={cfg.get('automation_name')!r}\n")

    diag = diagnose_brevo_api_key()
    print(
        f"API key: set={diag['api_key_set']}, len={diag['api_key_length']}, "
        f"v3_shape={diag['api_key_looks_like_v3']}, mcp_token_also_set={diag['mcp_token_set']}"
    )
    for hint in diag.get("hints") or []:
        print(f"  ! {hint}")
    if diag.get("hints"):
        print()

    try:
        report = verify_phase1_setup()
    except Exception as exc:
        print(f"Brevo API failed: {exc}", file=sys.stderr)
        print(
            "\nFix: Brevo → SMTP & API → API keys → create/copy a v3 key into BREVO_API_KEY in .env.",
            file=sys.stderr,
        )
        print(
            "Use .venv/bin/python (not system python3). MCP token (BREVO_MCP_TOKEN) does not work here.",
            file=sys.stderr,
        )
        return 2

    print("Lists in account:")
    for row in report.get("all_lists") or []:
        mark = " <-- configured" if row["id"] == report["list_id"] else ""
        print(
            f"  {row['id']:>6}  {row['name']}  "
            f"({row.get('total_subscribers', 0)} contacts){mark}"
        )

    if report["ok"]:
        print(
            f"\nOK: BREVO_LIFECYCLE_LIST_ID={report['list_id']} matches "
            f"{report['list_name']!r}"
        )
    else:
        print("\nIssues:")
        for issue in report["issues"]:
            print(f"  - {issue}")
        return 3

    print(CHECKLIST)
    print("Enroll (dry run): .venv/bin/python scripts/enroll_brevo_phase1.py --email you@example.com --dry-run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
