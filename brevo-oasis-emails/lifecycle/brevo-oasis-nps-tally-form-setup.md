# NPS survey links (email + web)

Email clients cannot embed a live 0–10 grid reliably. The NPS email uses **Yes / No / Maybe** buttons that open the full survey in the browser.

---

## Email flow

| Tap | Opens |
|-----|--------|
| **Yes** | `https://kahana.co/oasis-nps?email=…&recommend=yes` |
| **No** | `https://kahana.co/oasis-nps?email=…&recommend=no` |
| **Maybe** | `https://kahana.co/oasis-nps?email=…&recommend=maybe` |

Snippet: [`brevo-oasis-nps-tally-form-snippet.html`](brevo-oasis-nps-tally-form-snippet.html)  
Full template: [`brevo-oasis-nps-day3.html`](brevo-oasis-nps-day3.html)

`recommend` is optional tracking on the survey page; all three land on the same 0–10 experience.

---

## Tally (direct 0–10)

Form: https://tally.so/r/ODoBz7

Email fallback link (no pre-selected score):

```
https://tally.so/r/ODoBz7?email=test@example.com
```

Pre-filled score (if needed elsewhere):

```
https://tally.so/r/ODoBz7?linear_scale_37aadfce-8894-4772-9712-709dbb4cfdaf=8&email=test@example.com
```

Field id: `linear_scale_37aadfce-8894-4772-9712-709dbb4cfdaf`

---

## Brevo params

| Param | Use |
|-------|-----|
| `{{ params.GREETING }}` | Opener line |
| `{{ params.EMAIL }}` | Survey + Tally query string |

---

## QA

1. Send test email; tap **Yes**, **No**, **Maybe** — each opens `kahana.co/oasis-nps` with email in URL.
2. Confirm 0–10 picker works on that page (or use Tally fallback link).
3. `{{ params.GREETING }}` renders (not `Hi ,`).
