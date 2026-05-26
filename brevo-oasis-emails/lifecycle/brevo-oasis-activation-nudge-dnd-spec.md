# Brevo D&D spec: Oasis Activation Nudge

**Trigger:** `activation_nudge_24h` (≥24h after signup, no `llm_usage`)  
**Full HTML:** [`brevo-oasis-activation-nudge.html`](brevo-oasis-activation-nudge.html)  
**Plain text:** [`brevo-oasis-activation-nudge-plain-text.txt`](brevo-oasis-activation-nudge-plain-text.txt)

## Greeting (transactional API)

Opener: **`{{ params.GREETING }}`** — same rules as [`brevo-oasis-welcome-dnd-spec.md`](brevo-oasis-welcome-dnd-spec.md).

## Campaign setup

| Field | Value |
|-------|--------|
| Brevo template name | `Oasis Activation Nudge` |
| Subject | `A few ways to get more from Oasis` |
| Preheader | `Import, ask the assistant, train it — 1,000 tokens per training.` |
| From name | `Adam from Oasis` |

## Snippets (reference)

| Snippet | Use |
|---------|-----|
| [`brevo-oasis-activation-three-steps-snippet.html`](../shared/brevo-oasis-activation-three-steps-snippet.html) | 3-row checklist (import / assistant / train) |
| [`brevo-oasis-need-help-snippet.html`](../shared/brevo-oasis-need-help-snippet.html) | Help center, Contact, Slack |

Canonical HTML inlines these blocks; update snippets first, then sync into the main `.html` if you edit snippets only.

## Block checklist

| Block | Action |
|-------|--------|
| Title | `Get more out of Oasis` |
| Body | Founder header → `{{ params.GREETING }}` → **Three quick wins** headline → subline → 3-step checklist |
| Checklist | Same layout as welcome “first mission” — Firefox / ✦ / Hugging Face icons |
| Need help? | Compact 3-row card: Help center, Contact us, Join Slack (no install CTA) |
| Signoff | Short “Questions? Reply anytime” → cursive Adam → mantra → socials |
| Footer | Docs · Slack · Contact + mirror/unsubscribe |

## QA

- [ ] No `Browse docs` duplicate button stack (Help center only in Need help card)
- [ ] `{{ params.GREETING }}` renders (not `contact.FIRSTNAME`)
- [ ] Subject/preheader match table above
- [ ] Plain-text pasted from `brevo-oasis-activation-nudge-plain-text.txt`
