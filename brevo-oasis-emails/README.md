# Oasis Brevo email templates

HTML, plain-text, and drag-and-drop specs for Oasis lifecycle and Product Hunt campaigns.

**Live previews:** After deploy, open [`/email-machine`](https://oasis-analytics.vercel.app/email-machine) to see rendered subject lines and HTML for each shipped template (built from this folder at deploy time).

## Folders

| Folder | Contents |
|--------|----------|
| [`lifecycle/`](lifecycle/) | Welcome, activation, limit-hitter, cancelled win-back, NPS, PMF, Paid Zen |
| [`conversion/`](conversion/) | At-risk nurture, dead resurrection, return reinforcement |
| [`enterprise/`](enterprise/) | B2B founder + expansion (HubSpot) |
| [`operational/`](operational/) | Legal/policy + incident notices (SES primary) |
| [`ph-waitlist/`](ph-waitlist/) | Product Hunt teaser + launch emails, Zen gift snippets |
| [`shared/`](shared/) | Founder header/signoff, fonts, mantra, socials, Slack button, support links |

## Shared Adam signoff (all Adam-voiced Brevo emails)

Canonical layout from [`lifecycle/brevo-oasis-welcome.html`](lifecycle/brevo-oasis-welcome.html): founder headshot **before** greeting → body → help line → **`- Adam`** → mantra callout → **All my socials** + icon row (no LinkedIn). **Operational** emails (`operational/`) stay company tone without this block.

| Snippet | File |
|---------|------|
| Google Fonts (Geist + Bricolage) | [`shared/brevo-oasis-email-fonts-snippet.html`](shared/brevo-oasis-email-fonts-snippet.html) |
| Founder header + greeting | [`shared/brevo-oasis-lifecycle-founder-header-snippet.html`](shared/brevo-oasis-lifecycle-founder-header-snippet.html) |
| Full signoff package | [`shared/brevo-oasis-founder-signoff-package-snippet.html`](shared/brevo-oasis-founder-signoff-package-snippet.html) |
| `- Adam` only | [`shared/brevo-oasis-founder-adam-sign-snippet.html`](shared/brevo-oasis-founder-adam-sign-snippet.html) |
| Mantra callout | [`shared/brevo-oasis-founder-mantra-snippet.html`](shared/brevo-oasis-founder-mantra-snippet.html) |
| Feedback check-in callout | [`shared/brevo-oasis-feedback-checkin-callout-snippet.html`](shared/brevo-oasis-feedback-checkin-callout-snippet.html) |
| Limit-hitter training block | [`shared/brevo-oasis-limit-hitter-training-snippet.html`](shared/brevo-oasis-limit-hitter-training-snippet.html) |
| Social row | [`shared/brevo-oasis-founder-socials-snippet.html`](shared/brevo-oasis-founder-socials-snippet.html) |

Python helpers: [`brevo_oasis_email_blocks.py`](brevo_oasis_email_blocks.py). Regenerate shell templates: `python brevo-oasis-emails/generate_missing_templates.py`. Roll out HTML/plain signoff: `python3 scripts/sync_brevo_founder_signoff.py` and `python3 scripts/sync_brevo_plaintext_signoff.py`.

## Brevo template names (production)

Exact names for Brevo UI: [`docs/BREVO_NAMING.md`](../docs/BREVO_NAMING.md) (e.g. **Oasis Welcome**, **Oasis Activation Nudge**, list **Oasis Lifecycle**, automation **Oasis Phase 1**).

## Start here

| Index | Description |
|-------|-------------|
| [`lifecycle/lifecycle-emails.md`](lifecycle/brevo-oasis-lifecycle-emails.md) | Welcome, NPS, PMF, Zen paid |
| [`ph-waitlist/ph-waitlist-emails.md`](ph-waitlist/brevo-oasis-ph-waitlist-emails.md) | PH teaser + launch |
| [`conversion/brevo-oasis-conversion-emails.md`](conversion/brevo-oasis-conversion-emails.md) | At-risk, dead resurrection, return reinforcement |
| [`enterprise/brevo-oasis-enterprise-emails.md`](enterprise/brevo-oasis-enterprise-emails.md) | D55/D85 feedback check-ins (HubSpot) |
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
| Limit-hitter (D0, D7) — training-first, Zen footnote | `lifecycle/brevo-oasis-limit-hitter-upgrade.html`, `…-d7.html` · see [`lifecycle/brevo-oasis-lifecycle-emails.md`](lifecycle/brevo-oasis-lifecycle-emails.md#limit-hitter-d0-d7) |
| At-risk nurture (D0–D21) | `conversion/brevo-oasis-at-risk-nurture-d{0,7,14,21}.html` |
| Dead resurrection (D0, D14) | `conversion/brevo-oasis-dead-resurrection-d0.html`, `…-d14.html` |
| Return reinforcement | `conversion/brevo-oasis-return-reinforcement.html` |
| Cancelled win-back (D0, D14) | `lifecycle/brevo-oasis-cancelled-winback-d0.html`, `…-d14.html` |
| Enterprise founder (D55) — individual feedback, Book time CTA | `enterprise/brevo-oasis-enterprise-founder.html` · [`enterprise/brevo-oasis-enterprise-emails.md`](enterprise/brevo-oasis-enterprise-emails.md) |
| Enterprise expansion (D85) | `enterprise/brevo-oasis-enterprise-expansion.html` |

Regenerate conversion/lifecycle shell HTML: `python brevo-oasis-emails/generate_missing_templates.py` (uses `brevo_oasis_email_blocks.py`).
