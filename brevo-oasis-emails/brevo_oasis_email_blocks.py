"""Reusable HTML blocks for Oasis Brevo emails (canonical: brevo-oasis-welcome.html)."""

from __future__ import annotations

DOCS = "https://kahana.co/docs"
SLACK = "https://kahanaworkspace.slack.com/archives/C0B3QDPLH4P"
CONTACT = "https://kahana.co/contact"
ADAM_LINKTREE = "https://kahana.co/adam-kershner"
ADAM_TWITTER = "https://twitter.com/adam_kershner"
ADAM_INSTAGRAM = "https://www.instagram.com/adam_kershner/"
ADAM_TIKTOK = "https://www.tiktok.com/@adam_kershner"
ADAM_YOUTUBE = "https://www.youtube.com/@adam_kershner"
HEADSHOT = "https://kahana.co/images/about/adam-kershner.jpg"

GEIST_STACK = (
    "'Geist', 'Segoe UI', system-ui, -apple-system, BlinkMacSystemFont, "
    "Roboto, 'Helvetica Neue', Arial, sans-serif"
)
BRICOLAGE_STACK = (
    "'Bricolage Grotesque', 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
)

DEFAULT_HELP_HTML = (
    "I&apos;m here if you have questions, feedback, or just want to talk. "
    "Reply to this email anytime — my DMs are open on the links below. "
    "I&apos;m here to help :)"
)
DEFAULT_HELP_PLAIN = (
    "I'm here if you have questions, feedback, or just want to talk. "
    "Reply to this email anytime — my DMs are open on the links below. "
    "I'm here to help :)"
)
MANTRA_PLAIN = "Work hard. Be kind. The rest will follow."

CONVERSION_HELP_HTML = (
    "Reply to this email with anything on your mind — bugs, friction, or ideas for what would make "
    "Oasis better for you. I read every note and use it to improve the product."
)
CONVERSION_HELP_PLAIN = (
    "Reply to this email with anything on your mind — bugs, friction, or ideas for what would make "
    "Oasis better for you. I read every note and use it to improve the product."
)
INSTALL = "https://kahana.co/installations"
TRAINING_DOCS = "https://kahana.co/docs/technical-and-interaction-data"
ZEN_BILLING = "https://billing.stripe.com/p/login/bIYg16d6l3FqelieUU"
ADAM_CALENDAR = "https://go.oncehub.com/AdamKershner"

def oasis_green_button_html(label: str, url: str, margin_bottom: str = "20px") -> str:
    return f"""<table role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin: 0 auto {margin_bottom};">
              <tr>
                <td style="border-radius: 28px; background-color: #4A6200; border: 1px solid #7F9E36;">
                  <a href="{url}" target="_blank" rel="noopener noreferrer" style="display: inline-block; padding: 14px 28px; font-size: 16px; font-weight: bold; color: #ffffff; text-decoration: none;">{label}</a>
                </td>
              </tr>
            </table>"""


def limit_hitter_training_body_html(variant: str) -> str:
    if variant == "d7":
        return (
            '<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">'
            "A few days ago you hit your daily token limit. Your cap resets daily, "
            "but you may be hitting it again.</p>\n"
            '<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">'
            "<strong>Anonymous</strong> or <strong>personalized</strong> training can add "
            "<strong>bonus tokens</strong> when your feedback qualifies.</p>"
        )
    return (
        '<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">'
        "You hit your free daily token limit today. That usually means Oasis is working for you.</p>\n"
        '<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">'
        "Train in <strong>anonymous</strong> or <strong>personalized</strong> mode to improve "
        "answers and earn <strong>bonus tokens</strong> on your plan.</p>\n"
        '<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745; line-height: 1.6;">'
        "In Oasis you train in context with tags, notes, and thumbs on replies. "
        "Qualifying training adds bonus tokens; caps follow your plan.</p>"
    )


def limit_hitter_learn_more_button_html() -> str:
    return oasis_green_button_html("Learn more", TRAINING_DOCS)


def limit_hitter_zen_footnote_html(variant: str = "d0") -> str:
    if variant == "d7":
        text = (
            "Need more headroom now? <strong>Oasis Zen</strong> gives you "
            "<strong>1,000,000 tokens per day</strong> ($20/month), with training bonuses on top."
        )
    else:
        text = (
            "Need more commands today? <strong>Oasis Zen</strong> includes "
            "<strong>1,000,000 tokens per day</strong> ($20/month). "
            "You can still train on Zen and earn bonus tokens on top."
        )
    return f'<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745; line-height: 1.6;">{text}</p>'


def limit_hitter_upgrade_button_html() -> str:
    return oasis_green_button_html("Upgrade Oasis", ZEN_BILLING, margin_bottom="24px")


def limit_hitter_plain_paragraphs(variant: str) -> list[str]:
    if variant == "d7":
        body = [
            "A few days ago you hit your daily token limit. Your cap resets daily, "
            "but you may be hitting it again.",
            "Anonymous or personalized training can add bonus tokens when your feedback qualifies.",
        ]
        zen = (
            "Need more headroom now? Oasis Zen gives you 1,000,000 tokens per day ($20/month), "
            "with training bonuses on top."
        )
    else:
        body = [
            "You hit your free daily token limit today. That usually means Oasis is working for you.",
            "Train in anonymous or personalized mode to improve answers and earn bonus tokens on your plan.",
            "In Oasis you train in context with tags, notes, and thumbs on replies. "
            "Qualifying training adds bonus tokens; caps follow your plan.",
        ]
        zen = (
            "Need more commands today? Oasis Zen includes 1,000,000 tokens per day ($20/month). "
            "You can still train on Zen and earn bonus tokens on top."
        )
    return body + [f"Learn more: {TRAINING_DOCS}", zen, f"Upgrade Oasis: {ZEN_BILLING}"]


def enterprise_founder_body_html() -> str:
    return (
        '<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">'
        "You have been getting real use out of Oasis, and I wanted to check in personally.</p>\n"
        '<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745; line-height: 1.6;">'
        "I would love to hear how it fits your day-to-day workflow, what is working, and what we "
        "could do better. Honest feedback is how we improve the product. If a quick chat would "
        "help, grab time on my calendar.</p>"
    )


def enterprise_expansion_body_html() -> str:
    return (
        '<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">'
        "It has been a while since you started using Oasis regularly. How is it going?</p>\n"
        '<p style="margin: 0 0 16px; font-size: 16px; color: #4A5745; line-height: 1.6;">'
        "I am eager to learn more about your use case and anything we could improve. Reply with "
        "feedback anytime, or book a few minutes on my calendar if that is easier.</p>"
    )


def enterprise_calendar_button_html() -> str:
    return oasis_green_button_html("Book time", ADAM_CALENDAR, margin_bottom="24px")


def enterprise_plain_paragraphs(variant: str) -> list[str]:
    if variant == "expansion":
        return [
            "It has been a while since you started using Oasis regularly. How is it going?",
            "I am eager to learn more about your use case and anything we could improve. "
            "Reply with feedback anytime, or book a few minutes on my calendar if that is easier.",
            f"Book time: {ADAM_CALENDAR}",
        ]
    return [
        "You have been getting real use out of Oasis, and I wanted to check in personally.",
        "I would love to hear how it fits your day-to-day workflow, what is working, and what we "
        "could do better. Honest feedback is how we improve the product. "
        "If a quick chat would help, grab time on my calendar.",
        f"Book time: {ADAM_CALENDAR}",
    ]


def feedback_checkin_callout_html(
    lead: str = (
        "<strong>Reply to this email</strong> with feedback, bugs, or anything that would make "
        "Oasis better for you. I read every note. You can also reach us on "
        f'<a href="{SLACK}" target="_blank" rel="noopener noreferrer" style="color: #4A6200; font-weight: 600; text-decoration: underline;">Slack</a> '
        f'or <a href="{CONTACT}" target="_blank" rel="noopener noreferrer" style="color: #4A6200; font-weight: 600; text-decoration: underline;">contact</a>.'
    ),
) -> str:
    return f"""            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="margin: 0 0 20px; border: 2px solid #4A6200; border-radius: 12px; background-color: #F8FAF2; overflow: hidden;">
              <tr>
                <td style="padding: 16px 20px; border-left: 4px solid #4A6200;">
                  <p style="margin: 0 0 8px; font-size: 13px; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; color: #4A6200;">Your honest take helps</p>
                  <p style="margin: 0; font-size: 16px; color: #4A5745; line-height: 1.6;">{lead}</p>
                </td>
              </tr>
            </table>"""


def open_oasis_text_link_html() -> str:
    return (
        f'            <p style="margin: 0 0 16px; font-size: 15px; color: #6b7355; line-height: 1.5;">'
        f'If you are using Oasis today: <a href="{INSTALL}" target="_blank" rel="noopener noreferrer" '
        f'style="color: #4A6200; font-weight: 600; text-decoration: underline;">open Oasis</a>.</p>'
    )


def fonts_preheader_rows_html() -> str:
    return """  <tr>
    <td style="display: none; max-height: 0; overflow: hidden; mso-hide: all;">
      <style type="text/css">
        @import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;600;700;800&family=Geist:wght@400;500;600;700&display=swap');
      </style>
    </td>
  </tr>"""


def founder_header_html(greeting: str = "Hi") -> str:
    return f"""            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="margin: 0 0 12px;">
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
            <p style="margin: 0 0 16px; font-size: 16px; color: #4A5745;">{greeting} {{{{ contact.FIRSTNAME }}}},</p>"""


def signoff_package_html(help_paragraph: str | None = None) -> str:
    help_html = help_paragraph if help_paragraph is not None else DEFAULT_HELP_HTML
    return f"""            <p style="margin: 24px 0 16px; font-size: 16px; color: #4A5745;">{help_html}</p>
            <p style="margin: 0 0 16px; font-family: 'Brush Script MT', 'Segoe Script', 'Apple Chancery', 'Snell Roundhand', cursive; font-size: 26px; font-weight: 700; color: #313A00; line-height: 1.2;">- Adam</p>
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="margin: 0 0 16px; border: 1px solid #e8ebe0; border-radius: 12px; background-color: #F8FAF2;">
              <tr>
                <td align="center" style="padding: 16px 24px;">
                  <p style="margin: 0; font-size: 17px; font-weight: 700; color: #313A00; line-height: 1.45; text-align: center;">Work hard. Be kind. The rest will follow. 🖤</p>
                </td>
              </tr>
            </table>
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="margin: 0 0 28px; border: 1px solid #e8ebe0; border-radius: 12px; background-color: #F8FAF2;">
              <tr>
                <td align="center" style="padding: 18px 20px;">
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center">
                    <tr>
                      <td valign="middle" align="center" style="padding-right: 16px; white-space: nowrap;">
                        <a href="{ADAM_LINKTREE}" target="_blank" rel="noopener noreferrer" style="color: #4A6200; font-size: 15px; font-weight: 700; text-decoration: underline;">All my socials</a>
                      </td>
                      <td valign="middle" style="width: 1px; background-color: #d4d9c8; font-size: 0; line-height: 0;">&nbsp;</td>
                      <td valign="middle" align="center" style="padding-left: 16px;">
                        <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center">
                          <tr>
                            <td style="padding: 0 10px 0 0;">
                              <a href="{ADAM_TWITTER}" target="_blank" rel="noopener noreferrer" title="X (Twitter)" style="text-decoration: none;">
                                <img src="https://cdn.simpleicons.org/x/4A6200" alt="X" width="28" height="28" style="display: block; width: 28px; height: 28px; border: 0; border-radius: 6px;" />
                              </a>
                            </td>
                            <td style="padding: 0 10px 0 0;">
                              <a href="{ADAM_INSTAGRAM}" target="_blank" rel="noopener noreferrer" title="Instagram" style="text-decoration: none;">
                                <img src="https://cdn.simpleicons.org/instagram/4A6200" alt="Instagram" width="28" height="28" style="display: block; width: 28px; height: 28px; border: 0; border-radius: 6px;" />
                              </a>
                            </td>
                            <td style="padding: 0 10px 0 0;">
                              <a href="{ADAM_TIKTOK}" target="_blank" rel="noopener noreferrer" title="TikTok" style="text-decoration: none;">
                                <img src="https://cdn.simpleicons.org/tiktok/4A6200" alt="TikTok" width="28" height="28" style="display: block; width: 28px; height: 28px; border: 0; border-radius: 6px;" />
                              </a>
                            </td>
                            <td style="padding: 0;">
                              <a href="{ADAM_YOUTUBE}" target="_blank" rel="noopener noreferrer" title="YouTube" style="text-decoration: none;">
                                <img src="https://cdn.simpleicons.org/youtube/4A6200" alt="YouTube" width="28" height="28" style="display: block; width: 28px; height: 28px; border: 0; border-radius: 6px;" />
                              </a>
                            </td>
                          </tr>
                        </table>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>"""


def signoff_package_plain(help_paragraph: str | None = None) -> list[str]:
    help_plain = help_paragraph if help_paragraph is not None else DEFAULT_HELP_PLAIN
    return [
        "",
        help_plain,
        "",
        "- Adam",
        "",
        MANTRA_PLAIN,
        "",
        f"All my socials: {ADAM_LINKTREE}",
        f"X: {ADAM_TWITTER}",
        f"Instagram: {ADAM_INSTAGRAM}",
        f"TikTok: {ADAM_TIKTOK}",
        f"YouTube: {ADAM_YOUTUBE}",
    ]
