# Activation nudge — Supabase cron → Brevo (step 2 of 5)

**Trigger:** `activation_nudge_24h` · **Template:** Brevo **Oasis Activation Nudge**  
**When:** User signed up ≥24h ago, **no** `llm_usage` row, not already in `cs_outreach_log`.

**UI:** [Email Machine](https://oasis-analytics.vercel.app/email-machine#supabase-lifecycle)

---

## 1. Apply cohort RPC migration

Run in Oasis Supabase SQL Editor (or `supabase db push`):

[`supabase/migrations/20260525150000_lifecycle_cohort_activation_nudge.sql`](../supabase/migrations/20260525150000_lifecycle_cohort_activation_nudge.sql)

Test cohort:

```sql
select * from lifecycle_cohort_activation_nudge_24h(10);
```

---

## 2. Brevo template + secrets

1. List template id:

   ```bash
   .venv/bin/python scripts/list_brevo_smtp_templates.py
   ```

2. Paste HTML from [`brevo-oasis-activation-nudge.html`](../brevo-oasis-emails/lifecycle/brevo-oasis-activation-nudge.html) and plain text from [`brevo-oasis-activation-nudge-plain-text.txt`](../brevo-oasis-emails/lifecycle/brevo-oasis-activation-nudge-plain-text.txt).

   **Layout:** welcome-style **3-step checklist** + compact **Need help?** (Help center, Contact, Slack). No install / “Jump back in” button.

   **Brevo paste guide:** [`brevo-oasis-activation-nudge-dnd-spec.md`](../brevo-oasis-emails/lifecycle/brevo-oasis-activation-nudge-dnd-spec.md)

   | Field | Value |
   |-------|--------|
   | Subject | `A few ways to get more from Oasis` |
   | Preheader | `Import, ask the assistant, train it — 1,000 tokens per training.` |
   | Greeting | `{{ params.GREETING }}` (not `contact.FIRSTNAME`) |

3. `.env` and Edge secrets:

   ```env
   BREVO_TEMPLATE_ID_ACTIVATION_NUDGE=<numeric id>
   ```

   ```bash
   supabase secrets set BREVO_TEMPLATE_ID_ACTIVATION_NUDGE="<id>"
   ```

---

## 3. Local send (one user)

```bash
.venv/bin/python scripts/send_lifecycle_email.py \
  --trigger activation_nudge_24h \
  --email YOU@gmail.com --dry-run

.venv/bin/python scripts/send_lifecycle_email.py \
  --trigger activation_nudge_24h \
  --email YOU@gmail.com
```

Skips if `llm_usage` exists or `cs_outreach_log` already has `activation_nudge_24h`.

---

## 4. Deploy Edge Functions

```bash
supabase functions deploy lifecycle-send --no-verify-jwt
supabase functions deploy lifecycle-daily-cron --no-verify-jwt
```

**Manual cohort dry-run:**

```bash
curl -X POST "$SUPABASE_URL/functions/v1/lifecycle-daily-cron" \
  -H "Authorization: Bearer $SUPABASE_KEY" \
  -H "Content-Type: application/json" \
  -d '{"dry_run":true,"limit":5}'
```

**Production send (cap 500/run):**

```bash
curl -X POST "$SUPABASE_URL/functions/v1/lifecycle-daily-cron" \
  -H "Authorization: Bearer $SUPABASE_KEY" \
  -H "Content-Type: application/json" \
  -d '{"limit":500}'
```

---

## 5. Supabase Cron (daily)

Full setup + verification: [`LIFECYCLE_DAILY_CRON.md`](LIFECYCLE_DAILY_CRON.md)

Dashboard → **Cron** (or Edge Function schedules):

| Field | Value |
|-------|--------|
| Schedule | `0 14 * * *` (14:00 UTC — adjust for US morning) |
| URL | `https://<project>.supabase.co/functions/v1/lifecycle-daily-cron` |
| Method | POST |
| Body | `{}` or `{"limit":500}` |
| Headers | `Authorization: Bearer <service_role>` |

---

## 6. Done when

- [ ] Migration `lifecycle_cohort_activation_nudge_24h` applied
- [ ] `BREVO_TEMPLATE_ID_ACTIVATION_NUDGE` in Edge secrets + Brevo template pasted
- [ ] Local send returns `sent: true` for eligible test user
- [ ] Cron dry-run lists cohort; live run logs `cs_outreach_log`
- [ ] User with `llm_usage` is skipped (`has_first_prompt`)

---

## Next email

**Activation CS calendar** — [`LIFECYCLE_ACTIVATION_CS_CALENDAR.md`](LIFECYCLE_ACTIVATION_CS_CALENDAR.md)
