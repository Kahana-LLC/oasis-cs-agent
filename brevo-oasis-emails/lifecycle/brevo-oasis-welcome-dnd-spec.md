# Brevo D&D spec: Oasis welcome email

**Trigger:** On signup (all new Oasis users)  
**Full HTML:** [`brevo-oasis-welcome.html`](brevo-oasis-welcome.html)  
**Plain text:** [`brevo-oasis-welcome-plain-text.txt`](brevo-oasis-welcome-plain-text.txt)

## Campaign setup

| Field | Value |
|-------|--------|
| Brevo template name | `Oasis Welcome` |
| Subject | `Welcome to Oasis` |
| Preheader | `Docs, Slack, and support links to get started.` |
| From name | `Adam from Oasis` |
| Title font | **Bricolage Grotesque** (Google Fonts) |
| Body font | **Geist** (Google Fonts) — falls back to system UI sans in clients that block web fonts |

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
| First mission | Headline: *Here is your first mission in the Oasis* — 3 icon rows (import / AI / training) |
| P.S. | After signature: desert midnight theme + hero screenshot |
| Signoff | DM copy → bold tagline → cursive Adam → **All my socials** (underline) | divider | social icons → **P.S.** |
| Footer | Support links snippet + mirror/unsubscribe |

## Social links (welcome signoff)

| Platform | URL |
|----------|-----|
| X | https://twitter.com/adam_kershner |
| Instagram | https://www.instagram.com/adam_kershner/ |
| LinkedIn | https://www.linkedin.com/in/adam-kershner/ |
| TikTok | https://www.tiktok.com/@adam_kershner |
| YouTube | https://www.youtube.com/@adam_kershner |

Icons: X / Instagram / TikTok / YouTube via `cdn.simpleicons.org`. Mission step 2: green badge with ✦ (external AI icons blocked in Brevo). **LinkedIn removed** from welcome.

Cursive close: *Work hard. Be kind. The rest will follow.* 🖤 — **Adam**

## QA

- [ ] Adam headshot loads: `https://kahana.co/images/about/adam-kershner.jpg`
- [ ] Hero screenshot loads: `https://kahana.co/images/oasis-browser-assistant-screenshot.png`
- [ ] Slack icons load (white button, purple footer)
- [ ] All five social icons load and link correctly
- [ ] DM / help copy reads naturally in preview
- [ ] Plain-text pasted from `brevo-oasis-welcome-plain-text.txt`
