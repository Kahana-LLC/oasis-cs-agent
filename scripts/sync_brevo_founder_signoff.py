#!/usr/bin/env python3
"""Apply fonts + standard Adam signoff to Brevo HTML templates (excludes welcome + operational)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EMAILS = ROOT / "brevo-oasis-emails"
sys.path.insert(0, str(EMAILS))

from brevo_oasis_email_blocks import (  # noqa: E402
    BRICOLAGE_STACK,
    GEIST_STACK,
    fonts_preheader_rows_html,
    signoff_package_html,
)

SKIP = {
    "lifecycle/brevo-oasis-welcome.html",
    "operational/brevo-oasis-legal-notice.html",
    "operational/brevo-oasis-incident-notice.html",
}

FOLDERS = ("lifecycle", "conversion", "enterprise", "ph-waitlist")

OLD_SIGNOFF_PATTERNS = [
    re.compile(
        r'<p style="margin: 24px 0 16px; font-size: 16px; color: #4A5745;">I&apos;m here if you have questions[^<]*</p>\s*'
        r'<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">(?:Connect with me[^<]*|Reply to this email[^<]*)</p>\s*'
        r'(?:<p style="margin: 0(?: 0 24px)?; font-size: 16px; color: #4A5745;">[^<]*(?:Connect with me|connect with me)[^<]*</p>\s*)?',
        re.DOTALL,
    ),
    re.compile(
        r'<p style="margin: 24px 0 16px; font-size: 16px; color: #4A5745;">I&apos;m here if you have questions, feedback, or just want to talk about Oasis\.</p>\s*'
        r'<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">Connect with me on social media[^<]*</p>\s*'
        r'<p style="margin: 0(?: 0 24px)?; font-size: 16px; color: #4A5745;"><a href="https://kahana\.co/adam-kershner"[^>]*>Connect with me</a></p>',
        re.DOTALL,
    ),
    re.compile(
        r'<p style="margin: 24px 0 16px; font-size: 16px; color: #4A5745;">I&apos;m here if you have questions[^<]*</p>\s*'
        r'<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">Reply to this email or <a href="https://kahana\.co/adam-kershner"[^>]*>connect with me</a>\.</p>',
        re.DOTALL,
    ),
]

PH_OLD_SIGNOFF = re.compile(
    r'<p style="margin: 24px 0 16px; font-size: 16px; color: #4A5745;">I&apos;m hoping you&apos;ll join us[^<]*</p>\s*'
    r'<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">I&apos;ll be very much available[^<]*</p>\s*'
    r'<p style="margin: 0 0 24px; font-size: 16px; color: #4A5745;"><a href="https://kahana\.co/adam-kershner"[^>]*>Connect with me</a></p>',
    re.DOTALL,
)

PH_NEW_SIGNOFF = (EMAILS / "ph-waitlist/brevo-oasis-ph-founder-signoff-snippet.html").read_text(encoding="utf-8")
PH_NEW_SIGNOFF = "\n".join(
    ln for ln in PH_NEW_SIGNOFF.splitlines() if not ln.strip().startswith("<!--")
).strip()


def apply_fonts(html: str) -> str:
    if "@import url('https://fonts.googleapis.com" in html:
        pass
    elif "fonts_preheader" not in html:
        html = html.replace(
            '  <tr>\n    <td style="display: none; font-size: 1px;',
            f"{fonts_preheader_rows_html()}\n  <tr>\n    <td style=\"display: none; font-size: 1px;",
            1,
        )

    html = re.sub(
        r"font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;",
        f"font-family: {GEIST_STACK};",
        html,
    )
    html = re.sub(
        r"font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;",
        f"font-family: {GEIST_STACK};",
        html,
    )
    html = re.sub(
        r'<td style="padding: 24px 40px 32px;">',
        f'<td style="padding: 24px 40px 32px; font-family: {GEIST_STACK};">',
        html,
        count=1,
    )
    html = re.sub(
        r'<h1 style="margin: 0; font-size: 24px; font-weight: 800; color: #313A00; font-family: [^"]*;">',
        f'<h1 style="margin: 0; font-size: 24px; font-weight: 700; color: #313A00; font-family: {BRICOLAGE_STACK}; letter-spacing: -0.02em; line-height: 1.2;">',
        html,
        count=1,
    )
    html = re.sub(
        r'<td style="padding: 24px 40px 32px; background-color: #F8FAF2; border-top: 1px solid #e8ebe0;">',
        f'<td style="padding: 24px 40px 32px; background-color: #F8FAF2; border-top: 1px solid #e8ebe0; font-family: {GEIST_STACK};">',
        html,
        count=1,
    )
    return html


def replace_signoff(html: str, rel: str) -> tuple[str, bool]:
    if "All my socials" in html and "- Adam" in html and "Work hard. Be kind" in html:
        return html, False

    package = signoff_package_html()
    if rel.startswith("ph-waitlist/"):
        if PH_OLD_SIGNOFF.search(html):
            return PH_OLD_SIGNOFF.sub(PH_NEW_SIGNOFF + "\n            ", html), True
        return html, False

    for pat in OLD_SIGNOFF_PATTERNS:
        if pat.search(html):
            return pat.sub(package + "\n            ", html), True

    # Already has partial new signoff from welcome-style but missing blocks
    if "Connect with me" in html and "All my socials" not in html:
        idx = html.find("Connect with me")
        start = html.rfind("<p style=", 0, idx)
        if start > 0:
            end = html.find("</p>", idx) + 4
            block_start = html.rfind('<p style="margin: 24px 0 16px', 0, start)
            if block_start < 0:
                block_start = start
            html = html[:block_start] + package + "\n            " + html[end:]
            return html, True

    return html, False


ORPHAN_CONNECT = re.compile(
    r'\s*<p style="margin: 0; font-size: 16px; color: #4A5745;"><a href="https://kahana\.co/adam-kershner"[^>]*>Connect with me</a></p>',
)


def main() -> None:
    changed = []
    for folder in FOLDERS:
        for path in sorted((EMAILS / folder).glob("brevo-oasis-*.html")):
            rel = f"{folder}/{path.name}"
            if rel in SKIP or "snippet" in path.name:
                continue
            text = path.read_text(encoding="utf-8")
            updated = apply_fonts(text)
            updated, did_sign = replace_signoff(updated, rel)
            if ORPHAN_CONNECT.search(updated):
                updated = ORPHAN_CONNECT.sub("", updated)
                did_sign = True
            if updated != text:
                path.write_text(updated, encoding="utf-8")
                changed.append(rel)
                print(f"updated {rel}" + (" (signoff)" if did_sign else " (fonts)"))

    if not changed:
        print("no changes")
    else:
        print(f"\n{len(changed)} file(s) updated")


if __name__ == "__main__":
    main()
