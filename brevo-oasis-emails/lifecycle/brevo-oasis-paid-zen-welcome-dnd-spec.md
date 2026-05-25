# Brevo D&D spec: Paid Zen welcome email

**Trigger:** Zen plan upgrade ($20/mo)  
**Full HTML:** [`brevo-oasis-paid-zen-welcome.html`](brevo-oasis-paid-zen-welcome.html)  
**Plain text:** [`brevo-oasis-paid-zen-welcome-plain-text.txt`](brevo-oasis-paid-zen-welcome-plain-text.txt)  
**Billing portal:** https://billing.stripe.com/p/login/bIYg16d6l3FqelieUU

## Campaign setup

| Field | Value |
|-------|--------|
| Brevo template name | `Oasis Paid Zen Welcome` |
| Subject | `Welcome to Oasis Zen` |
| Preheader | `1M tokens per day and priority support are now active.` |
| From name | `Adam from Oasis` |

## Snippets to paste

| Snippet | Use |
|---------|-----|
| [`brevo-oasis-lifecycle-founder-header-snippet.html`](../shared/brevo-oasis-lifecycle-founder-header-snippet.html) | After greeting |
| [`brevo-oasis-slack-button-snippet.html`](../shared/brevo-oasis-slack-button-snippet.html) | After billing CTA |
| [`brevo-oasis-lifecycle-founder-signoff-snippet.html`](../shared/brevo-oasis-lifecycle-founder-signoff-snippet.html) | Before footer |
| [`brevo-oasis-support-links-snippet.html`](../shared/brevo-oasis-support-links-snippet.html) | Footer |

## Block checklist

| Block | Action |
|-------|--------|
| Title | `Welcome to Zen` |
| Body | Adam headshot + thank you + Zen benefits list |
| Button 1 | Manage billing → Stripe portal URL |
| Button 2 | Join Slack (purple `#4A154B`) |
| Signoff | `- Adam` + mantra + **All my socials** row → `https://kahana.co/adam-kershner` + X/IG/TikTok/YouTube icons |
| Footer | Support links snippet |

## Brevo trigger note

Fire from Stripe checkout webhook or Brevo automation when contact attribute `plan = zen`. Separate workflow from day 3/10 sequence.

## QA

- [ ] Adam headshot loads
- [ ] Billing portal link works
- [ ] Slack button and footer icon load
- [ ] All my socials link and icon row load (no LinkedIn)
- [ ] Zen benefits match [`pages/oasis-pricing.jsx`](../../pages/oasis-pricing.jsx)
