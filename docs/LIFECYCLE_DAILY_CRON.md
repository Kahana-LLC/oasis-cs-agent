# Daily lifecycle cron (`lifecycle-daily-cron`)

One scheduled job sends **Phase 1** (activation nudge, CS calendar, NPS, PMF) and **Phase 2** (limit-hitter, at-risk, dead, return, enterprise, cancelled D14). Welcome stays on `users` INSERT; upgrade/cancel stay on `user_plans` webhook. See [`LIFECYCLE_PHASE2.md`](LIFECYCLE_PHASE2.md).

**Project:** `wvclepquxxczgrukfqyr`  
**Function URL:** `https://wvclepquxxczgrukfqyr.supabase.co/functions/v1/lifecycle-daily-cron`

---

## Is it already set up?

Run in **SQL Editor** (Dashboard → SQL):

```sql
select jobid, jobname, schedule, active
from cron.job
where jobname ilike '%lifecycle%'
   or command ilike '%lifecycle-daily-cron%';
```

| Result | Meaning |
|--------|---------|
| **0 rows** | Not scheduled — create the job below |
| **1 row**, `active = true` | Scheduled — use [Verify after a run](#verify-after-a-run) |

Your project already uses **pg_cron + pg_net** for `report-builder` (`feedback-report-every-6-hours`). Lifecycle should follow the same pattern.

---

## Option A — SQL (recommended; matches existing jobs)

1. Dashboard → **Project Settings → API** → copy the **service_role** key (secret).
2. SQL Editor → run (replace `YOUR_SERVICE_ROLE_KEY`):

```sql
select cron.schedule(
  'lifecycle-daily-cron',
  '0 14 * * *',  -- 14:00 UTC daily (~9am US Eastern in winter)
  $$
  select net.http_post(
    url := 'https://wvclepquxxczgrukfqyr.supabase.co/functions/v1/lifecycle-daily-cron',
    headers := jsonb_build_object(
      'Content-Type', 'application/json',
      'Authorization', 'Bearer YOUR_SERVICE_ROLE_KEY',
      'apikey', 'YOUR_SERVICE_ROLE_KEY'
    ),
    body := '{"limit":500}'::jsonb
  ) as request_id;
  $$
);
```

3. Re-run the [check query](#is-it-already-set-up) — you should see `lifecycle-daily-cron`.

**Change time:** edit `schedule` (cron syntax). Examples:

| Cron | When (UTC) |
|------|------------|
| `0 14 * * *` | 14:00 daily (default in docs) |
| `0 15 * * *` | 15:00 daily |
| `30 13 * * *` | 13:30 daily |

**Remove / replace job:**

```sql
select cron.unschedule('lifecycle-daily-cron');
-- then schedule again with updated SQL
```

---

## Option B — Dashboard Cron UI

1. Dashboard → **Integrations** → **Cron** (or **Edge Functions** → `lifecycle-daily-cron` → **Schedules**).
2. Create HTTP job:
   - **Method:** POST
   - **URL:** `https://wvclepquxxczgrukfqyr.supabase.co/functions/v1/lifecycle-daily-cron`
   - **Body:** `{"limit":500}`
   - **Header:** `Authorization: Bearer <service_role>`
   - **Schedule:** daily at your chosen UTC hour

If the UI is unavailable, use Option A.

---

## Manual test (before or after scheduling)

From repo root with `.env` loaded (`SUPABASE_URL`, `SUPABASE_KEY` = service role):

**Dry-run (no Brevo sends):**

```bash
curl -sS -X POST "$SUPABASE_URL/functions/v1/lifecycle-daily-cron" \
  -H "Authorization: Bearer $SUPABASE_KEY" \
  -H "Content-Type: application/json" \
  -d '{"dry_run":true,"limit":5}'
```

**Live send (cap 500 per trigger):**

```bash
curl -sS -X POST "$SUPABASE_URL/functions/v1/lifecycle-daily-cron" \
  -H "Authorization: Bearer $SUPABASE_KEY" \
  -H "Content-Type: application/json" \
  -d '{"limit":500}'
```

Single trigger only:

```bash
-d '{"dry_run":true,"limit":5,"triggers":["activation_cs_calendar"]}'
```

Expect HTTP **200** and JSON with `results[]` per trigger (`cohort_size`, `outcomes`).

---

## Verify after a run

### 1. pg_cron ran the HTTP call

```sql
select j.jobname, d.status, d.return_message, d.start_time, d.end_time
from cron.job_run_details d
join cron.job j on j.jobid = d.jobid
where j.jobname = 'lifecycle-daily-cron'
order by d.start_time desc
limit 10;
```

`status` should be `succeeded`. `return_message` often contains the `net.http_post` request id.

### 2. Edge function logged

Dashboard → **Edge Functions** → `lifecycle-daily-cron` → **Logs**  
Look for `POST | 200 | .../lifecycle-daily-cron` at the scheduled time (not only manual curls).

### 3. Sends recorded

```sql
select trigger_name, count(*) as n, max(sent_at) as last_sent
from cs_outreach_log
where trigger_name in ('activation_nudge_24h', 'activation_cs_calendar')
  and sent_at > now() - interval '7 days'
group by 1
order by 1;
```

After a **live** cron (not `dry_run`), eligible users get new rows. Re-running the same day should **not** duplicate (dedup in `cs_outreach_log`).

### 4. Cohort sanity (optional)

```sql
select count(*) from lifecycle_cohort_activation_nudge_24h(500);
select count(*) from lifecycle_cohort_activation_cs_calendar(500);
```

---

## Edge secrets checklist

Cron only **invokes** the function; Brevo sends still need Edge secrets:

- `BREVO_API_KEY`
- `LIFECYCLE_SENDER_EMAIL`, `LIFECYCLE_SENDER_NAME`
- `BREVO_TEMPLATE_ID_ACTIVATION_NUDGE`
- `BREVO_TEMPLATE_ID_ACTIVATION_CS_CALENDAR`
- `BREVO_TEMPLATE_ID_NPS_DAY3`
- `BREVO_TEMPLATE_ID_PMF_DAY10`

`supabase secrets list` on the linked project.

---

## Security note

`cron.job.command` stores the service role key in plain text (same as your existing `report-builder` job). Prefer SQL Editor for one-off setup; do not commit keys into this git repo. Rotating the service role requires updating the cron job command.

Optional: set `LIFECYCLE_INVOKE_SECRET` on Edge and use that bearer instead of the full service role in cron (see `_shared/auth.ts`).
