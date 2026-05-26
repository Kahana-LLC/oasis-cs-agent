#!/usr/bin/env python3
"""Fix NPS/PMF/Paid Zen HTML signoffs after partial sync (remove orphan Connect with me)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EMAILS = ROOT / "brevo-oasis-emails"
sys.path.insert(0, str(EMAILS))

from brevo_oasis_email_blocks import signoff_package_html  # noqa: E402

FILES = [
    "lifecycle/brevo-oasis-nps-day3.html",
    "lifecycle/brevo-oasis-pmf-day10.html",
    "lifecycle/brevo-oasis-paid-zen-welcome.html",
]

START_MARKERS = [
    '<p style="margin: 24px 0 16px; font-size: 16px; color: #4A5745;">I&apos;m here if you have questions',
    '<p style="margin: 24px 0 16px; font-size: 16px; color: #4A5745;">I&apos;m here if you have questions, feedback, or just want to talk about Oasis',
    '                        <p style="margin: 24px 0 16px; font-size: 16px; color: #4A5745;">I&apos;m here if you have questions',
]

END_MARKER = re.compile(
    r'\s*</td>\s*</tr>\s*<tr>\s*<td style="padding: 24px 40px 32px; background-color: #F8FAF2; border-top: 1px solid #e8ebe0',
)


def fix(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    start = -1
    for marker in START_MARKERS:
        idx = text.find(marker)
        if idx >= 0:
            start = idx
            break
    if start < 0:
        return False
    m = END_MARKER.search(text, start)
    if not m:
        return False
    new_text = text[:start] + signoff_package_html() + "\n" + text[m.start() :]
    if new_text == text:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    for rel in FILES:
        p = EMAILS / rel
        if fix(p):
            print(f"fixed {rel}")
        else:
            print(f"skip {rel}")


if __name__ == "__main__":
    main()
