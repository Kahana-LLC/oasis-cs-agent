#!/usr/bin/env python3
"""Add preview metadata to sequences missing templates in email_sequences.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "public" / "email_sequences.json"

FROM_NAME = "Adam from Oasis"

# touch_id -> (html rel, plain rel, subject, preheader)
TOUCH_PREVIEWS: dict[str, tuple[str, str, str, str]] = {
    "activation_nudge_d1": (
        "brevo-oasis-emails/lifecycle/brevo-oasis-activation-nudge.html",
        "brevo-oasis-emails/lifecycle/brevo-oasis-activation-nudge-plain-text.txt",
        "Try your first AI command in Oasis",
        "Import from Chrome, Safari, Brave, or Edge — then ask the assistant anything.",
    ),
    "activation_cs_calendar_d3": (
        "brevo-oasis-emails/lifecycle/brevo-oasis-activation-cs-calendar.html",
        "brevo-oasis-emails/lifecycle/brevo-oasis-activation-cs-calendar-plain-text.txt",
        "Need help getting started with Oasis?",
        "Book time with me — train the assistant for 1,000 bonus tokens.",
    ),
    "limit_hitter_upgrade_d0": (
        "brevo-oasis-emails/lifecycle/brevo-oasis-limit-hitter-upgrade.html",
        "brevo-oasis-emails/lifecycle/brevo-oasis-limit-hitter-upgrade-plain-text.txt",
        "You hit your daily limit — training can add bonus tokens",
        "Anonymous or personalized training in Oasis. Learn how it works.",
    ),
    "limit_hitter_upgrade_d7": (
        "brevo-oasis-emails/lifecycle/brevo-oasis-limit-hitter-upgrade-d7.html",
        "brevo-oasis-emails/lifecycle/brevo-oasis-limit-hitter-upgrade-d7-plain-text.txt",
        "Still on the free plan after your limit?",
        "Training can add bonus tokens; Zen gives 1M/day if you need more now.",
    ),
    "at_risk_nurture_d0": (
        "brevo-oasis-emails/conversion/brevo-oasis-at-risk-nurture-d0.html",
        "brevo-oasis-emails/conversion/brevo-oasis-at-risk-nurture-d0-plain-text.txt",
        "Quick check-in: how is Oasis going?",
        "Making sure nothing is broken on your side — honest feedback welcome.",
    ),
    "at_risk_nurture_d7": (
        "brevo-oasis-emails/conversion/brevo-oasis-at-risk-nurture-d7.html",
        "brevo-oasis-emails/conversion/brevo-oasis-at-risk-nurture-d7-plain-text.txt",
        "Checking in on your Oasis experience",
        "What is working, what is not — your honest take helps us improve.",
    ),
    "at_risk_nurture_d14": (
        "brevo-oasis-emails/conversion/brevo-oasis-at-risk-nurture-d14.html",
        "brevo-oasis-emails/conversion/brevo-oasis-at-risk-nurture-d14-plain-text.txt",
        "Honest feedback would help us improve Oasis",
        "No pressure to return — I want to understand what would make Oasis better for you.",
    ),
    "at_risk_nurture_d21": (
        "brevo-oasis-emails/conversion/brevo-oasis-at-risk-nurture-d21.html",
        "brevo-oasis-emails/conversion/brevo-oasis-at-risk-nurture-d21-plain-text.txt",
        "Last check-in for a while",
        "If you have two minutes of honest feedback, it would mean a lot.",
    ),
    "dead_resurrection_d0": (
        "brevo-oasis-emails/conversion/brevo-oasis-dead-resurrection-d0.html",
        "brevo-oasis-emails/conversion/brevo-oasis-dead-resurrection-d0-plain-text.txt",
        "Checking in — has Oasis been working for you?",
        "If you left because something was not good enough, I would like to hear what happened.",
    ),
    "dead_resurrection_d14": (
        "brevo-oasis-emails/conversion/brevo-oasis-dead-resurrection-d14.html",
        "brevo-oasis-emails/conversion/brevo-oasis-dead-resurrection-d14-plain-text.txt",
        "One last check-in from me",
        "A minute of honest feedback helps us build a better product.",
    ),
    "return_reinforcement_d0": (
        "brevo-oasis-emails/conversion/brevo-oasis-return-reinforcement.html",
        "brevo-oasis-emails/conversion/brevo-oasis-return-reinforcement-plain-text.txt",
        "Glad you are back — how is it going?",
        "Checking in to make sure things are running smoothly after your break.",
    ),
    "cancelled_winback_d0": (
        "brevo-oasis-emails/lifecycle/brevo-oasis-cancelled-winback-d0.html",
        "brevo-oasis-emails/lifecycle/brevo-oasis-cancelled-winback-d0-plain-text.txt",
        "Sorry to see you cancel Oasis Zen",
        "You can keep using Oasis free or reactivate Zen anytime.",
    ),
    "cancelled_winback_d14": (
        "brevo-oasis-emails/lifecycle/brevo-oasis-cancelled-winback-d14.html",
        "brevo-oasis-emails/lifecycle/brevo-oasis-cancelled-winback-d14-plain-text.txt",
        "Reconsider Oasis Zen?",
        "1M tokens per day — reply if price or features was the blocker.",
    ),
    "enterprise_founder_d55": (
        "brevo-oasis-emails/enterprise/brevo-oasis-enterprise-founder.html",
        "brevo-oasis-emails/enterprise/brevo-oasis-enterprise-founder-plain-text.txt",
        "How is Oasis working for you?",
        "I'd love your honest feedback on your workflow and the product.",
    ),
    "enterprise_expansion_d85": (
        "brevo-oasis-emails/enterprise/brevo-oasis-enterprise-expansion.html",
        "brevo-oasis-emails/enterprise/brevo-oasis-enterprise-expansion-plain-text.txt",
        "Quick check-in: your Oasis experience",
        "Share feedback or book a few minutes on my calendar.",
    ),
}


def preview_obj(
    touch_id: str,
    html_rel: str,
    plain_rel: str,
    subject: str,
    preheader: str,
    deploy_provider: str,
) -> dict:
    return {
        "source": html_rel,
        "path": f"/emails/{touch_id}.html",
        "subject": subject,
        "preheader": preheader,
        "from_name": FROM_NAME,
        "plain_text_source": plain_rel,
        "deploy_provider": deploy_provider,
    }


def deploy_provider_for_seq(seq: dict) -> str:
    return str(seq.get("provider_id") or seq.get("provider_id") or "")


def main() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for seq in data.get("sequences") or []:
        provider = deploy_provider_for_seq(seq)
        touches = seq.get("touches") or []
        first_touch_preview = None
        for touch in touches:
            tid = touch.get("touch_id")
            if tid not in TOUCH_PREVIEWS:
                continue
            html_rel, plain_rel, subject, preheader = TOUCH_PREVIEWS[tid]
            pv = preview_obj(tid, html_rel, plain_rel, subject, preheader, provider)
            touch["preview"] = pv
            if first_touch_preview is None:
                first_touch_preview = pv
        if first_touch_preview:
            seq["preview"] = dict(first_touch_preview)
    MANIFEST.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"patched {MANIFEST}")


if __name__ == "__main__":
    main()
