#!/usr/bin/env python3
"""One-shot generator for missing lifecycle/conversion/enterprise email fragments."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = "https://kahana.co/docs"
SLACK = "https://kahanaworkspace.slack.com/archives/C0B3QDPLH4P"
CONTACT = "https://kahana.co/contact"
ADAM = "https://kahana.co/adam-kershner"
BILLING = "https://billing.stripe.com/p/login/bIYg16d6l3FqelieUU"
INSTALL = "https://kahana.co/installations"
HEADSHOT = "https://kahana.co/images/about/adam-kershner.jpg"
SLACK_ICON = "https://a.slack-edge.com/80588/marketing/img/icons/icon_slack_hash_colored.png"
SCREENSHOT = "https://kahana.co/images/oasis-browser-assistant-screenshot.png"


def shell(preheader: str, title: str, body_html: str, cta_label: str, cta_url: str, footer_reason: str) -> str:
    cta = ""
    if cta_label and cta_url:
        cta = f"""<table role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin: 0 auto 24px;">
              <tr>
                <td style="border-radius: 28px; background-color: #4A6200; border: 1px solid #7F9E36;">
                  <a href="{cta_url}" target="_blank" rel="noopener noreferrer" style="display: inline-block; padding: 14px 28px; font-size: 16px; font-weight: bold; color: #ffffff; text-decoration: none;">{cta_label}</a>
                </td>
              </tr>
            </table>"""
    return f"""<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: #f0f0f0; padding: 40px 20px; margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; font-size: 16px; line-height: 1.6; color: #4A5745;">
  <tr>
    <td style="display: none; font-size: 1px; line-height: 1px; max-height: 0; max-width: 0; opacity: 0; overflow: hidden; mso-hide: all;">{preheader}</td>
  </tr>
  <tr>
    <td align="center">
      <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="max-width: 520px; background-color: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 24px rgba(49, 58, 0, 0.08);">
        <tr>
          <td style="background-color: #F8FAF2; padding: 32px 40px 24px; border-bottom: 1px solid #e8ebe0;">
            <p style="margin: 0 0 4px; font-size: 13px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; color: #978455;">Oasis by Kahana</p>
            <h1 style="margin: 0; font-size: 24px; font-weight: 800; color: #313A00; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">{title}</h1>
          </td>
        </tr>
        <tr>
          <td style="padding: 24px 40px 32px;">
            <p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">Hi {{{{ contact.FIRSTNAME }}}},</p>
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="margin: 0 0 16px;">
              <tr>
                <td width="56" valign="top" style="padding-right: 12px;">
                  <img src="{HEADSHOT}" alt="Adam Kershner" width="56" height="56" style="display: block; width: 56px; height: 56px; border-radius: 50%; object-fit: cover;" />
                </td>
                <td valign="middle">
                  <p style="margin: 0; font-size: 15px; font-weight: 700; color: #313A00; line-height: 1.3;">Adam Kershner</p>
                  <p style="margin: 2px 0 0; font-size: 13px; color: #6b7355; line-height: 1.3;">Founder, Oasis</p>
                </td>
              </tr>
            </table>
            {body_html}
            {cta}
            <p style="margin: 24px 0 16px; font-size: 16px; color: #4A5745;">I&apos;m here if you have questions, feedback, or just want to talk about Oasis.</p>
            <p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">Reply to this email or <a href="{ADAM}" target="_blank" rel="noopener noreferrer" style="color: #4A6200; font-weight: 600; text-decoration: underline;">connect with me</a>.</p>
          </td>
        </tr>
        <tr>
          <td style="padding: 24px 40px 32px; background-color: #F8FAF2; border-top: 1px solid #e8ebe0;">
            <p style="margin: 0 0 12px; font-size: 13px; color: #6b7355;">{footer_reason} <a href="{DOCS}" target="_blank" rel="noopener noreferrer" style="color: #4A6200; font-weight: 600; text-decoration: none;">Docs</a> · <a href="{SLACK}" target="_blank" rel="noopener noreferrer" style="color: #4A6200; font-weight: 600; text-decoration: none;">Slack</a> · <a href="{CONTACT}" style="color: #4A6200; font-weight: 600; text-decoration: none;">Contact</a></p>
            <p style="margin: 0 0 8px; font-size: 13px; color: #6b7355;"><a href="{{{{ mirror }}}}" style="color: #4A6200; font-weight: 600; text-decoration: none;">View in browser</a></p>
            <p style="margin: 0; font-size: 13px; color: #6b7355;"><a href="{{{{ unsubscribe }}}}" style="color: #4A6200; font-weight: 600; text-decoration: none;">Unsubscribe</a> · <a href="https://kahana.co/privacy-policy" style="color: #4A6200; font-weight: 600; text-decoration: none;">Privacy Policy</a></p>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>"""


def plain(title: str, paragraphs: list[str], cta_label: str, cta_url: str, footer: str) -> str:
    lines = ["Hi {{ contact.FIRSTNAME }},", "", "Adam Kershner", "Founder, Oasis", ""]
    lines.extend(paragraphs)
    if cta_label and cta_url:
        lines.extend(["", f"{cta_label}: {cta_url}"])
    lines.extend(["", "I'm here if you have questions.", f"Connect with me: {ADAM}", "", footer, f"Docs: {DOCS}", f"Slack: {SLACK}", f"Contact: {CONTACT}", "View in browser: {{ mirror }}", "Unsubscribe: {{ unsubscribe }}"])
    return "\n".join(lines) + "\n"


TEMPLATES: list[tuple[str, str, str, str, str, str, str, list[str], str, str]] = [
    (
        "lifecycle/brevo-oasis-activation-nudge.html",
        "lifecycle/brevo-oasis-activation-nudge-plain-text.txt",
        "Try your first AI command in Oasis — import from your old browser",
        "Try your first AI command",
        """<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">You signed up for Oasis but have not sent your first AI command yet. The fastest win: import bookmarks and history from Chrome, Safari, Brave, or Edge, then ask the assistant anything.</p>
            <p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">Oasis is a privacy-first browser you can train. Your data stays on your device until you choose to share.</p>""",
        "Open Oasis",
        INSTALL,
        ["You signed up but have not sent your first AI command yet.", "Import from Chrome, Safari, Brave, or Edge, then try the assistant.", f"Open Oasis: {INSTALL}"],
        "You're receiving this because you signed up for Oasis.",
    ),
    (
        "lifecycle/brevo-oasis-activation-cs-calendar.html",
        "lifecycle/brevo-oasis-activation-cs-calendar-plain-text.txt",
        "Need help getting started? Book time with me",
        "Let us get you unstuck",
        """<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">I noticed you have not had a chance to run your first AI command in Oasis yet. I would love to help you get set up — import from your prior browser, run a prompt, or train the assistant (you earn <strong>1,000 bonus tokens</strong> when you train).</p>
            <p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">If a quick call would help, grab time on my calendar and I will walk you through it live.</p>""",
        "Book a call",
        ADAM,
        ["I would love to help you get started with Oasis.", "Train the assistant to earn 1,000 bonus tokens.", f"Book time: {ADAM}"],
        "You're receiving this because you signed up for Oasis.",
    ),
    (
        "lifecycle/brevo-oasis-limit-hitter-upgrade.html",
        "lifecycle/brevo-oasis-limit-hitter-upgrade-plain-text.txt",
        "You hit your daily limit — unlock unlimited AI with Oasis Zen",
        "You hit your daily limit",
        """<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">You have been getting real value from Oasis — you hit your free daily token limit today. That is a great sign you are onboarded and activated.</p>
            <p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;"><strong>Oasis Zen</strong> ($20/month) removes the daily cap with <strong>1,000,000 tokens per day</strong>, priority support, and the full privacy-first experience without interruptions.</p>""",
        "Upgrade to Oasis Zen",
        BILLING,
        ["You hit your free daily token limit.", "Oasis Zen gives you 1M tokens/day for $20/month.", f"Upgrade: {BILLING}"],
        "You're receiving this because you use Oasis on the free plan.",
    ),
    (
        "lifecycle/brevo-oasis-limit-hitter-upgrade-d7.html",
        "lifecycle/brevo-oasis-limit-hitter-upgrade-d7-plain-text.txt",
        "Still on the free plan? Your limit resets daily",
        "Reminder: unlimited AI",
        """<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">A few days ago you hit your daily token limit on Oasis. If you are still on the free plan, you may be bumping into the cap again.</p>
            <p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">Upgrade to <strong>Oasis Zen</strong> for unlimited daily AI ($20/month) — same browser you already know, without stopping mid-flow.</p>""",
        "View Oasis Zen",
        BILLING,
        ["Reminder: you hit your daily limit recently.", "Oasis Zen removes the cap.", f"Upgrade: {BILLING}"],
        "You're receiving this because you hit your Oasis daily token limit.",
    ),
    (
        "conversion/brevo-oasis-at-risk-nurture-d0.html",
        "conversion/brevo-oasis-at-risk-nurture-d0-plain-text.txt",
        "We miss you in Oasis — come back today",
        "We miss you in Oasis",
        """<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">You were active on Oasis recently, but we have not seen you in the last day or two. A quick session is enough to pick up where you left off.</p>
            <p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">Open Oasis, run one AI command, or train the assistant — small steps keep your workflow in Oasis instead of falling back to your old browser.</p>""",
        "Open Oasis",
        INSTALL,
        ["We have not seen you in Oasis recently.", "One quick session keeps your habit alive.", f"Open Oasis: {INSTALL}"],
        "You're receiving this as an Oasis user.",
    ),
    (
        "conversion/brevo-oasis-at-risk-nurture-d7.html",
        "conversion/brevo-oasis-at-risk-nurture-d7-plain-text.txt",
        "Your Oasis workflow is waiting",
        "Your workflow is waiting",
        """<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">It has been about a week since you were last active in Oasis. Users who return within seven days are far more likely to make Oasis their daily browser.</p>
            <p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">Try one focused task today: research in the assistant, import a tab set from Chrome or Safari, or finish something you started last week.</p>""",
        "Return to Oasis",
        INSTALL,
        ["Return within seven days to rebuild the habit.", f"Open Oasis: {INSTALL}"],
        "You're receiving this as an Oasis user.",
    ),
    (
        "conversion/brevo-oasis-at-risk-nurture-d14.html",
        "conversion/brevo-oasis-at-risk-nurture-d14-plain-text.txt",
        "Before you drift away from Oasis",
        "Before you drift away",
        """<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">Two weeks without Oasis usually means the old browser wins by default. I would hate to lose you before you have seen what a trained, privacy-first assistant can do daily.</p>
            <p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">Reply to this email if something blocked you — bugs, confusion, or missing features. I read every note.</p>""",
        "Give Oasis another try",
        INSTALL,
        ["Two weeks away makes churn likely.", "Reply if something blocked you.", f"Open Oasis: {INSTALL}"],
        "You're receiving this as an Oasis user.",
    ),
    (
        "conversion/brevo-oasis-at-risk-nurture-d21.html",
        "conversion/brevo-oasis-at-risk-nurture-d21-plain-text.txt",
        "Last nudge: still here when you are ready",
        "Still here when you are ready",
        """<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">This is my last scheduled check-in for a while. Your Oasis account is still here — same privacy-first browser, same assistant you can train.</p>
            <p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">Whenever you are ready, open Oasis for one task. No pressure — just an open door.</p>""",
        "Open Oasis",
        INSTALL,
        ["Last nurture check-in for a while.", f"Open Oasis: {INSTALL}"],
        "You're receiving this as an Oasis user.",
    ),
    (
        "conversion/brevo-oasis-dead-resurrection-d0.html",
        "conversion/brevo-oasis-dead-resurrection-d0-plain-text.txt",
        "It has been a while — Oasis has improved",
        "Oasis has improved",
        """<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">It has been at least 30 days since you used Oasis. We have shipped improvements to the assistant, browser import, and training rewards (<strong>1,000 tokens</strong> when you train).</p>
            <p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">Your account is still active. Give Oasis one fresh try — import from your current browser and run a single command.</p>""",
        "Try Oasis again",
        INSTALL,
        ["It has been 30+ days since you used Oasis.", "Train the assistant for 1,000 bonus tokens.", f"Try again: {INSTALL}"],
        "You're receiving this because you previously used Oasis.",
    ),
    (
        "conversion/brevo-oasis-dead-resurrection-d14.html",
        "conversion/brevo-oasis-dead-resurrection-d14-plain-text.txt",
        "One more invite back to Oasis",
        "One more invite back",
        """<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">I am sending one more note in case timing was the issue. Oasis is built for people who want AI without giving up privacy — your data stays local until you choose otherwise.</p>
            <p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">If you do not need Oasis anymore, you can ignore this. If you want to see what is new, the door is open.</p>""",
        "See what is new",
        INSTALL,
        ["Final resurrection email in this series.", f"See what is new: {INSTALL}"],
        "You're receiving this because you previously used Oasis.",
    ),
    (
        "conversion/brevo-oasis-return-reinforcement.html",
        "conversion/brevo-oasis-return-reinforcement-plain-text.txt",
        "Welcome back to Oasis",
        "Welcome back",
        """<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">Good to see you back in Oasis. Picking up after a break is easier than starting from scratch — your trained assistant and imports are still here.</p>
            <p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">One high-value move today: run a research task in the assistant, or train it on a new workflow so it earns you <strong>1,000 bonus tokens</strong>.</p>""",
        "Continue in Oasis",
        INSTALL,
        ["Welcome back to Oasis.", "Train the assistant for 1,000 bonus tokens.", f"Continue: {INSTALL}"],
        "You're receiving this because you returned to Oasis.",
    ),
    (
        "lifecycle/brevo-oasis-cancelled-winback-d0.html",
        "lifecycle/brevo-oasis-cancelled-winback-d0-plain-text.txt",
        "Sorry to see you cancel Oasis Zen",
        "Sorry to see you go",
        """<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">Your Oasis Zen subscription has ended. I am sorry to see you go — if something was missing or broken, I want to hear about it.</p>
            <p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">You can keep using Oasis on the free plan. If you change your mind, you can reactivate Zen anytime from the billing portal.</p>""",
        "Reactivate Oasis Zen",
        BILLING,
        ["Your Zen subscription ended.", "You can reactivate anytime.", f"Billing portal: {BILLING}"],
        "You're receiving this because you had an Oasis Zen subscription.",
    ),
    (
        "lifecycle/brevo-oasis-cancelled-winback-d14.html",
        "lifecycle/brevo-oasis-cancelled-winback-d14-plain-text.txt",
        "Reconsider Oasis Zen?",
        "Reconsider Oasis Zen?",
        """<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">It has been two weeks since you cancelled Oasis Zen. If daily token limits on the free plan are getting in your way again, Zen is still available — <strong>1M tokens per day</strong> and priority support for $20/month.</p>
            <p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">Reply if price, features, or support was the blocker. I read every message.</p>""",
        "Reactivate Zen",
        BILLING,
        ["Follow-up after cancellation.", f"Reactivate: {BILLING}"],
        "You're receiving this because you cancelled Oasis Zen.",
    ),
    (
        "enterprise/brevo-oasis-enterprise-founder.html",
        "enterprise/brevo-oasis-enterprise-founder-plain-text.txt",
        "Oasis for your team — founder outreach",
        "Oasis for your team",
        """<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">You are using a company email with Oasis and have been actively exploring the product. I would love to learn how your team works today and whether a privacy-first AI browser fits your workflow.</p>
            <p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">If you are evaluating tools for your org, reply with your goals — security, deployment, or team rollout — and I will share what we can do on Zen and enterprise terms.</p>""",
        "Reply to discuss",
        f"mailto:hello@kahana.co",
        ["Company email user with strong engagement.", "Reply to discuss team rollout.", "Contact: hello@kahana.co"],
        "You're receiving this because you use Oasis with a company email.",
    ),
    (
        "enterprise/brevo-oasis-enterprise-expansion.html",
        "enterprise/brevo-oasis-enterprise-expansion-plain-text.txt",
        "Expanding Oasis with your team?",
        "Expanding with your team?",
        """<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">You have been using Oasis consistently on a company email. Teams that standardize on Oasis typically care about privacy, trainable assistants, and controlled AI spend.</p>
            <p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">If you are ready to expand seats or discuss procurement, I would be glad to set up a short call or send a one-pager for your stakeholders.</p>""",
        "Let's talk expansion",
        ADAM,
        ["Follow-up for engaged company-email users.", f"Book time: {ADAM}"],
        "You're receiving this because you use Oasis with a company email.",
    ),
]


def main() -> None:
    for html_rel, txt_rel, pre, title, body, cta_l, cta_u, plain_paras, footer in TEMPLATES:
        html_path = ROOT / html_rel
        txt_path = ROOT / txt_rel
        html_path.parent.mkdir(parents=True, exist_ok=True)
        html_path.write_text(shell(pre, title, body, cta_l, cta_u, footer), encoding="utf-8")
        txt_path.write_text(plain(title, plain_paras, cta_l, cta_u, footer), encoding="utf-8")
        print(f"wrote {html_rel}")


if __name__ == "__main__":
    main()
