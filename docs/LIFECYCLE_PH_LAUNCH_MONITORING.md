# Product Hunt launch — lifecycle email monitoring

**Pre-launch QA (day before PH):** [`LIFECYCLE_QA_PRE_LAUNCH.md`](LIFECYCLE_QA_PRE_LAUNCH.md) — full pass/fail matrix for another engineer.

Runbook for PH week: verify sends, read the analytics dashboard, and fix gaps.

**Dashboard:** [oasis-analytics](https://oasis-analytics.vercel.app/) — sections **Email delivery health**, **Phase 1 lifecycle sends**, **DAU model**, **Email exposure × DAU buckets**.

**Email Machine:** [/email-machine#supabase-lifecycle](https://oasis-analytics.vercel.app/email-machine#supabase-lifecycle) — same delivery table when live API is configured.

---

## Before launch (one-time)

| Check | Action |
|-------|--------|
| Welcome webhook | Sign up test user → `cs_outreach_log` row `welcome_email` within minutes |
| Vercel env | `SUPABASE_URL` + `SUPABASE_KEY` (service role) on oasis-analytics |
| Cron scheduled | SQL: `select jobname, schedule, active from cron.job where jobname = 'lifecycle-daily-cron'` |
| Brevo templates | 54–57 pasted; Edge secrets set |
| Dry-run cron | See below |

---

## Daily during PH week

1. Hard-refresh dashboard — confirm **Source: live (Supabase)**.
2. **Key insights** — act on any **missed** or **cron stale** cards.
3. **Email delivery health** — `Missed overdue` should stay **0**; `Due now` may be &gt; 0 until cron runs.
4. **DAU model** — watch `bucket_new`, `flow_NURR`, `flow_CURR`, `bucket_current`.
5. **Email exposure × buckets** — directional compare (V1, not causal).

---

## Dry-run cron (no Brevo sends)

```bash
curl -sS -X POST "$SUPABASE_URL/functions/v1/lifecycle-daily-cron" \
  -H "Authorization: Bearer $SUPABASE_KEY" \
  -H "Content-Type: application/json" \
  -d '{"dry_run":true,"limit":10}'
```

---

## Verify cron ran

```sql
select j.jobname, d.status, d.start_time, d.end_time
from cron.job_run_details d
join cron.job j on j.jobid = d.jobid
where j.jobname = 'lifecycle-daily-cron'
order by d.start_time desc
limit 5;
```

```sql
select trigger_name, count(*) as sends, max(sent_at) as last_send
from cs_outreach_log
group by trigger_name
order by trigger_name;
```

---

## If `Missed overdue` &gt; 0

| Trigger | Likely cause |
|---------|----------------|
| `welcome_email` | `lifecycle-on-signup` webhook not firing; check Oasis `users` INSERT |
| Cron emails | pg_cron failed; Edge error; Brevo API; or **500 cap** per run |

**500 cap:** Each cron trigger processes at most 500 users. If PH adds &gt;500 eligible users in one day, increase `limit` in the cron job body or run cron twice.

---

## Related docs

- [`LIFECYCLE_DAILY_CRON.md`](LIFECYCLE_DAILY_CRON.md)
- [`SUPABASE_LIFECYCLE_EMAIL_PLAN.md`](SUPABASE_LIFECYCLE_EMAIL_PLAN.md)
- [`VERCEL_DEPLOY.md`](VERCEL_DEPLOY.md)
