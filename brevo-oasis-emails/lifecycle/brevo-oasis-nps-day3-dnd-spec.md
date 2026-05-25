# Brevo D&D spec: NPS email (day 3)

**Trigger:** 3 days after signup  
**Full HTML:** [`brevo-oasis-nps-day3.html`](brevo-oasis-nps-day3.html)  
**Plain text:** [`brevo-oasis-nps-day3-plain-text.txt`](brevo-oasis-nps-day3-plain-text.txt)  
**Survey page:** https://kahana.co/oasis-nps  
**Tally embed (email score links):** https://tally.so/r/ODoBz7

## Campaign setup

| Field | Value |
|-------|--------|
| Brevo template name | `Oasis NPS` |
| Subject | `Quick question: how likely are you to recommend Oasis?` |
| Preheader | `One question. Your feedback helps us improve.` |
| From name | `Adam from Oasis` |

## Snippets to paste

| Snippet | Use |
|---------|-----|
| [`brevo-oasis-lifecycle-founder-header-snippet.html`](../shared/brevo-oasis-lifecycle-founder-header-snippet.html) | After greeting |
| [`brevo-oasis-nps-tally-form-snippet.html`](brevo-oasis-nps-tally-form-snippet.html) | Inline 0-10 NPS scale (replaces Share your score button) |
| [`brevo-oasis-slack-button-snippet.html`](../shared/brevo-oasis-slack-button-snippet.html) | After NPS form |
| [`brevo-oasis-founder-signoff-package-snippet.html`](../shared/brevo-oasis-founder-signoff-package-snippet.html) | Help line + `- Adam` + mantra + socials before footer |
| [`brevo-oasis-support-links-snippet.html`](../shared/brevo-oasis-support-links-snippet.html) | Footer |

Tally setup: [`brevo-oasis-nps-tally-form-setup.md`](brevo-oasis-nps-tally-form-setup.md)

## Block checklist

| Block | Action |
|-------|--------|
| Title | `How are we doing so far?` |
| Body | Adam headshot + first-person NPS ask |
| NPS form card | Paste 0-10 score grid snippet |
| Button | Join Slack (purple `#4A154B`) |
| Signoff | `- Adam` + mantra + **All my socials** row → `https://kahana.co/adam-kershner` + X/IG/TikTok/YouTube icons |
| Footer | Support links snippet |

## QA

- [ ] Adam headshot loads
- [ ] Each score link opens Tally with score pre-selected (test 0, 5, 10)
- [ ] Slack button and footer icon load
- [ ] All my socials link and icon row load (no LinkedIn)
- [ ] Exclude unsubscribed users from automation
