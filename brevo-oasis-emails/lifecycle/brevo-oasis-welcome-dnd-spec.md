# Brevo D&D spec: Oasis welcome email

**Trigger:** On signup (all new Oasis users)  
**Full HTML:** [`brevo-oasis-welcome.html`](brevo-oasis-welcome.html)  
**Plain text:** [`brevo-oasis-welcome-plain-text.txt`](brevo-oasis-welcome-plain-text.txt)

## Campaign setup

| Field | Value |
|-------|--------|
| Subject | `Welcome to Oasis` |
| Preheader | `Docs, Slack, and support links to get started.` |
| From name | `Adam from Oasis` |

## Snippets to paste

| Snippet | Use |
|---------|-----|
| [`brevo-oasis-lifecycle-founder-header-snippet.html`](../shared/brevo-oasis-lifecycle-founder-header-snippet.html) | After greeting |
| Hero screenshot block | After founder intro (see HTML) |
| [`brevo-oasis-slack-button-snippet.html`](../shared/brevo-oasis-slack-button-snippet.html) | After Browse docs button |
| [`brevo-oasis-lifecycle-founder-signoff-snippet.html`](../shared/brevo-oasis-lifecycle-founder-signoff-snippet.html) | Before footer |
| [`brevo-oasis-support-links-snippet.html`](../shared/brevo-oasis-support-links-snippet.html) | Footer |

## Block checklist

| Block | Action |
|-------|--------|
| Title | `Welcome to Oasis` |
| Body | Adam headshot + first-person welcome + hero screenshot + support block |
| Button 1 | Browse docs → `https://kahana.co/docs` |
| Button 2 | Join Slack (purple `#4A154B`) → Slack channel URL |
| Signoff | Connect with me → `https://kahana.co/adam-kershner` |
| Footer | Support links snippet + mirror/unsubscribe |

## QA

- [ ] Adam headshot loads: `https://kahana.co/images/about/adam-kershner.jpg`
- [ ] Hero screenshot loads: `https://kahana.co/images/oasis-browser-assistant-screenshot.png`
- [ ] Slack icons load (white button, purple footer)
- [ ] Connect with me link works: `https://kahana.co/adam-kershner`
- [ ] Plain-text pasted from `brevo-oasis-welcome-plain-text.txt`
