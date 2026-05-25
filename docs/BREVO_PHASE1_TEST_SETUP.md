# Brevo Phase 1 setup and testing

> **Recommended path:** [`SUPABASE_LIFECYCLE_EMAIL_PLAN.md`](SUPABASE_LIFECYCLE_EMAIL_PLAN.md) — Supabase Edge Functions + cron trigger sends; Brevo supplies templates only. This doc is the **legacy Brevo automation** fallback (list + workflow).

Production-style **Oasis Phase 1** automation: real day-based waits and conditional sends driven by Supabase-backed contact attributes. No compressed “1-minute between all five emails” workflow.

See [`BREVO_NAMING.md`](BREVO_NAMING.md) for template and list names.

**Test accounts:** `adamkershnerdev1@gmail.com`, `adamthewrite@gmail.com`  
**Manifest:** `launch_config.brevo_phase1` in [`public/email_sequences.json`](../public/email_sequences.json)

---

## Philosophy

| Do | Don’t |
|----|--------|
| Manual **test send** each template once (layout, links, merge tags) | Run all five emails back-to-back in ~5 minutes |
| Build automation with **production timing + conditions** | Use 1-minute waits to “simulate” the funnel |
| Enroll **two cohorts** (stuck vs activated) and verify who gets nudge/CS | Assume one inbox proves every branch |
| **Sync attributes** from Supabase when product state changes | Expect Brevo to know `llm_usage` without sync |

Calendar waits (1 day, 3 days, 10 days) are intentional — you are validating triggers, not copy throughput.

---

## Prerequisites

| Item | Notes |
|------|--------|
| Brevo Starter+ | Automation with waits and conditions |
| `BREVO_API_KEY` | v3 key (`xkeysib-…`); IP allowlisted if required |
| `BREVO_LIFECYCLE_LIST_ID` | List **Oasis Lifecycle** (e.g. `72`) |
| Contact attributes | Boolean: **`HAS_FIRST_PROMPT`**, **`HAS_TRAINING`** (Brevo → Contacts → Settings) |
| Supabase | Service role for enroll + attribute sync |
| Templates | Five Phase 1 templates pasted from repo / Email Machine |

```bash
.venv/bin/pip install brevo-python python-dotenv
.venv/bin/python scripts/verify_brevo_phase1.py
```

---

## Part A — Brevo UI

### A.1 Contact attributes

Create (exact names, type **Boolean**):

| Attribute | Source | Used for |
|-----------|--------|----------|
| `HAS_FIRST_PROMPT` | `llm_usage` in Supabase | Skip activation nudge / CS when user already prompted |
| `HAS_TRAINING` | `feedback_events` in Supabase | Skip CS calendar when user trained assistant |
| `FIRSTNAME` | user name | Personalization (already used) |
| `OASIS_USER_ID` | users.user_id | Debugging / future sync |

Enroll and [`scripts/sync_brevo_contact_attributes.py`](../scripts/sync_brevo_contact_attributes.py) set the two boolean flags from live data.

### A.2 Templates

Manual **test send** each template to yourself before activating the workflow (subjects/HTML in [`BREVO_NAMING.md`](BREVO_NAMING.md)). That is the only “fast” copy check.

### A.3 Automation — `Oasis Phase 1` (production logic)

| Setting | Value |
|---------|--------|
| **Trigger** | Contact **added to list** → **Oasis Lifecycle** |
| **From name** | `Adam from Oasis` on every send step |

**Recommended step graph** (single workflow; adjust labels to match your Brevo UI):

```text
[Added to Oasis Lifecycle]
  → Send Oasis Welcome (immediately)

  → Wait 1 day
  → IF HAS_FIRST_PROMPT is false
      → Send Oasis Activation Nudge

  → Wait 2 days   (contact is now ~day 3 from list entry)
  → IF HAS_FIRST_PROMPT is false AND HAS_TRAINING is false
      → Send Oasis Activation CS Calendar

  → Send Oasis NPS
      (exclude unsubscribed; no “has prompt” gate — all signups get NPS at day 3)

  → Wait 7 days   (day 10 from list entry)
  → Send Oasis PMF
      (exclude unsubscribed)
```

**Repo trigger contract** (for comparison):

| Step | Sequence ID | Timing | Condition |
|------|-------------|--------|-----------|
| Welcome | `welcome` | Immediate on list add | — |
| Activation nudge | `activation_nudge` | 24h after signup | `users_with_first_prompt == false` |
| Activation CS | `activation_cs_calendar` | ~day 3 | Still no prompt **and** no training |
| NPS | `nps_day3` | Day 3 | Unsubscribed excluded |
| PMF | `pmf_day10` | Day 10 | Unsubscribed excluded |

Keep workflow **inactive** until templates pass manual test send. **Activate** when ready for real calendar testing.

**Re-test reset:** Remove contact from **Oasis Lifecycle** or delete the contact before re-enrolling so “added to list” fires again.

---

## Part B — Repo bridge

### Enroll (sets attributes + list add → starts automation)

```bash
.venv/bin/python scripts/enroll_brevo_phase1.py --email you@example.com --dry-run
.venv/bin/python scripts/enroll_brevo_phase1.py --email adamkershnerdev1@gmail.com
```

Dry-run prints `activation_attributes` (`HAS_FIRST_PROMPT`, `HAS_TRAINING`) from Supabase at enroll time.

### Sync attributes after product usage

When a test user sends their first prompt or completes training **after** enroll, refresh Brevo before the next conditional wait:

```bash
.venv/bin/python scripts/sync_brevo_contact_attributes.py --email you@example.com
```

---

## Part C — Trigger validation (two cohorts)

Use two Gmail test accounts that exist in Supabase.

### Cohort A — “Stuck” (should get nudge + CS)

1. Pick a user with **no** `llm_usage` rows (or use a fresh signup).
2. Delete/remove Brevo contact; enroll: `enroll_brevo_phase1.py --email A`.
3. Confirm dry-run/enroll shows `HAS_FIRST_PROMPT: false`, `HAS_TRAINING: false`.
4. **Expect:** Welcome immediately → nudge ~24h later → CS ~day 3 if still stuck → NPS ~day 3 → PMF ~day 10.

### Cohort B — “Activated” (should skip nudge + CS)

1. Pick a user with **≥1** `llm_usage` row (or prompt once after enroll, then sync).
2. Reset Brevo contact; enroll with `HAS_FIRST_PROMPT: true`.
3. **Expect:** Welcome only from activation branch → **no** nudge, **no** CS → still NPS + PMF on calendar days.

### Mid-test activation

1. Enroll cohort A.
2. In Oasis, send first AI command.
3. Run `sync_brevo_contact_attributes.py` before the 24h nudge wait elapses.
4. **Expect:** Nudge does **not** send; CS branch should also stay off if training happened.

Track results in Brevo contact timeline + inbox. Full chain spans **~10 calendar days** — that is expected.

---

## Part D — What to check

| Check | Pass criteria |
|-------|----------------|
| Welcome trigger | Email within minutes of enroll |
| Nudge conditional | Only cohort A; suppressed after sync on B |
| CS conditional | Only A at day 3 if still no prompt/training |
| NPS / PMF | Both cohorts ~day 3 and ~day 10 |
| Attributes | Brevo contact shows booleans matching Supabase |
| Links / unsubscribe | Per link checklist in prior runs |

---

## Risks

| Risk | Mitigation |
|------|------------|
| Stale attributes | Re-run `sync_brevo_contact_attributes.py` after product events |
| Re-test doesn’t fire | Remove from list / delete contact before re-enroll |
| Waits still run when branch skipped | Brevo still advances calendar waits; conditions only gate **sends** |
| 10-day test cycle | Use two cohorts in parallel; don’t compress timing |

---

## Related

- [`BREVO_NAMING.md`](BREVO_NAMING.md)
- `integrations.brevo_phase1.enroll_user_for_phase1`
- [Email Machine](https://oasis-analytics.vercel.app/email-machine) — copy HTML
