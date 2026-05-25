#!/usr/bin/env python3
"""List Brevo SMTP (transactional) templates — find numeric id for Oasis Welcome."""

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


def main() -> int:
    _load_env()
    try:
        from integrations.brevo_phase1 import _brevo_client, load_manifest

        client = _brevo_client()
        resp = client.transactional_emails.get_smtp_templates(limit=100, offset=0)
        templates = getattr(resp, "templates", None) or []
        manifest = load_manifest()
        names = {
            t.get("brevo_template")
            for t in (manifest.get("launch_config", {})
                      .get("supabase_lifecycle_email", {})
                      .get("triggers") or [])
            if t.get("brevo_template")
        }
        print(f"{'ID':>8}  {'NAME':<40}  match")
        print("-" * 56)
        for tpl in templates:
            tid = getattr(tpl, "id", None)
            name = (getattr(tpl, "name", None) or getattr(tpl, "subject", None) or "").strip()
            mark = " <-- lifecycle" if name in names else ""
            print(f"{tid:>8}  {name:<40}{mark}")
        print("\nSet in .env, e.g. BREVO_TEMPLATE_ID_WELCOME=<id> for Oasis Welcome")
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
