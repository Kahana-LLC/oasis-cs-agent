#!/usr/bin/env python3
"""Sync plain-text Brevo templates to standard Adam signoff (skip operational)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EMAILS = ROOT / "brevo-oasis-emails"
sys.path.insert(0, str(EMAILS))

from brevo_oasis_email_blocks import (  # noqa: E402
    ADAM_INSTAGRAM,
    ADAM_LINKTREE,
    ADAM_TIKTOK,
    ADAM_TWITTER,
    ADAM_YOUTUBE,
    DEFAULT_HELP_PLAIN,
    MANTRA_PLAIN,
    signoff_package_plain,
)

SKIP_DIRS = {"operational"}

OLD_SIGNOFF = re.compile(
    r"\n(?:I['\u2019]m here if you have questions[^\n]*\n)+"
    r"(?:Connect with me on social media[^\n]*\n)?"
    r"(?:Connect with me: https://kahana\.co/adam-kershner\n)?",
    re.IGNORECASE,
)

DUPLICATE_BEFORE_NEW = re.compile(
    r"I['\u2019]m here if you have questions, feedback, or just want to talk about Oasis\.\n\n"
    r"Connect with me on social media[^\n]+\n\n"
    r"(?=I['\u2019]m here if you have questions, feedback, or just want to talk\. Reply)",
)

OLD_SHORT = re.compile(
    r"\nI['\u2019]m here if you have questions[^\n]*\nConnect with me: https://kahana\.co/adam-kershner\n",
)


def new_block() -> str:
    return "\n".join(signoff_package_plain()) + "\n"


def fix_ph_footer_line(text: str) -> str:
    return text.replace(
        "Connect with me: https://kahana.co/adam-kershner",
        f"All my socials: {ADAM_LINKTREE}",
    )


def process(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    if "Adam Kershner" not in text and "Founder, Oasis" not in text:
        # PH / some files: ensure founder header if missing at top
        if path.name.startswith("brevo-oasis-ph-"):
            pass

    if "Work hard. Be kind" in text and "All my socials:" in text:
        text = fix_ph_footer_line(text)
        if text != original:
            path.write_text(text, encoding="utf-8")
            return True
        return False

    if DUPLICATE_BEFORE_NEW.search(text):
        text = DUPLICATE_BEFORE_NEW.sub("", text)

    for pat in (OLD_SIGNOFF, OLD_SHORT):
        if pat.search(text):
            text = pat.sub(new_block(), text, count=1)
            break
    else:
        # Insert before footer markers
        footer_markers = [
            "\nYou're receiving this",
            "\nQuestions?",
            "\nView in browser:",
            "\nIf the button",
        ]
        insert_at = len(text)
        for m in footer_markers:
            idx = text.find(m)
            if 0 <= idx < insert_at:
                insert_at = idx
        if insert_at < len(text) and "All my socials:" not in text:
            text = text[:insert_at].rstrip() + new_block() + text[insert_at:]

    text = fix_ph_footer_line(text)

    # Normalize duplicate founder blocks at top for files that already have Adam first
    if text.count("Adam Kershner\nFounder, Oasis") > 1:
        parts = text.split("Adam Kershner\nFounder, Oasis\n", 1)
        text = "Adam Kershner\nFounder, Oasis\n" + parts[1]

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = []
    for path in sorted(EMAILS.rglob("*-plain-text.txt")):
        if path.parent.name in SKIP_DIRS:
            continue
        if process(path):
            changed.append(path.relative_to(EMAILS))
    for path in sorted(EMAILS.rglob("*plain-text.txt")):
        if "operational" in path.parts:
            continue
        if path in changed:
            continue
        if process(path):
            changed.append(path.relative_to(EMAILS))
    for rel in changed:
        print(f"updated {rel}")
    if not changed:
        print("no plain-text changes")


if __name__ == "__main__":
    main()
