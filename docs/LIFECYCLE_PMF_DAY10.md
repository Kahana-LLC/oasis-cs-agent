# PMF day 10 — Supabase cron → Brevo (step 5 of 5)

**Trigger:** `pmf_day10` · **Template:** Brevo **Oasis PMF** (id **57**)  
**When:** Signup **day 10–12** window, all active users.  
**CTA:** `https://kahana.co/oasis-pmf?email=…` (full survey in browser)  
**Dedup:** `cs_outreach_log` · **Cron:** [`LIFECYCLE_DAILY_CRON.md`](LIFECYCLE_DAILY_CRON.md)

Completes **Phase 1** lifecycle (welcome + 4 cron emails).

---

## 1. Apply cohort RPC migration

[`supabase/migrations/20260525230000_lifecycle_cohort_pmf_day10.sql`](../supabase/migrations/20260525230000_lifecycle_cohort_pmf_day10.sql)

```sql
select * from lifecycle_cohort_pmf_day10(10);
```

---

## 2. Brevo template + secrets

| Field | Value |
|-------|--------|
| Subject | e.g. `Quick favor — help us improve Oasis?` |
| Preheader | `Your ideas and honest feedback help us make Oasis better for you.` |
| Greeting | `{{ params.GREETING }}` |
| Survey links | `{{ params.EMAIL }}` on `kahana.co/oasis-pmf` and optional `tally.so/r/EkNbXX` |

Paste:

- [`brevo-oasis-pmf-day10.html`](../brevo-oasis-emails/lifecycle/brevo-oasis-pmf-day10.html)
- [`brevo-oasis-pmf-day10-plain-text.txt`](../brevo-oasis-emails/lifecycle/brevo-oasis-pmf-day10-plain-text.txt)

```env
BREVO_TEMPLATE_ID_PMF_DAY10=57
```

Edge: include in bulk secrets or `supabase secrets set BREVO_TEMPLATE_ID_PMF_DAY10=57`

Deploy:

```bash
supabase functions deploy lifecycle-send lifecycle-daily-cron --project-ref wvclepquxxczgrukfqyr --no-verify-jwt
```

---

## 3. Local test

```bash
.venv/bin/python scripts/send_lifecycle_email.py \
  --trigger pmf_day10 \
  --email YOU@gmail.com --dry-run

.venv/bin/python scripts/send_lifecycle_email.py \
  --trigger pmf_day10 \
  --email YOU@gmail.com --force
```

---

## 4. Cron

`lifecycle-daily-cron` **DEFAULT_TRIGGERS** now includes all Phase 1 emails (nudge, CS, NPS, PMF). No new cron job needed.

```bash
curl -X POST "$SUPABASE_URL/functions/v1/lifecycle-daily-cron" \
  -H "Authorization: Bearer $SUPABASE_KEY" \
  -H "Content-Type: application/json" \
  -d '{"dry_run":true,"limit":5,"triggers":["pmf_day10"]}'
```

---

## 5. Production checklist

| Item | Status |
|------|--------|
| Migration `lifecycle_cohort_pmf_day10` | Apply on Oasis |
| Deploy `lifecycle-send` + `lifecycle-daily-cron` | After code change |
| `BREVO_TEMPLATE_ID_PMF_DAY10=57` in Edge secrets | Confirm |
| Brevo template **57** pasted (`params.GREETING`, `params.EMAIL`) | You confirm |
| Test send + survey link works | You confirm |
