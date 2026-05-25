# Welcome email — Supabase → Brevo (step 1 of 5)

First lifecycle send in the [Supabase Edge plan](SUPABASE_LIFECYCLE_EMAIL_PLAN.md). **Trigger:** `welcome_email` on `users` INSERT. **Template:** Brevo SMTP template **Oasis Welcome**.

**UI:** [Email Machine](https://oasis-analytics.vercel.app/email-machine#supabase-lifecycle)

---

## 1. Supabase: dedup table

Run in Oasis Supabase SQL Editor (or `supabase db push` from a clone of this migration):

[`supabase/migrations/20260525140000_cs_outreach_log.sql`](../supabase/migrations/20260525140000_cs_outreach_log.sql)

---

## 2. Brevo: template id + sender

1. **Campaigns → Templates → Transactional** (or SMTP templates) — confirm **Oasis Welcome** exists and uses `{{ params.FIRSTNAME }}` or `{{ contact.FIRSTNAME }}` as in your pasted HTML.
2. List ids:

   ```bash
   .venv/bin/python scripts/list_brevo_smtp_templates.py
   ```

3. `.env`:

   ```env
   BREVO_TEMPLATE_ID_WELCOME=123
   LIFECYCLE_SENDER_EMAIL=you@verified-domain.com
   LIFECYCLE_SENDER_NAME=Adam from Oasis
   ```

   (`FROM_EMAIL` / `FROM_NAME` work as fallbacks.)

---

## 3. Local test (this repo)

```bash
.venv/bin/pip install brevo-python python-dotenv

# Dry run
.venv/bin/python scripts/send_lifecycle_email.py \
  --email YOUR@gmail.com --dry-run

# Send (requires cs_outreach_log + template id)
.venv/bin/python scripts/send_lifecycle_email.py \
  --email YOUR@gmail.com
```

- **Skipped `already_sent`:** row exists in `cs_outreach_log` for that user — delete the row to re-test or use `--force`.
- **404 table:** run migration §1.

---

## 4. Deploy Edge Functions (Oasis Supabase project)

Copy [`supabase/functions/`](../supabase/functions/) into the Oasis app repo (or deploy from a monorepo path).

**Secrets** (Supabase → Edge Functions → Secrets):

| Secret | Value |
|--------|--------|
| `BREVO_API_KEY` | v3 `xkeysib-…` |
| `BREVO_TEMPLATE_ID_WELCOME` | numeric template id |
| `LIFECYCLE_SENDER_EMAIL` | verified sender |
| `LIFECYCLE_SENDER_NAME` | `Adam from Oasis` |

`SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` are provided automatically.

```bash
supabase functions deploy lifecycle-send
supabase functions deploy lifecycle-on-signup
```

**Manual invoke (production check):**

```bash
curl -X POST "$SUPABASE_URL/functions/v1/lifecycle-send" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Content-Type: application/json" \
  -d '{"trigger_name":"welcome_email","email":"you@example.com","dry_run":true}'
```

---

## 5. Database webhook (automatic on signup)

Supabase Dashboard → **Database → Webhooks**:

| Field | Value |
|-------|--------|
| Table | `users` |
| Events | Insert |
| URL | `https://<project>.supabase.co/functions/v1/lifecycle-on-signup` |
| Headers | `Authorization: Bearer <service_role_key>` |

New signups send welcome once; dedup prevents duplicates.

**Do not** activate Brevo **Oasis Phase 1** welcome step if Edge path is live (double welcome).

---

## 6. Done when

- [ ] `cs_outreach_log` exists
- [ ] `BREVO_TEMPLATE_ID_WELCOME` set
- [ ] Local `send_lifecycle_email.py` returns `sent: true` for a test user
- [ ] Edge `lifecycle-send` dry-run OK
- [ ] Webhook on `users` INSERT deployed
- [ ] One real signup receives **Oasis Welcome** once

---

## Next email

**Activation nudge** (`activation_nudge_24h`) — daily cron + no `llm_usage` cohort (not started yet).
