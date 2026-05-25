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
--- Brevo UI: Oasis Phase 1 (production triggers) ---

1. Contact attributes (Boolean): HAS_FIRST_PROMPT, HAS_TRAINING
2. Manual test-send each of the 5 templates (copy QA only — not the funnel test)
3. Automation "Oasis Phase 1":
   Trigger: added to list → Oasis Lifecycle
   Welcome (now) → wait 1d → nudge IF HAS_FIRST_PROMPT false
   → wait to day 3 → CS IF no prompt AND no training → NPS (day 3) → wait 7d → PMF (day 10)
4. Activate, then enroll + verify two cohorts (stuck vs activated)

Enroll:  .venv/bin/python scripts/enroll_brevo_phase1.py --email YOU@gmail.com
Sync:    .venv/bin/python scripts/sync_brevo_contact_attributes.py --email YOU@gmail.com

Full procedure: docs/BREVO_PHASE1_TEST_SETUP.md
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
        err = str(exc)
        print(f"Brevo API failed: {exc}", file=sys.stderr)
        if "unrecognised IP" in err or "authorized_ips" in err:
            print(
                "\nFix: Brevo blocked this machine's IP. Either add your IP at",
                file=sys.stderr,
            )
            print(
                "  https://app.brevo.com/security/authorised_ips",
                file=sys.stderr,
            )
            print(
                "  or use the one-click link in the security email Brevo sent, then re-run verify.",
                file=sys.stderr,
            )
        elif not diag.get("api_key_looks_like_v3"):
            print(
                "\nFix: Brevo → SMTP & API → API keys → create/copy a v3 key (xkeysib-) into BREVO_API_KEY.",
                file=sys.stderr,
            )
        else:
            print(
                "\nFix: check BREVO_API_KEY is active and BREVO_LIFECYCLE_LIST_ID matches Oasis Lifecycle.",
                file=sys.stderr,
            )
        print(
            "Use .venv/bin/python (not system python3). MCP token does not work for these scripts.",
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
