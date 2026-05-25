"""Copy snapshot JSON and email previews into public/ for Vercel static deployment."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from reporting.sync_email_previews import sync_copy_manifest, sync_previews

SRC = ROOT / "reporting" / "baseline_snapshot.json"
DST = ROOT / "public" / "baseline_snapshot.json"
EMAIL_MACHINE_SRC = ROOT / "public" / "email-machine.html"
EMAIL_MACHINE_INDEX = ROOT / "public" / "email-machine" / "index.html"


def sync_email_machine_route() -> None:
    """Mirror vercel.json /email-machine rewrite for plain static servers."""
    if not EMAIL_MACHINE_SRC.exists():
        print(f"Skip email-machine route sync — missing {EMAIL_MACHINE_SRC}", file=sys.stderr)
        return
    EMAIL_MACHINE_INDEX.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EMAIL_MACHINE_SRC, EMAIL_MACHINE_INDEX)
    print(f"Synced email-machine route -> {EMAIL_MACHINE_INDEX}")


def build() -> int:
    if not SRC.exists():
        print(
            f"Missing {SRC}\n"
            "Run locally: .venv/bin/python main.py --baseline",
            file=sys.stderr,
        )
        return 1
    DST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SRC, DST)
    print(f"Copied snapshot -> {DST}")

    try:
        n = sync_previews()
        print(f"Synced {n} email previews -> {ROOT / 'public' / 'emails'}")
        m = sync_copy_manifest()
        print(f"Synced {m} copy sources -> {ROOT / 'public' / 'emails' / 'copy_manifest.json'}")
    except FileNotFoundError as e:
        print(f"Email preview sync failed: {e}", file=sys.stderr)
        return 1

    sync_email_machine_route()

    return 0


if __name__ == "__main__":
    raise SystemExit(build())
