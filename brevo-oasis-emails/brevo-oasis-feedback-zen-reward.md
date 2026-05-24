# Oasis feedback survey Zen reward

Thank-you for completing Oasis NPS or PMF surveys on the website.

## Offer

| Item | Value |
|------|--------|
| Reward | 1 month Oasis Zen (1,000,000 tokens per day) |
| Qualifier | Complete NPS **or** PMF Tally form |
| Limit | One month per survey per Oasis account (max 2 months if both) |
| Verification | Match Tally response email to Oasis account |
| Fulfillment | Manual Stripe/admin upgrade; confirmation reply |
| SLA | 2-3 business days |

## Survey pages

| Survey | Page | Tally form |
|--------|------|------------|
| NPS | https://kahana.co/oasis-nps | https://tally.so/r/ODoBz7 |
| PMF | https://kahana.co/oasis-pmf | https://tally.so/r/EkNbXX |

Config source: [`data/oasis-feedback-surveys.js`](../../data/oasis-feedback-surveys.js)

## Redemption runbook

1. User completes NPS or PMF on the survey page (or via lifecycle email).
2. Tally response includes email matching their Oasis account.
3. Team verifies submission is complete and not duplicate for that survey.
4. Manually extend Zen / token limit for 1 month (Stripe or internal admin).
5. Send confirmation email to the user.

If the same person completes **both** surveys, grant 1 month per survey (2 months total).

## Tally admin checklist

- Both forms collect **email** (required field or hidden `email` for pre-fill from `?email=` URL param)
- Tag or filter responses by form ID (`ODoBz7` vs `EkNbXX`)
- Optional: post-submit redirect to a thank-you page mentioning Zen activation timeline

## Lifecycle email links

NPS day 3 email: inline 0-10 score links still open Tally pre-filled; fallback links to https://kahana.co/oasis-nps

PMF day 10 email: primary CTA links to https://kahana.co/oasis-pmf (shows Zen offer before submit)

## QA

- [ ] `/oasis-nps` and `/oasis-pmf` embed Tally and show Zen reward card
- [ ] `?email=user@example.com` pre-fills Tally on both pages
- [ ] Footer links: Refer a Friend Survey, Help Us Improve
- [ ] Zen numbers match [`pages/oasis-pricing.jsx`](../../pages/oasis-pricing.jsx) (1M tokens/day, $20/mo plan)
