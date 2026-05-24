# Product Hunt Zen gift offer

Launch-day thank-you for waitlist subscribers who leave genuine feedback on Product Hunt.

## Offer

| Item | Value |
|------|--------|
| Gift | 1,000,000 tokens per day for 6 months |
| Equivalent | Oasis Zen ($20/mo, ~$120 value) |
| Qualifier | Genuine comment on PH launch page |
| Redemption | Reply to campaign email with screenshot of PH comment |
| Window | 7 days from launch |

## Email placement

| Email | Snippet | Reveal level |
|-------|---------|--------------|
| Teaser (May 26) | [`brevo-oasis-ph-zen-gift-teaser-snippet.html`](brevo-oasis-ph-zen-gift-teaser-snippet.html) | Hint only |
| Launch (May 27) | [`brevo-oasis-ph-zen-gift-launch-snippet.html`](brevo-oasis-ph-zen-gift-launch-snippet.html) | Full offer + claim steps |
| Launch terms | [`brevo-oasis-ph-zen-gift-terms-snippet.html`](brevo-oasis-ph-zen-gift-terms-snippet.html) | Fine print (inline in launch snippet) |

## Links

| Label | URL |
|-------|-----|
| Product Hunt signup | https://www.producthunt.com/ |
| PH launch (comment) | https://www.producthunt.com/products/kahana?embed=true&utm_source=badge-featured&utm_medium=badge&utm_campaign=badge-oasis-browser-for-mac |

## Redemption runbook

1. User leaves a genuine comment on the PH launch listing.
2. User replies to the Brevo campaign with a screenshot of their comment.
3. Team verifies the comment exists on Product Hunt and is original feedback.
4. Match reply email to Oasis account email.
5. Manually upgrade to Zen / extend token limit for 6 months (Stripe or internal admin).
6. Send confirmation reply to the user.

**Brevo setup:** Set reply-to to a monitored inbox (e.g. `adam@kahana.co` or support).

## QA

- [ ] Teaser hints only; no full claim steps
- [ ] Launch has full offer, 3 steps, screenshot instructions
- [ ] Zen numbers match [`pages/oasis-pricing.jsx`](../../pages/oasis-pricing.jsx)
- [ ] No em dashes in copy
