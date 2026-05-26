# Oasis lifecycle emails (Brevo)

HTML templates for signup, feedback, and paid-plan automations. All four emails use **Adam's founder voice** with headshot before greeting, Slack button, and the shared signoff package (`- Adam`, mantra, **All my socials** + icons). Same design system as Product Hunt waitlist emails in [`brevo-oasis-ph-waitlist-emails.md`](../ph-waitlist/brevo-oasis-ph-waitlist-emails.md).

**From name (all campaigns):** `Adam from Oasis`

## Files

| Email | Brevo template name | Trigger | HTML | Plain text | D&D spec |
|-------|---------------------|---------|------|------------|----------|
| Welcome | Oasis Welcome | On signup | [`brevo-oasis-welcome.html`](brevo-oasis-welcome.html) | [`brevo-oasis-welcome-plain-text.txt`](brevo-oasis-welcome-plain-text.txt) | [`brevo-oasis-welcome-dnd-spec.md`](brevo-oasis-welcome-dnd-spec.md) |
| Activation nudge (24h) | Oasis Activation Nudge | 24h after signup, no first prompt | [`brevo-oasis-activation-nudge.html`](brevo-oasis-activation-nudge.html) | [`brevo-oasis-activation-nudge-plain-text.txt`](brevo-oasis-activation-nudge-plain-text.txt) | [`brevo-oasis-activation-nudge-dnd-spec.md`](brevo-oasis-activation-nudge-dnd-spec.md) |
| NPS (day 3) | Oasis NPS | 3 days after signup | [`brevo-oasis-nps-day3.html`](brevo-oasis-nps-day3.html) | [`brevo-oasis-nps-day3-plain-text.txt`](brevo-oasis-nps-day3-plain-text.txt) | [`brevo-oasis-nps-day3-dnd-spec.md`](brevo-oasis-nps-day3-dnd-spec.md) |
| PMF (day 10) | Oasis PMF | 10 days after signup | [`brevo-oasis-pmf-day10.html`](brevo-oasis-pmf-day10.html) | [`brevo-oasis-pmf-day10-plain-text.txt`](brevo-oasis-pmf-day10-plain-text.txt) | [`brevo-oasis-pmf-day10-dnd-spec.md`](brevo-oasis-pmf-day10-dnd-spec.md) |
| Paid Zen welcome | Oasis Paid Zen Welcome | Zen plan upgrade | [`brevo-oasis-paid-zen-welcome.html`](brevo-oasis-paid-zen-welcome.html) | [`brevo-oasis-paid-zen-welcome-plain-text.txt`](brevo-oasis-paid-zen-welcome-plain-text.txt) | [`brevo-oasis-paid-zen-welcome-dnd-spec.md`](brevo-oasis-paid-zen-welcome-dnd-spec.md) |

## Shared snippets

| File | Purpose |
|------|---------|
| [`brevo-oasis-lifecycle-founder-header-snippet.html`](../shared/brevo-oasis-lifecycle-founder-header-snippet.html) | Adam headshot + Founder, Oasis |
| [`brevo-oasis-founder-signoff-package-snippet.html`](../shared/brevo-oasis-founder-signoff-package-snippet.html) | Help line + `- Adam` + mantra + socials |
| [`brevo-oasis-slack-button-snippet.html`](../shared/brevo-oasis-slack-button-snippet.html) | Purple Join Slack button with icon |
| [`brevo-oasis-support-links-snippet.html`](../shared/brevo-oasis-support-links-snippet.html) | Docs · Slack (icon) · Contact footer row |
| [`brevo-oasis-activation-three-steps-snippet.html`](../shared/brevo-oasis-activation-three-steps-snippet.html) | Activation nudge 3-step checklist |
| [`brevo-oasis-need-help-snippet.html`](../shared/brevo-oasis-need-help-snippet.html) | Compact Help center / Contact / Slack card |
| [`brevo-oasis-email-links.js`](../brevo-oasis-email-links.js) | Canonical URLs (site reference) |

---

## Campaign setup

### Welcome (on signup)

| Field | Value |
|-------|--------|
| Subject | `Welcome to Oasis` |
| Preheader | `Docs, Slack, and support links to get started.` |
| From name | `Adam from Oasis` |
| Trigger | Brevo automation: new Oasis user signup |
| Hero image | `https://kahana.co/images/oasis-browser-assistant-screenshot.png` (desert midnight theme) |

### NPS (day 3)

| Field | Value |
|-------|--------|
| Subject | `Quick question: how likely are you to recommend Oasis?` |
| Preheader | `One question. Your feedback helps us improve.` |
| From name | `Adam from Oasis` |
| Trigger | Brevo automation: 3 days after signup |
| Primary CTA | https://kahana.co/oasis-nps?email={{ contact.EMAIL }} |

### PMF (day 10)

| Field | Value |
|-------|--------|
| Subject | `Quick favor — help us improve Oasis?` |
| Preheader | `Your ideas and honest feedback help us make Oasis better for you.` |
| From name | `Adam from Oasis` |
| Trigger | Brevo automation: 10 days after signup |
| Primary CTA | https://kahana.co/oasis-pmf?email={{ contact.EMAIL }} |

### Paid Zen welcome

| Field | Value |
|-------|--------|
| Subject | `Welcome to Oasis Zen` |
| Preheader | `1M tokens per day and priority support are now active.` |
| From name | `Adam from Oasis` |
| Trigger | Stripe checkout / Brevo when plan = Zen |
| Primary CTA | https://billing.stripe.com/p/login/bIYg16d6l3FqelieUU |

---

## Automation flow

```text
Signup → Welcome (immediate)
       → Wait 3 days → NPS
       → Wait 10 days → PMF
Zen upgrade → Paid Zen welcome (immediate, separate workflow)
Limit hit (free) → Limit Hitter D0 → wait 7 days → Limit Hitter D7 (if still free)
```

### Limit hitter (D0, D7)

Training-first when a free user hits the daily token cap. Concise copy; two green buttons (no open-Oasis line).

| Field | D0 | D7 |
|-------|----|----|
| Brevo template | Oasis Limit Hitter D0 | Oasis Limit Hitter D7 |
| Subject | `You hit your daily limit — training can add bonus tokens` | `Still on the free plan after your limit?` |
| Preheader | `Anonymous or personalized training in Oasis. Learn how it works.` | `Training can add bonus tokens; Zen gives 1M/day if you need more now.` |
| HTML | [`brevo-oasis-limit-hitter-upgrade.html`](brevo-oasis-limit-hitter-upgrade.html) | [`brevo-oasis-limit-hitter-upgrade-d7.html`](brevo-oasis-limit-hitter-upgrade-d7.html) |
| Plain text | `…-upgrade-plain-text.txt` | `…-upgrade-d7-plain-text.txt` |
| Button: Learn more | https://kahana.co/docs/technical-and-interaction-data | same |
| Button: Upgrade Oasis | https://billing.stripe.com/p/login/bIYg16d6l3FqelieUU | same |

Snippet: [`../shared/brevo-oasis-limit-hitter-training-snippet.html`](../shared/brevo-oasis-limit-hitter-training-snippet.html). Regenerate: `python brevo-oasis-emails/generate_missing_templates.py`.

**Brevo re-paste after copy changes:** paste full HTML, update subject/preheader/plain text, test send. From name: `Adam from Oasis`. List: **Oasis Lifecycle**.

Rules:
- Exclude unsubscribed contacts from NPS/PMF
- Paid Zen welcome is independent of the day 3/10 sequence
- Test send each template before enabling automations

---

## Links reference

| Label | URL |
|-------|-----|
| Adam linktree | https://kahana.co/adam-kershner |
| Adam X | https://twitter.com/adam_kershner |
| Adam Instagram | https://www.instagram.com/adam_kershner/ |
| Adam LinkedIn | https://www.linkedin.com/in/adam-kershner/ |
| Adam TikTok | https://www.tiktok.com/@adam_kershner |
| Adam YouTube | https://www.youtube.com/@adam_kershner |
| Adam headshot | https://kahana.co/images/about/adam-kershner.jpg |
| Welcome hero screenshot | https://kahana.co/images/oasis-browser-assistant-screenshot.png |
| Slack icon (button) | https://kahana.co/images/icons/slack-mark-white.png |
| Slack icon (footer) | https://kahana.co/images/icons/slack-mark-purple.png |
| Docs | https://kahana.co/docs |
| Contact | https://kahana.co/contact |
| Join Slack | https://kahanaworkspace.slack.com/archives/C0B3QDPLH4P |
| NPS survey page | https://kahana.co/oasis-nps |
| NPS Tally (email score links) | https://tally.so/r/ODoBz7 |
| PMF survey page | https://kahana.co/oasis-pmf |
| PMF Tally embed | https://tally.so/r/EkNbXX |
| Zen billing portal | https://billing.stripe.com/p/login/bIYg16d6l3FqelieUU |
| Training (technical + interaction data) | https://kahana.co/docs/technical-and-interaction-data |
| Install Mac | https://kahana.co/installations |
| Assistant themes | https://kahana.co/docs/assistant-themes |
| Privacy Policy | https://kahana.co/privacy-policy |

---

## QA checklist

- [ ] Single root `<table>`; no DOCTYPE wrapper
- [ ] No em dashes in copy
- [ ] Adam headshot loads in all four emails
- [ ] Welcome hero screenshot loads (desert midnight theme)
- [ ] Slack button and footer icons load (deploy `public/images/icons/` first)
- [ ] All my socials link and icon row work: `https://kahana.co/adam-kershner`
- [ ] All links open correctly (docs, contact, Slack, Tally, billing)
- [ ] `{{ contact.FIRSTNAME }}`, `{{ mirror }}`, `{{ unsubscribe }}` render in Brevo preview
- [ ] Plain-text tab pasted for each campaign
- [ ] From name set to `Adam from Oasis` in Brevo
- [ ] Mobile preview: buttons and link rows readable
- [ ] Test send completed before enabling automations
