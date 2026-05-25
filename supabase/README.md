# Supabase (Oasis project)

Migrations and Edge Functions for lifecycle email. Deploy against the **Oasis app** Supabase project (not the analytics Vercel site).

| Path | Purpose |
|------|---------|
| [`migrations/20260525140000_cs_outreach_log.sql`](migrations/20260525140000_cs_outreach_log.sql) | Email dedup table |
| [`functions/lifecycle-send/`](functions/lifecycle-send/) | Invoke send by `user_id` / `email` |
| [`functions/lifecycle-on-signup/`](functions/lifecycle-on-signup/) | `users` INSERT webhook → welcome |
| [`functions/_shared/`](functions/_shared/) | Brevo + outreach helpers |

**Welcome runbook:** [`docs/LIFECYCLE_WELCOME.md`](../docs/LIFECYCLE_WELCOME.md)
