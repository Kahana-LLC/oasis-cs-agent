#!/usr/bin/env python3
"""One-shot generator for missing lifecycle/conversion/enterprise email fragments."""

from __future__ import annotations

from pathlib import Path

from brevo_oasis_email_blocks import (
    CONVERSION_HELP_HTML,
    CONVERSION_HELP_PLAIN,
    DOCS,
    GEIST_STACK,
    BRICOLAGE_STACK,
    INSTALL,
    SLACK,
    CONTACT,
    feedback_checkin_callout_html,
    founder_header_html,
    fonts_preheader_rows_html,
    limit_hitter_learn_more_button_html,
    limit_hitter_plain_paragraphs,
    limit_hitter_training_body_html,
    limit_hitter_upgrade_button_html,
    limit_hitter_zen_footnote_html,
    enterprise_calendar_button_html,
    enterprise_expansion_body_html,
    enterprise_founder_body_html,
    enterprise_plain_paragraphs,
    open_oasis_text_link_html,
    signoff_package_html,
    signoff_package_plain,
)

ROOT = Path(__file__).resolve().parent
BILLING = "https://billing.stripe.com/p/login/bIYg16d6l3FqelieUU"
ADAM = "https://kahana.co/adam-kershner"

CALLOUT_DEFAULT = feedback_checkin_callout_html()


def shell(
    preheader: str,
    title: str,
    body_html: str,
    cta_label: str,
    cta_url: str,
    footer_reason: str,
    help_paragraph: str | None = None,
) -> str:
    cta = ""
    if cta_label and cta_url:
        cta = f"""<table role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin: 0 auto 24px;">
              <tr>
                <td style="border-radius: 28px; background-color: #4A6200; border: 1px solid #7F9E36;">
                  <a href="{cta_url}" target="_blank" rel="noopener noreferrer" style="display: inline-block; padding: 14px 28px; font-size: 16px; font-weight: bold; color: #ffffff; text-decoration: none;">{cta_label}</a>
                </td>
              </tr>
            </table>"""
    return f"""<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: #f0f0f0; padding: 40px 20px; margin: 0; font-family: {GEIST_STACK}; font-size: 16px; line-height: 1.6; color: #4A5745;">
  <tr>
    <td style="display: none; font-size: 1px; line-height: 1px; max-height: 0; max-width: 0; opacity: 0; overflow: hidden; mso-hide: all;">{preheader}</td>
  </tr>
{fonts_preheader_rows_html()}
  <tr>
    <td align="center">
      <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="max-width: 520px; background-color: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 24px rgba(49, 58, 0, 0.08);">
        <tr>
          <td style="background-color: #F8FAF2; padding: 32px 40px 24px; border-bottom: 1px solid #e8ebe0;">
            <p style="margin: 0 0 4px; font-size: 13px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; color: #978455;">Oasis by Kahana</p>
            <h1 style="margin: 0; font-size: 24px; font-weight: 700; color: #313A00; font-family: {BRICOLAGE_STACK}; letter-spacing: -0.02em; line-height: 1.2;">{title}</h1>
          </td>
        </tr>
        <tr>
          <td style="padding: 24px 40px 32px; font-family: {GEIST_STACK};">
{founder_header_html("Hi")}
            {body_html}
            {cta}
{signoff_package_html(help_paragraph)}
          </td>
        </tr>
        <tr>
          <td style="padding: 24px 40px 32px; background-color: #F8FAF2; border-top: 1px solid #e8ebe0; font-family: {GEIST_STACK};">
            <p style="margin: 0 0 12px; font-size: 13px; color: #6b7355;">{footer_reason} <a href="{DOCS}" target="_blank" rel="noopener noreferrer" style="color: #4A6200; font-weight: 600; text-decoration: none;">Docs</a> · <a href="{SLACK}" target="_blank" rel="noopener noreferrer" style="color: #4A6200; font-weight: 600; text-decoration: none;">Slack</a> · <a href="{CONTACT}" style="color: #4A6200; font-weight: 600; text-decoration: none;">Contact</a></p>
            <p style="margin: 0 0 8px; font-size: 13px; color: #6b7355;"><a href="{{{{ mirror }}}}" style="color: #4A6200; font-weight: 600; text-decoration: none;">View in browser</a></p>
            <p style="margin: 0; font-size: 13px; color: #6b7355;"><a href="{{{{ unsubscribe }}}}" style="color: #4A6200; font-weight: 600; text-decoration: none;">Unsubscribe</a> · <a href="https://kahana.co/privacy-policy" style="color: #4A6200; font-weight: 600; text-decoration: none;">Privacy Policy</a></p>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>"""


def plain(
    title: str,
    paragraphs: list[str],
    cta_label: str,
    cta_url: str,
    footer: str,
    help_paragraph: str | None = None,
) -> str:
    help_plain = (
        CONVERSION_HELP_PLAIN if help_paragraph == CONVERSION_HELP_HTML else help_paragraph
    )
    lines = ["Adam Kershner", "Founder, Oasis", "", "Hi {{ contact.FIRSTNAME }},", ""]
    lines.extend(paragraphs)
    if cta_label and cta_url:
        lines.extend(["", f"{cta_label}: {cta_url}"])
    lines.extend(signoff_package_plain(help_plain))
    lines.extend(["", footer, f"Docs: {DOCS}", f"Slack: {SLACK}", f"Contact: {CONTACT}", "View in browser: {{ mirror }}", "Unsubscribe: {{ unsubscribe }}"])
    return "\n".join(lines) + "\n"


TEMPLATES: list[tuple[str, str, str, str, str, str, str, list[str], str, str | None]] = [
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
        None,
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
        None,
    ),
    (
        "lifecycle/brevo-oasis-limit-hitter-upgrade.html",
        "lifecycle/brevo-oasis-limit-hitter-upgrade-plain-text.txt",
        "Anonymous or personalized training in Oasis. Learn how it works.",
        "You hit your daily limit",
        f"""{limit_hitter_training_body_html("d0")}
{limit_hitter_learn_more_button_html()}
{limit_hitter_zen_footnote_html("d0")}
{limit_hitter_upgrade_button_html()}""",
        "",
        "",
        limit_hitter_plain_paragraphs("d0"),
        "You're receiving this because you use Oasis on the free plan.",
        None,
    ),
    (
        "lifecycle/brevo-oasis-limit-hitter-upgrade-d7.html",
        "lifecycle/brevo-oasis-limit-hitter-upgrade-d7-plain-text.txt",
        "Training can add bonus tokens; Zen gives 1M/day if you need more now.",
        "Still hitting your limit?",
        f"""{limit_hitter_training_body_html("d7")}
{limit_hitter_learn_more_button_html()}
{limit_hitter_zen_footnote_html("d7")}
{limit_hitter_upgrade_button_html()}""",
        "",
        "",
        limit_hitter_plain_paragraphs("d7"),
        "You're receiving this because you hit your Oasis daily token limit.",
        None,
    ),
    (
        "conversion/brevo-oasis-at-risk-nurture-d0.html",
        "conversion/brevo-oasis-at-risk-nurture-d0-plain-text.txt",
        "Quick check-in — is Oasis running smoothly for you?",
        "Quick check-in",
        f"""<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">I noticed we have not seen you in Oasis for a day or two and wanted to check in — not to push you back, but to make sure nothing is broken on your side.</p>
            <p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">If something felt off, confusing, or missing, I would really like to know. Honest feedback is how we make Oasis a higher-quality product. If the product is not good enough yet, that is useful signal too.</p>
{CALLOUT_DEFAULT}
{open_oasis_text_link_html()}""",
        "",
        "",
        [
            "I wanted to check in — we have not seen you in Oasis for a day or two.",
            "Is everything running smoothly? If something felt off, confusing, or missing, I would really like to know.",
            "YOUR HONEST TAKE HELPS: Reply to this email with feedback, bugs, or anything that would make Oasis better for you.",
            f"If you are using Oasis today: {INSTALL}",
        ],
        "You're receiving this as an Oasis user.",
        CONVERSION_HELP_HTML,
    ),
    (
        "conversion/brevo-oasis-at-risk-nurture-d7.html",
        "conversion/brevo-oasis-at-risk-nurture-d7-plain-text.txt",
        "Checking in on your Oasis experience",
        "Checking in",
        f"""<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">It has been about a week since you were last active in Oasis. I am checking in to see how your experience has been so far — what is working, what is not, and whether anything got in the way.</p>
            <p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">We are trying to build something genuinely useful. The only way to get there is the honest truth from people who have tried it. If there is something that would make Oasis better for you, please speak up.</p>
{CALLOUT_DEFAULT}
{open_oasis_text_link_html()}""",
        "",
        "",
        [
            "It has been about a week since you were last active in Oasis.",
            "How has your experience been? What is working, what is not?",
            "YOUR HONEST TAKE HELPS: Reply to this email with feedback, bugs, or ideas to improve Oasis.",
            f"If you are using Oasis today: {INSTALL}",
        ],
        "You're receiving this as an Oasis user.",
        CONVERSION_HELP_HTML,
    ),
    (
        "conversion/brevo-oasis-at-risk-nurture-d14.html",
        "conversion/brevo-oasis-at-risk-nurture-d14-plain-text.txt",
        "Honest feedback would help us improve Oasis",
        "Honest feedback helps",
        f"""<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">It has been about two weeks since you were last active in Oasis. I am reaching out because your perspective matters — if Oasis is not fitting your workflow, I want to understand why.</p>
            <p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">Bugs, confusion, missing features, or a competitor that works better: whatever the honest truth is, it helps us prioritize what to fix and build next. No pressure to return — I care most about making the product better.</p>
{CALLOUT_DEFAULT}
{open_oasis_text_link_html()}""",
        "",
        "",
        [
            "It has been about two weeks since you were last active in Oasis.",
            "If Oasis is not fitting your workflow, I want to understand why — bugs, confusion, missing features, or something else.",
            "YOUR HONEST TAKE HELPS: Reply to this email. I read every note.",
            f"If you are using Oasis today: {INSTALL}",
        ],
        "You're receiving this as an Oasis user.",
        CONVERSION_HELP_HTML,
    ),
    (
        "conversion/brevo-oasis-at-risk-nurture-d21.html",
        "conversion/brevo-oasis-at-risk-nurture-d21-plain-text.txt",
        "Last check-in for a while",
        "Last check-in for a while",
        f"""<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">This is my last scheduled check-in for a while. I did not want to go quiet without asking one more time: how has Oasis been for you, and is there anything we should fix or build?</p>
            <p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">Your account is still here if you need it. No pressure either way — but if you have two minutes of honest feedback, it would mean a lot for making Oasis a super high-quality product.</p>
{CALLOUT_DEFAULT}""",
        "",
        "",
        [
            "This is my last scheduled check-in for a while.",
            "How has Oasis been for you? Is there anything we should fix or build?",
            "YOUR HONEST TAKE HELPS: Reply to this email anytime with honest feedback.",
        ],
        "You're receiving this as an Oasis user.",
        CONVERSION_HELP_HTML,
    ),
    (
        "conversion/brevo-oasis-dead-resurrection-d0.html",
        "conversion/brevo-oasis-dead-resurrection-d0-plain-text.txt",
        "Checking in — has Oasis been working for you?",
        "Checking in",
        f"""<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">It has been at least 30 days since you used Oasis. I wanted to check in — we have shipped improvements to the assistant, import, and training, but product quality matters more than a feature list.</p>
            <p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">If you stepped away because something was not good enough, I would genuinely like to hear what happened. Bugs, missing capabilities, or a workflow that did not click — your honest take helps us improve for everyone.</p>
{CALLOUT_DEFAULT}
{open_oasis_text_link_html()}""",
        "",
        "",
        [
            "It has been 30+ days since you used Oasis — checking in, not pushing you back.",
            "If you left because something was not good enough, I would like to hear what happened.",
            "YOUR HONEST TAKE HELPS: Reply to this email with feedback, bugs, or ideas.",
            f"If you want to try Oasis again: {INSTALL}",
        ],
        "You're receiving this because you previously used Oasis.",
        CONVERSION_HELP_HTML,
    ),
    (
        "conversion/brevo-oasis-dead-resurrection-d14.html",
        "conversion/brevo-oasis-dead-resurrection-d14-plain-text.txt",
        "One last check-in from me",
        "One last check-in",
        f"""<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">This is the last email I will send in this series. I did not want to close the loop without saying: if you have a minute of honest feedback about Oasis, it would help us build a better product.</p>
            <p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">If you do not need Oasis anymore, that is completely fine — ignore this. If something almost worked but did not, I would love to know what would have made it better for you.</p>
{CALLOUT_DEFAULT}""",
        "",
        "",
        [
            "Last email in this series — checking in, not inviting you back.",
            "If you have a minute of honest feedback about Oasis, it would help us improve.",
            "YOUR HONEST TAKE HELPS: Reply to this email. No pressure.",
        ],
        "You're receiving this because you previously used Oasis.",
        CONVERSION_HELP_HTML,
    ),
    (
        "conversion/brevo-oasis-return-reinforcement.html",
        "conversion/brevo-oasis-return-reinforcement-plain-text.txt",
        "Glad you are back — how is it going?",
        "How is it going?",
        f"""<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">Good to see you back in Oasis. I wanted to check in and make sure things are running smoothly after your break — not to lecture you on habits, but to hear how the experience feels now.</p>
            <p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">Anything rough, confusing, or broken? If something would make Oasis better for you, please speak up. We are building in the open and your honest truth directly shapes what we fix next.</p>
{CALLOUT_DEFAULT}
{open_oasis_text_link_html()}""",
        "",
        "",
        [
            "Good to see you back in Oasis — checking in on how things are going.",
            "Anything rough, confusing, or broken? What would make Oasis better for you?",
            "YOUR HONEST TAKE HELPS: Reply to this email with feedback.",
            f"Open Oasis: {INSTALL}",
        ],
        "You're receiving this because you returned to Oasis.",
        CONVERSION_HELP_HTML,
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
        None,
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
        None,
    ),
    (
        "enterprise/brevo-oasis-enterprise-founder.html",
        "enterprise/brevo-oasis-enterprise-founder-plain-text.txt",
        "I'd love your honest feedback on your workflow and the product.",
        "Quick question about your Oasis workflow",
        f"""{enterprise_founder_body_html()}
{enterprise_calendar_button_html()}""",
        "",
        "",
        enterprise_plain_paragraphs("founder"),
        "You're receiving this because you use Oasis.",
        None,
    ),
    (
        "enterprise/brevo-oasis-enterprise-expansion.html",
        "enterprise/brevo-oasis-enterprise-expansion-plain-text.txt",
        "Share feedback or book a few minutes on my calendar.",
        "Checking in on your Oasis experience",
        f"""{enterprise_expansion_body_html()}
{enterprise_calendar_button_html()}""",
        "",
        "",
        enterprise_plain_paragraphs("expansion"),
        "You're receiving this because you use Oasis.",
        None,
    ),
]


def main() -> None:
    for html_rel, txt_rel, pre, title, body, cta_l, cta_u, plain_paras, footer, help in TEMPLATES:
        html_path = ROOT / html_rel
        txt_path = ROOT / txt_rel
        html_path.parent.mkdir(parents=True, exist_ok=True)
        html_path.write_text(shell(pre, title, body, cta_l, cta_u, footer, help), encoding="utf-8")
        txt_path.write_text(plain(title, plain_paras, cta_l, cta_u, footer, help), encoding="utf-8")
        print(f"wrote {html_rel}")


if __name__ == "__main__":
    main()
