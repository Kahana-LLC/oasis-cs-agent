# NPS day 3 — Supabase cron → Brevo (step 4 of 5)

**Trigger:** `nps_day3` · **Template:** Brevo **Oasis NPS** (id **56**)  
**When:** Signup **day 3–5** window, all active users (no prompt/training gate).  
**Dedup:** `cs_outreach_log` · **Cron:** same job as nudge/CS — [`LIFECYCLE_DAILY_CRON.md`](LIFECYCLE_DAILY_CRON.md)

---

## 1. Apply cohort RPC migration

[`supabase/migrations/20260525220000_lifecycle_cohort_nps_day3.sql`](../supabase/migrations/20260525220000_lifecycle_cohort_nps_day3.sql)

```sql
select * from lifecycle_cohort_nps_day3(10);
```

---

## 2. Brevo template + secrets

| Field | Value |
|-------|--------|
| Subject | e.g. `How are we doing so far?` |
| Preheader | `One question. Your feedback helps us improve.` |
| Greeting | `{{ params.GREETING }}` |
| Yes / No / Maybe | Link to `https://kahana.co/oasis-nps?email={{ params.EMAIL }}&recommend=yes|no|maybe` — 0–10 on web |
| Fallback | `https://tally.so/r/ODoBz7?email={{ params.EMAIL }}` |

Paste:

- [`brevo-oasis-nps-day3.html`](../brevo-oasis-emails/lifecycle/brevo-oasis-nps-day3.html)
- [`brevo-oasis-nps-day3-plain-text.txt`](../brevo-oasis-emails/lifecycle/brevo-oasis-nps-day3-plain-text.txt)

```env
BREVO_TEMPLATE_ID_NPS_DAY3=56
```

Edge: `supabase secrets set BREVO_TEMPLATE_ID_NPS_DAY3=56`

Deploy:

```bash
supabase functions deploy lifecycle-send lifecycle-daily-cron --project-ref wvclepquxxczgrukfqyr --no-verify-jwt
```

---

## 3. Local test

```bash
.venv/bin/python scripts/send_lifecycle_email.py \
  --trigger nps_day3 \
  --email YOU@gmail.com --dry-run

.venv/bin/python scripts/send_lifecycle_email.py \
  --trigger nps_day3 \
  --email YOU@gmail.com --force
```

Tap **Yes**, **No**, or **Maybe** — should open `kahana.co/oasis-nps` with your email; pick 0–10 on that page.

---

## 4. Cron

Daily `lifecycle-daily-cron` now includes `nps_day3` in **DEFAULT_TRIGGERS** (no cron SQL change needed if job already scheduled).

Dry-run one trigger:

```bash
curl -X POST "$SUPABASE_URL/functions/v1/lifecycle-daily-cron" \
  -H "Authorization: Bearer $SUPABASE_KEY" \
  -H "Content-Type: application/json" \
  -d '{"dry_run":true,"limit":5,"triggers":["nps_day3"]}'
```

---

## 5. Production checklist

| Item | Status |
|------|--------|
| Migration `lifecycle_cohort_nps_day3` | Done (Oasis DB) |
| `lifecycle-send` + `lifecycle-daily-cron` include `nps_day3` | Done (deployed) |
| Daily cron job `lifecycle-daily-cron` | Done (you scheduled job id 4) |
| `BREVO_TEMPLATE_ID_NPS_DAY3=56` in Edge secrets | Confirm (you bulk-set secrets) |
| Brevo template **56** HTML pasted (Yes/No/Maybe + `params.GREETING`) | **You confirm** after latest paste |
| Test send in inbox looks right | **You confirm** |
| `kahana.co/oasis-nps` shows 0–10 after tap | **You confirm** on phone |
| First live cron batch in `cs_outreach_log` | Pending next 14:00 UTC run |

---

## Next email

**PMF day 10** — [`LIFECYCLE_PMF_DAY10.md`](LIFECYCLE_PMF_DAY10.md) (final Phase 1 email)
