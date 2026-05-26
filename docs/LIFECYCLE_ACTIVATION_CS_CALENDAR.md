# Activation CS calendar — Supabase cron → Brevo (step 3 of 5)

**Trigger:** `activation_cs_calendar` · **Template:** Brevo **Oasis Activation CS Calendar**  
**When:** Signup **day 3–5** window, **no** `llm_usage`, **no** `feedback_events`, not in `cs_outreach_log`.

**UI:** [Email Machine](https://oasis-analytics.vercel.app/email-machine#supabase-lifecycle)

---

## 1. Apply cohort RPC migration

[`supabase/migrations/20260525210000_lifecycle_cohort_activation_cs_calendar.sql`](../supabase/migrations/20260525210000_lifecycle_cohort_activation_cs_calendar.sql)

```sql
select * from lifecycle_cohort_activation_cs_calendar(10);
```

---

## 2. Brevo template + secrets

| Field | Value |
|-------|--------|
| Subject | `Need help getting started with Oasis?` (or your chosen subject) |
| Preheader | `Book time with me — train the assistant for 1,000 bonus tokens.` |
| Greeting | `{{ params.GREETING }}` |

Paste [`brevo-oasis-activation-cs-calendar.html`](../brevo-oasis-emails/lifecycle/brevo-oasis-activation-cs-calendar.html) + plain text.

```env
BREVO_TEMPLATE_ID_ACTIVATION_CS_CALENDAR=<numeric id>
```

---

## 3. Local test

```bash
.venv/bin/python scripts/send_lifecycle_email.py \
  --trigger activation_cs_calendar \
  --email YOU@gmail.com --dry-run
```

Skips if `llm_usage` or `feedback_events` exist, or already logged.

---

## 4. Cron

Setup and verification: [`LIFECYCLE_DAILY_CRON.md`](LIFECYCLE_DAILY_CRON.md)

`lifecycle-daily-cron` runs **activation_nudge_24h** and **activation_cs_calendar** by default.

```bash
curl -X POST "$SUPABASE_URL/functions/v1/lifecycle-daily-cron" \
  -H "Authorization: Bearer $SUPABASE_KEY" \
  -H "Content-Type: application/json" \
  -d '{"dry_run":true,"limit":5,"triggers":["activation_cs_calendar"]}'
```

---

## 5. Done when

- [ ] Migration applied
- [ ] Template pasted + `BREVO_TEMPLATE_ID_ACTIVATION_CS_CALENDAR` in Edge secrets
- [ ] Test send to a dev email (`--force` or delete log row to re-test)
- [ ] Daily cron scheduled (same job as nudge)

---

## Next email

**NPS day 3** — [`LIFECYCLE_NPS_DAY3.md`](LIFECYCLE_NPS_DAY3.md)
