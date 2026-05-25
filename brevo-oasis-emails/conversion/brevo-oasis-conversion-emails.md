# Oasis conversion emails (Brevo / EmailOctopus)

Phase 2 conversion sequences: **at-risk nurture**, **dead resurrection**, and **return reinforcement**. All use Adam's founder voice (headshot, signoff package).

**Tone:** Founder **check-in**, not win-back. Goal is product quality — honest feedback, bugs, friction, and "what would make Oasis better for you?" Silence may mean the product is not good enough yet; that signal helps us improve.

## Voice

| Do | Avoid |
|----|--------|
| Check in ("how are things going?", "is anything broken?") | "We miss you", "come back", "nudge" |
| Ask for honest experience and improvements | Habit homework, "daily browser", churn guilt |
| **Reply to this email** as primary action | Pushy resurrection CTAs |
| Optional text link to [installations](https://kahana.co/installations) | Large green "Return to Oasis" as hero CTA |

Shared feedback callout: [`../shared/brevo-oasis-feedback-checkin-callout-snippet.html`](../shared/brevo-oasis-feedback-checkin-callout-snippet.html)

## Templates

| Brevo name | Touch | HTML |
|------------|-------|------|
| Oasis At-risk D0 | at_risk_nurture_d0 | [`brevo-oasis-at-risk-nurture-d0.html`](brevo-oasis-at-risk-nurture-d0.html) |
| Oasis At-risk D7 | at_risk_nurture_d7 | [`brevo-oasis-at-risk-nurture-d7.html`](brevo-oasis-at-risk-nurture-d7.html) |
| Oasis At-risk D14 | at_risk_nurture_d14 | [`brevo-oasis-at-risk-nurture-d14.html`](brevo-oasis-at-risk-nurture-d14.html) |
| Oasis At-risk D21 | at_risk_nurture_d21 | [`brevo-oasis-at-risk-nurture-d21.html`](brevo-oasis-at-risk-nurture-d21.html) |
| Oasis Dead Resurrection D0 | dead_resurrection_d0 | [`brevo-oasis-dead-resurrection-d0.html`](brevo-oasis-dead-resurrection-d0.html) |
| Oasis Dead Resurrection D14 | dead_resurrection_d14 | [`brevo-oasis-dead-resurrection-d14.html`](brevo-oasis-dead-resurrection-d14.html) |
| Oasis Return Reinforcement | return_reinforcement_d0 | [`brevo-oasis-return-reinforcement.html`](brevo-oasis-return-reinforcement.html) |

Plain-text: matching `*-plain-text.txt` beside each HTML file.

Regenerate shells from source: `python brevo-oasis-emails/generate_missing_templates.py` (conversion rows only change when you edit `TEMPLATES` in that script).

## Automation exit rules (implement in ESP)

Sequences are spec'd in [`public/email_sequences.json`](../../public/email_sequences.json) with `implementation_status: needs_implementation`. Before enabling drips, configure **exit** so users are not nagged after they return or reply.

### At-risk nurture (D0 → D7 → D14 → D21)

**Stop the sequence when any of:**

1. User **leaves** `at_risk_wau` or `at_risk_mau` (bucket transition to active, reactivated, resurrected, etc.).
2. **New Oasis session** after touch 1 (e.g. `last_active_at` within 24–48 hours) — avoids "I came back and still got D7 two days later."
3. **Reply** to a nurture email (tag e.g. `nurture_replied` or cancel via HubSpot/ESP activity).

### Dead resurrection (D0, D14)

Exit when user leaves `dead` bucket, has a new session, or replies. Respect cap: 20 new users/month when contacts are tight (see sequence notes in `email_sequences.json`).

### Return reinforcement (single touch)

Trigger only on `reactivated` / `resurrected`. **Do not** enroll the same user in at-risk nurture while they are in a returned bucket — buckets should be mutually exclusive in the automation logic.

## Brevo re-paste checklist

After editing HTML in this repo:

1. Open each template in Brevo by name from [`docs/BREVO_NAMING.md`](../../docs/BREVO_NAMING.md) (Oasis At-risk D0, etc.).
2. Paste full HTML from the table above (single root `<table role="presentation">`).
3. Paste matching plain text into the Plain-text tab.
4. Update **subject** and **preheader** to match `email_sequences.json` preview metadata.
5. Send a test to yourself; confirm tone reads as check-in, not win-back.
6. Deploy or run `python reporting/sync_email_previews.py` so `/email-machine` previews refresh.

Links: [`brevo-oasis-email-links.js`](../brevo-oasis-email-links.js)
