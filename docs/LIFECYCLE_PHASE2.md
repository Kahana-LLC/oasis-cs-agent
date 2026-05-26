# Lifecycle Phase 2+ (Supabase Edge + Brevo)

Extends Phase 1 with monetization, conversion, and enterprise emails. Same architecture: **Supabase cohort SQL → Edge cron/webhook → Brevo transactional templates → `cs_outreach_log` dedup**.

**Migration:** `supabase/migrations/20260526200000_lifecycle_phase2_cohorts.sql`  
**Daily cron:** `lifecycle-daily-cron` (Phase 1 + Phase 2 triggers)  
**Plan webhook:** `lifecycle-on-user-plan` (`user_plans` INSERT/UPDATE)

---

## Triggers

| `dedup_trigger_name` | Channel | Brevo template (create in UI) | Env secret |
|----------------------|---------|-------------------------------|------------|
| `limit_hitter_upgrade` | cron | Oasis Limit Hitter D0 | `BREVO_TEMPLATE_ID_LIMIT_HITTER_D0` |
| `limit_hitter_upgrade_d7` | cron | Oasis Limit Hitter D7 | `BREVO_TEMPLATE_ID_LIMIT_HITTER_D7` |
| `upgrade_thank_you` | webhook | Oasis Paid Zen Welcome | `BREVO_TEMPLATE_ID_UPGRADE_THANK_YOU` |
| `cancelled_winback` | webhook | Oasis Cancelled Win-back D0 | `BREVO_TEMPLATE_ID_CANCELLED_D0` |
| `cancelled_winback_d14` | cron | Oasis Cancelled Win-back D14 | `BREVO_TEMPLATE_ID_CANCELLED_D14` |
| `at_risk_nurture_d0` … `d21` | cron | Oasis At-risk D0/D7/D14/D21 | `BREVO_TEMPLATE_ID_AT_RISK_D*` |
| `dead_resurrection_d0` | cron (cap 20/mo) | Oasis Dead Resurrection D0 | `BREVO_TEMPLATE_ID_DEAD_D0` |
| `dead_resurrection_d14` | cron | Oasis Dead Resurrection D14 | `BREVO_TEMPLATE_ID_DEAD_D14` |
| `return_reinforcement` | cron | Oasis Return Reinforcement | `BREVO_TEMPLATE_ID_RETURN_REINFORCEMENT` |
| `enterprise_founder` | cron | Oasis Enterprise Founder | `BREVO_TEMPLATE_ID_ENTERPRISE_FOUNDER` |
| `enterprise_expansion` | cron | Oasis Enterprise Expansion | `BREVO_TEMPLATE_ID_ENTERPRISE_EXPANSION` |

**Operational** (`legal_notice`, `incident_notice`): use `scripts/send_operational.py` — Resend Pro backup until SES production is approved. Not wired to Edge.

---

## Deploy checklist

1. **Apply migration** on Oasis Supabase (SQL editor or `supabase db push`).
2. **Create Brevo templates** from `brevo-oasis-emails/` HTML (see [`BREVO_NAMING.md`](BREVO_NAMING.md)).
3. **Set Edge secrets** for all `BREVO_TEMPLATE_ID_*` above + existing Phase 1 secrets.
4. **Deploy functions:** `lifecycle-daily-cron`, `lifecycle-send`, `lifecycle-on-user-plan`.
5. **Webhook:** Database → Webhooks → `user_plans` INSERT + UPDATE → `lifecycle-on-user-plan` URL, Bearer service role.
6. **Cron:** existing `lifecycle-daily-cron` job unchanged (function body now runs Phase 2 cohorts).
7. **Dry-run:**  
   `curl -X POST "$SUPABASE_URL/functions/v1/lifecycle-daily-cron" -H "Authorization: Bearer $SERVICE_ROLE" -H "Content-Type: application/json" -d '{"dry_run":true,"triggers":["limit_hitter_upgrade"]}'`

---

## Cohort rules (summary)

- **Limit hitter:** `llm_daily_usage.total_tokens` ≥ effective daily limit; has `llm_usage`; not on active paid `user_plans`.
- **At-risk nurture:** DAU bucket `at_risk_wau` / `at_risk_mau` via `lifecycle_user_bucket()`; follow-ups 7/14/21 days after D0 send.
- **Dead resurrection:** bucket `dead`; D0 capped at 20 new users per calendar month; no resurrection email in prior 30 days.
- **Return reinforcement:** bucket transition into `reactivated` or `resurrected` (today vs yesterday).
- **Enterprise:** company email (non-consumer domain); lifecycle day 7–8 + ≥2 sessions (founder), or 14–15 + ≥4 sessions (expansion).

---

## Manual test (single user)

```bash
# After templates + secrets are set
python scripts/send_lifecycle_email.py --trigger limit_hitter_upgrade --email you@example.com --dry-run
```

Or POST to `lifecycle-send` with `{ "trigger_name": "at_risk_nurture_d0", "email": "..." }`.
