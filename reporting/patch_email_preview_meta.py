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
        "You hit your daily limit — unlock unlimited AI",
        "Oasis Zen removes the cap ($20/mo, 1M tokens/day).",
    ),
    "limit_hitter_upgrade_d7": (
        "brevo-oasis-emails/lifecycle/brevo-oasis-limit-hitter-upgrade-d7.html",
        "brevo-oasis-emails/lifecycle/brevo-oasis-limit-hitter-upgrade-d7-plain-text.txt",
        "Still on the free plan after hitting your limit?",
        "Reminder: Oasis Zen gives you unlimited daily AI.",
    ),
    "at_risk_nurture_d0": (
        "brevo-oasis-emails/conversion/brevo-oasis-at-risk-nurture-d0.html",
        "brevo-oasis-emails/conversion/brevo-oasis-at-risk-nurture-d0-plain-text.txt",
        "We miss you in Oasis",
        "Come back today — one quick session keeps the habit alive.",
    ),
    "at_risk_nurture_d7": (
        "brevo-oasis-emails/conversion/brevo-oasis-at-risk-nurture-d7.html",
        "brevo-oasis-emails/conversion/brevo-oasis-at-risk-nurture-d7-plain-text.txt",
        "Your Oasis workflow is waiting",
        "Return within seven days to rebuild your daily browser habit.",
    ),
    "at_risk_nurture_d14": (
        "brevo-oasis-emails/conversion/brevo-oasis-at-risk-nurture-d14.html",
        "brevo-oasis-emails/conversion/brevo-oasis-at-risk-nurture-d14-plain-text.txt",
        "Before you drift away from Oasis",
        "Reply if something blocked you — I read every note.",
    ),
    "at_risk_nurture_d21": (
        "brevo-oasis-emails/conversion/brevo-oasis-at-risk-nurture-d21.html",
        "brevo-oasis-emails/conversion/brevo-oasis-at-risk-nurture-d21-plain-text.txt",
        "Still here when you are ready",
        "Last scheduled check-in for a while — your account is still here.",
    ),
    "dead_resurrection_d0": (
        "brevo-oasis-emails/conversion/brevo-oasis-dead-resurrection-d0.html",
        "brevo-oasis-emails/conversion/brevo-oasis-dead-resurrection-d0-plain-text.txt",
        "It has been a while — Oasis has improved",
        "Your account is still active. Try one fresh session.",
    ),
    "dead_resurrection_d14": (
        "brevo-oasis-emails/conversion/brevo-oasis-dead-resurrection-d14.html",
        "brevo-oasis-emails/conversion/brevo-oasis-dead-resurrection-d14-plain-text.txt",
        "One more invite back to Oasis",
        "Privacy-first AI — the door is open when you are ready.",
    ),
    "return_reinforcement_d0": (
        "brevo-oasis-emails/conversion/brevo-oasis-return-reinforcement.html",
        "brevo-oasis-emails/conversion/brevo-oasis-return-reinforcement-plain-text.txt",
        "Welcome back to Oasis",
        "Train the assistant today for 1,000 bonus tokens.",
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
        "Oasis for your team?",
        "Company-email user with strong engagement — let's talk rollout.",
    ),
    "enterprise_expansion_d85": (
        "brevo-oasis-emails/enterprise/brevo-oasis-enterprise-expansion.html",
        "brevo-oasis-emails/enterprise/brevo-oasis-enterprise-expansion-plain-text.txt",
        "Expanding Oasis with your team?",
        "Ready for seats or procurement? Let's set up a short call.",
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
