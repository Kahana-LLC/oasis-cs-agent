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
| Subject | `Quick favor — help us improve Oasis?` |
| Preheader | `Your ideas and honest feedback help us make Oasis better for you.` |
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
| Body | Adam headshot + casual ask for suggestions, issues, what’s working |
| Button 1 | Share your thoughts → `https://kahana.co/oasis-pmf?email={{ params.EMAIL }}` |
| Button 2 | Join Slack (purple `#4A154B`) |
| Signoff | `- Adam` + mantra + **All my socials** row → `https://kahana.co/adam-kershner` + X/IG/TikTok/YouTube icons |
| Footer | Support links snippet |

## QA

- [ ] Adam headshot loads
- [ ] Tally survey opens from button and fallback link
- [ ] Slack button and footer icon load
- [ ] All my socials link and icon row load (no LinkedIn)
- [ ] Exclude unsubscribed users from automation
