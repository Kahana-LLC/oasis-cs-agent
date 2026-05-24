# Tally form setup for email embed (w8V8GA)

Email clients **cannot** run a live Tally iframe or JavaScript embed inside the message. The teaser email uses [Tally’s recommended pattern](https://tally.so/help/how-to-embed-a-form-in-an-email): **tappable buttons in the email** that open a **pre-filled Tally form** in the browser.

Snippet to paste in Brevo: [`brevo-oasis-ph-tally-form-snippet.html`](brevo-oasis-ph-tally-form-snippet.html)

---

## One-time Tally configuration

In the Tally editor for form `w8V8GA`, add these **hidden fields** (type `/hidden`):

| Hidden field name | URL parameter | Purpose |
|-------------------|---------------|---------|
| `browser_engine` | `browser_engine` | Pre-select Browser Engine from email tap |
| `email` | `email` | Pre-fill email from Brevo contact |
| `ref` | `ref` | Track source (`ph_teaser`) |

For each hidden field used to pre-select an answer:

1. Add the hidden field block with the exact name above.
2. On the **Browser Engine** question, set the hidden field value as the **default answer** for that question (Tally: question settings → default from hidden field).

Example email button URL:

```
https://tally.so/r/w8V8GA?browser_engine=Firefox&ref=ph_teaser&email={{ contact.EMAIL }}
```

When the recipient taps **Firefox**, Tally opens with Browser Engine already selected; they complete remaining pages and submit.

---

## Test before send

1. Publish the Tally form after adding hidden fields.
2. Open this URL in a browser (replace email manually):

   `https://tally.so/r/w8V8GA?browser_engine=Firefox&ref=ph_teaser&email=test@example.com`

3. Confirm Browser Engine is pre-selected to **Firefox**.
4. Send a Brevo **test email** to yourself; tap each button and confirm pre-fill works.

---

## Brevo D&D

After the platform paragraph in the teaser, paste [`brevo-oasis-ph-tally-form-snippet.html`](brevo-oasis-ph-tally-form-snippet.html) into a **Text block** (source mode).

Remove the old inline “Choose your version” text link if it duplicates the form card.

---

## View in browser

The interactive buttons work in all email clients. Recipients who use **View in browser** get the same experience: still not a live iframe inside the email, but fully tappable.

For a full inline form on the web, use [`pages/oasis-waitlist.jsx`](../../pages/oasis-waitlist.jsx) (iframe embed on kahana.co/oasis-waitlist).
