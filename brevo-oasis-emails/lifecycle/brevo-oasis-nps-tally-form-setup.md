# Tally NPS form setup for email embed (ODoBz7)

Email clients **cannot** run a live Tally iframe inside the message. The NPS email uses [Tally's recommended pattern](https://tally.so/help/how-to-embed-a-form-in-an-email): **tappable 0-10 score buttons** that open a **pre-filled Tally form** in the browser.

Snippet to paste in Brevo: [`brevo-oasis-nps-tally-form-snippet.html`](brevo-oasis-nps-tally-form-snippet.html)

---

## Form field

The NPS question uses Tally linear scale field:

`linear_scale_37aadfce-8894-4772-9712-709dbb4cfdaf`

Example pre-filled URL (score 8):

```
https://tally.so/r/ODoBz7?linear_scale_37aadfce-8894-4772-9712-709dbb4cfdaf=8&email=test@example.com
```

---

## Optional: hidden email field

To identify respondents in Tally responses, add a hidden field in the Tally editor:

| Hidden field name | URL parameter | Purpose |
|-------------------|---------------|---------|
| `email` | `email` | Pre-fill or track Brevo contact email |

The email snippet already passes `email={{ contact.EMAIL }}` on every score link.

---

## Test before send

1. Open in browser: `https://tally.so/r/ODoBz7?linear_scale_37aadfce-8894-4772-9712-709dbb4cfdaf=9&email=test@example.com`
2. Confirm score **9** is pre-selected.
3. Send a Brevo test email; tap scores 0, 5, and 10 and confirm pre-fill works.

---

## Brevo D&D

Replace the single "Share your score" button with [`brevo-oasis-nps-tally-form-snippet.html`](brevo-oasis-nps-tally-form-snippet.html) in a **Text block** (source mode).
