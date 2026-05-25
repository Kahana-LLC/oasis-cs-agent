# Oasis Brevo email templates

HTML, plain-text, and drag-and-drop specs for Oasis lifecycle and Product Hunt campaigns.

**Live previews:** After deploy, open [`/email-machine`](https://oasis-analytics.vercel.app/email-machine) to see rendered subject lines and HTML for each shipped template (built from this folder at deploy time).

## Folders

| Folder | Contents |
|--------|----------|
| [`lifecycle/`](lifecycle/) | Welcome, activation, limit-hitter, cancelled win-back, NPS, PMF, Paid Zen |
| [`conversion/`](conversion/) | At-risk nurture, dead resurrection, return reinforcement |
| [`enterprise/`](enterprise/) | B2B founder + expansion (HubSpot) |
| [`operational/`](operational/) | Legal/policy + incident notices (Resend / SES) |
| [`ph-waitlist/`](ph-waitlist/) | Product Hunt teaser + launch emails, Zen gift snippets |
| [`shared/`](shared/) | Founder header/signoff, Slack button, support links |

## Start here

| Index | Description |
|-------|-------------|
| [`lifecycle/lifecycle-emails.md`](lifecycle/brevo-oasis-lifecycle-emails.md) | Welcome, NPS, PMF, Zen paid |
| [`ph-waitlist/ph-waitlist-emails.md`](ph-waitlist/brevo-oasis-ph-waitlist-emails.md) | PH teaser + launch |
| [`brevo-oasis-feedback-zen-reward.md`](brevo-oasis-feedback-zen-reward.md) | Survey Zen reward ops |
| [`brevo-oasis-email-links.js`](brevo-oasis-email-links.js) | Canonical URLs |

## Quick paths (full HTML paste)

| Email | File |
|-------|------|
| Welcome | `lifecycle/brevo-oasis-welcome.html` |
| NPS | `lifecycle/brevo-oasis-nps-day3.html` |
| PMF | `lifecycle/brevo-oasis-pmf-day10.html` |
| Paid Zen | `lifecycle/brevo-oasis-paid-zen-welcome.html` |
| PH teaser | `ph-waitlist/brevo-oasis-ph-teaser-waitlist.html` |
| PH launch | `ph-waitlist/brevo-oasis-ph-launch-waitlist.html` |

## Lifecycle expansion + conversion + enterprise

| Touch | File |
|-------|------|
| Activation nudge (D1) | `lifecycle/brevo-oasis-activation-nudge.html` |
| Activation CS / calendar (D3) | `lifecycle/brevo-oasis-activation-cs-calendar.html` |
| Limit-hitter upgrade (D0, D7) | `lifecycle/brevo-oasis-limit-hitter-upgrade.html`, `…-d7.html` |
| At-risk nurture (D0–D21) | `conversion/brevo-oasis-at-risk-nurture-d{0,7,14,21}.html` |
| Dead resurrection (D0, D14) | `conversion/brevo-oasis-dead-resurrection-d0.html`, `…-d14.html` |
| Return reinforcement | `conversion/brevo-oasis-return-reinforcement.html` |
| Cancelled win-back (D0, D14) | `lifecycle/brevo-oasis-cancelled-winback-d0.html`, `…-d14.html` |
| Enterprise founder (D55) | `enterprise/brevo-oasis-enterprise-founder.html` |
| Enterprise expansion (D85) | `enterprise/brevo-oasis-enterprise-expansion.html` |

Regenerate HTML from specs: `python brevo-oasis-emails/generate_missing_templates.py`
