# Brevo D&D spec: PMF email (day 10)

**Trigger:** 10 days after signup  
**Full HTML:** [`brevo-oasis-pmf-day10.html`](brevo-oasis-pmf-day10.html)  
**Plain text:** [`brevo-oasis-pmf-day10-plain-text.txt`](brevo-oasis-pmf-day10-plain-text.txt)  
**Survey page:** https://kahana.co/oasis-pmf  
**Tally embed:** https://tally.so/r/EkNbXX

## Campaign setup

| Field | Value |
|-------|--------|
| Brevo template name | `Oasis PMF` |
| Subject | `Help us understand how Oasis fits your workflow` |
| Preheader | `2-minute product survey. Your answers shape what we build next.` |
| From name | `Adam from Oasis` |

## Snippets to paste

| Snippet | Use |
|---------|-----|
| [`brevo-oasis-lifecycle-founder-header-snippet.html`](../shared/brevo-oasis-lifecycle-founder-header-snippet.html) | After greeting |
| [`brevo-oasis-slack-button-snippet.html`](../shared/brevo-oasis-slack-button-snippet.html) | After survey CTA |
| [`brevo-oasis-lifecycle-founder-signoff-snippet.html`](../shared/brevo-oasis-lifecycle-founder-signoff-snippet.html) | Before footer |
| [`brevo-oasis-support-links-snippet.html`](../shared/brevo-oasis-support-links-snippet.html) | Footer |

## Block checklist

| Block | Action |
|-------|--------|
| Title | `We'd love your input` |
| Body | Adam headshot + first-person PMF framing |
| Button 1 | Take the survey → `https://kahana.co/oasis-pmf?email={{ contact.EMAIL }}` |
| Button 2 | Join Slack (purple `#4A154B`) |
| Signoff | `- Adam` + mantra + **All my socials** row → `https://kahana.co/adam-kershner` + X/IG/TikTok/YouTube icons |
| Footer | Support links snippet |

## QA

- [ ] Adam headshot loads
- [ ] Tally survey opens from button and fallback link
- [ ] Slack button and footer icon load
- [ ] All my socials link and icon row load (no LinkedIn)
- [ ] Exclude unsubscribed users from automation
