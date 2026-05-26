# Supabase lifecycle email plan (Phase 1)

**Recommended architecture** for Oasis Phase 1 lifecycle email: Supabase owns **when** and **who**; Brevo owns **how** (templates, deliverability, unsubscribe).

Replaces the primary reliance on **Brevo automation** (`Oasis Phase 1` list trigger + day waits + synced contact attributes). Brevo automations remain optional for PH waitlist or manual experiments.

**UI:** [Email Machine → Supabase lifecycle plan](https://oasis-analytics.vercel.app/email-machine#supabase-lifecycle)  
**Manifest:** `launch_config.supabase_lifecycle_email` in [`public/email_sequences.json`](../public/email_sequences.json)

---

## Why

| Problem with Brevo-only automations | Edge + cron fix |
|-------------------------------------|-----------------|
| Product state (`llm_usage`, training) lives in Supabase | Query Supabase at send time — no `HAS_FIRST_PROMPT` sync |
| Testing real triggers takes calendar days | Invoke function or cron manually with test user |
| One workflow mixes timing + conditions | Each `trigger_name` is explicit code + SQL |
| Signup not wired | `users` INSERT webhook fires welcome immediately |

This repo’s CS agent ([`PLAN.md`](../PLAN.md)) already assumes **`cs_outreach_log`** dedup and rule-based triggers ([`triggers/evaluate.py`](../triggers/evaluate.py)). Edge functions are the production wiring for Phase 1 sends.

---

## Architecture

```text
Oasis Supabase
  users (INSERT) ──webhook──► edge: lifecycle-on-signup ──► Brevo send (Oasis Welcome)
  pg_cron / Supabase Cron (daily)
       └──► edge: lifecycle-daily-cron
              ├── SQL: activation_nudge_24h cohort
              ├── SQL: activation_cs_calendar_d3 cohort
              ├── SQL: nps_day3 cohort
              └── SQL: pmf_day10 cohort
              each → dedup cs_outreach_log → Brevo transactional template send

Brevo
  Templates: Oasis Welcome, Activation Nudge, … (names in BREVO_NAMING.md)
  API: POST transactional / smtp email with templateId

oasis-cs-agent (this repo)
  brevo-oasis-emails/     HTML source of truth
  integrations/brevo_phase1.py   Python reference for enroll + send patterns
  Email Machine           Plan + inventory + previews
```

**Deploy location:** Edge Functions and cron live in the **Oasis app Supabase project** (not Vercel). This analytics repo holds the spec, templates, and reference integration.

---

## Prerequisites

| Item | Owner | Notes |
|------|--------|------|
| `cs_outreach_log` table | Supabase migration | See [`PLAN.md`](../PLAN.md) §6.2 |
| Brevo templates + template IDs | Brevo UI | Map in Edge Function secrets or config table |
| `BREVO_API_KEY` | Supabase secrets | v3 `xkeysib-`; allowlist Supabase egress IPs or disable IP lock for server |
| Service role | Edge Functions only | Never expose to browser |
| `outreach_log` check | Edge Function | Skip send if `(user_id, trigger_name)` exists |

---

## Phase 1 triggers (canonical)

| `dedup_trigger_name` | Sequence ID | Brevo template | When | SQL / event condition |
|----------------------|-------------|----------------|------|------------------------|
| `welcome_email` | `welcome` | Oasis Welcome | On signup | `users` INSERT (active user) |
| `activation_nudge_24h` | `activation_nudge` | Oasis Activation Nudge | 24h after signup | No row in `llm_usage` for `user_id` |
| `activation_cs_calendar` | `activation_cs_calendar` | Oasis Activation CS Calendar | Day 3 window | No `llm_usage` and no `feedback_events` for `user_id` |
| `nps_day3` | `nps_day3` | Oasis NPS | Day 3 after signup | `created_at` + 3d ≤ now; not in outreach_log |
| `pmf_day10` | `pmf_day10` | Oasis PMF | Day 10 after signup | `created_at` + 10d ≤ now; not in outreach_log |

Use **ranges** where the repo specifies them (e.g. `lifecycle_day` 3–4) to survive a missed cron day — mirror [`triggers/evaluate.py`](../triggers/evaluate.py) patterns.

**Unsubscribed / paid:** Before send, exclude contacts unsubscribed in Brevo and users on paid plan (query `user_plans` / `plan_id`).

---

## Edge Functions (Oasis repo)

### 1. `lifecycle-send` (shared)

**Input:** `{ user_id, trigger_name, template_key }`  
**Steps:**

1. Load user email, name from `users`.
2. If `was_triggered(user_id, trigger_name)` → return `{ skipped: true }`.
3. Resolve Brevo template ID from config.
4. Call Brevo API (transactional email with template + params: `FIRSTNAME`, `EMAIL`).
5. Insert `cs_outreach_log` row (`channel: email`, `provider: brevo`).
6. Optionally upsert Brevo contact (no list automation required).

Reference implementation: [`integrations/brevo_phase1.py`](../integrations/brevo_phase1.py) (extend with `send_transactional_template`).

### 2. `lifecycle-on-signup`

- **Trigger:** Database webhook on `public.users` INSERT (or auth.users → users sync).
- **Action:** `lifecycle-send` with `welcome_email`.
- **Idempotent:** dedup table prevents double welcome on replay.

### 3. `lifecycle-daily-cron`

- **Trigger:** Supabase Cron `0 14 * * *` (or pg_cron) — pick UTC hour for US morning.
- **Action:** Run cohort queries; for each row call `lifecycle-send` for applicable triggers.
- **Batch limit:** Cap sends per run (e.g. 500) to respect Brevo daily limits; log overflow.

**Auth:** Cron invokes function with `Authorization: Bearer <service_role or cron secret>`.

---

## SQL cohort sketches

```sql
-- Activation nudge: signed up ≥24h ago, never prompted
select u.user_id, u.email
from users u
where u.status = 'active'
  and u.created_at <= now() - interval '24 hours'
  and u.created_at > now() - interval '25 hours'  -- optional narrow window, or use day bucket
  and not exists (select 1 from llm_usage lu where lu.user_id = u.user_id)
  and not exists (
    select 1 from cs_outreach_log o
    where o.user_id = u.user_id and o.trigger_name = 'activation_nudge_24h'
  );
```

Widen windows in production (`created_at <= now() - interval '24 hours'` without upper bound) and rely on dedup only.

---

## Testing (no 10-day Brevo wait)

| Test | How |
|------|-----|
| Welcome | Insert test user or invoke `lifecycle-on-signup` with fixture payload |
| Nudge | User with old `created_at`, no `llm_usage`; run daily cron once |
| Skip nudge | Same user after one `llm_usage` row; cron should not send |
| Dedup | Run cron twice; second run skips |
| Templates | Brevo manual test send + Email Machine copy HTML |

Keep [`scripts/enroll_brevo_phase1.py`](../scripts/enroll_brevo_phase1.py) as **dev fallback** (Brevo contact + list) until Edge path is live.

---

## Step-by-step (one email at a time)

| Step | Email | Runbook | Status |
|------|--------|---------|--------|
| **1** | Welcome | [`LIFECYCLE_WELCOME.md`](LIFECYCLE_WELCOME.md) | Shipped — webhook + live signup verified |
| **2** | Activation nudge | [`LIFECYCLE_ACTIVATION_NUDGE.md`](LIFECYCLE_ACTIVATION_NUDGE.md) | Shipped — tested |
| **3** | Activation CS calendar | [`LIFECYCLE_ACTIVATION_CS_CALENDAR.md`](LIFECYCLE_ACTIVATION_CS_CALENDAR.md) | Shipped |
| **4** | NPS day 3 | [`LIFECYCLE_NPS_DAY3.md`](LIFECYCLE_NPS_DAY3.md) | Shipped |
| **5** | PMF day 10 | [`LIFECYCLE_PMF_DAY10.md`](LIFECYCLE_PMF_DAY10.md) | Shipped |

---

## Implementation checklist

| # | Task | Repo / project | Status |
|---|------|----------------|--------|
| 1 | Create `cs_outreach_log` (+ RLS if needed) | Oasis Supabase | pending |
| 2 | Map Brevo template name → numeric template ID in config | Oasis Supabase secrets | pending |
| 3 | Implement `lifecycle-send` (TypeScript) | Oasis `supabase/functions` | pending |
| 4 | Webhook `lifecycle-on-signup` | Oasis Supabase | pending |
| 5 | Cron `lifecycle-daily-cron` + cohort SQL | Oasis Supabase | pending |
| 6 | Port cohort logic from `triggers/evaluate.py` / manifest | This repo spec | in progress |
| 7 | Wire signup in Oasis app to fire webhook | Oasis app | pending |
| 8 | Deprecate **Oasis Phase 1** Brevo automation (optional) | Brevo UI | optional |
| 9 | Document template IDs in manifest | `email_sequences.json` | pending |

---

## Brevo vs Supabase responsibilities

| Concern | Owner |
|---------|--------|
| HTML / subject / preheader | This repo → paste into Brevo templates |
| Template IDs | Oasis Edge config |
| Send timing & conditions | Supabase SQL + Edge |
| Dedup | `cs_outreach_log` |
| Unsubscribe | Brevo template footer + blacklist API |
| Marketing list **Oasis Lifecycle** | Optional segment sync; not required for sends |

---

## Related

- [`BREVO_NAMING.md`](BREVO_NAMING.md) — template names  
- [`BREVO_PHASE1_TEST_SETUP.md`](BREVO_PHASE1_TEST_SETUP.md) — legacy Brevo automation test (fallback)  
- [`PLAN.md`](../PLAN.md) — CS agent + outreach_log  
- [`integrations/brevo_phase1.py`](../integrations/brevo_phase1.py) — enroll + attribute sync (bridge)
