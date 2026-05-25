# Brevo Phase 1 setup and testing

End-to-end setup for the five Phase 1 lifecycle emails on Brevo. Uses **production naming** everywhere: list **Oasis Lifecycle**, automation **Oasis Phase 1**, templates **Oasis Welcome**, etc. (no QA prefix, no em dashes). See [`BREVO_NAMING.md`](BREVO_NAMING.md).

Signup in Oasis does **not** enroll in Brevo until you run the enroll script (or wire Oasis later).

**Test accounts:** `adamkershnerdev1@gmail.com`, `adamthewrite@gmail.com`  
**Manifest:** `launch_config.brevo_phase1` in [`public/email_sequences.json`](../public/email_sequences.json)

---

## Prerequisites

| Item | Notes |
|------|--------|
| Brevo account | Starter (or higher) recommended for automation volume |
| Domain / sender | Verified sender; **From name:** `Adam from Oasis` |
| API key | `BREVO_API_KEY` in `.env` (see [`.env.example`](../.env.example)) |
| Supabase | Service role for `scripts/enroll_brevo_phase1.py` user lookup |
| HTML sources | [`brevo-oasis-emails/lifecycle/`](../brevo-oasis-emails/lifecycle/) |
| Link reference | [`brevo-oasis-emails/brevo-oasis-email-links.js`](../brevo-oasis-emails/brevo-oasis-email-links.js) |

After creating the list in Brevo, set **one** of:

- `BREVO_LIFECYCLE_LIST_ID=<numeric>` in `.env`, or  
- `launch_config.brevo_phase1.list_id` in the manifest

Discover list IDs and confirm `.env` wiring:

```bash
.venv/bin/pip install brevo-python python-dotenv
.venv/bin/python scripts/verify_brevo_phase1.py
.venv/bin/python scripts/enroll_brevo_phase1.py --list-lists
```

`verify_brevo_phase1.py` checks `BREVO_API_KEY` + `BREVO_LIFECYCLE_LIST_ID` and prints the automation build checklist.

---

## Part A — Brevo UI (list, templates, automation)

### A.1 List

1. **Contacts → Lists → Create a list** (or rename existing list)
2. Name: **`Oasis Lifecycle`**
3. Until Oasis signup is wired, only add contacts via the enroll script or intentional test signups.
4. Copy the numeric **list ID** into `.env` or manifest (see above).

**Re-test reset:** Remove the contact from this list, or delete the contact in Brevo, before re-enrolling so the “added to list” automation can fire again.

### A.2 Five email templates (manual test send each)

Build each as a **campaign** or **automation email step** template. Use the **exact Brevo template name** below. Paste HTML + plain text; send yourself a **manual test** before activating the workflow.

| Order | Sequence ID | Brevo template name | Subject | HTML | Plain text |
|------|-------------|---------------------|---------|------|------------|
| 1 | `welcome` | **Oasis Welcome** | Welcome to Oasis | [`brevo-oasis-welcome.html`](../brevo-oasis-emails/lifecycle/brevo-oasis-welcome.html) | [`brevo-oasis-welcome-plain-text.txt`](../brevo-oasis-emails/lifecycle/brevo-oasis-welcome-plain-text.txt) |
| 2 | `activation_nudge` | **Oasis Activation Nudge** | Try your first AI command in Oasis | [`brevo-oasis-activation-nudge.html`](../brevo-oasis-emails/lifecycle/brevo-oasis-activation-nudge.html) | [`brevo-oasis-activation-nudge-plain-text.txt`](../brevo-oasis-emails/lifecycle/brevo-oasis-activation-nudge-plain-text.txt) |
| 3 | `activation_cs_calendar` | **Oasis Activation CS Calendar** | Need help getting started with Oasis? | [`brevo-oasis-activation-cs-calendar.html`](../brevo-oasis-emails/lifecycle/brevo-oasis-activation-cs-calendar.html) | [`brevo-oasis-activation-cs-calendar-plain-text.txt`](../brevo-oasis-emails/lifecycle/brevo-oasis-activation-cs-calendar-plain-text.txt) |
| 4 | `nps_day3` | **Oasis NPS** | Quick question: how likely are you to recommend Oasis? | [`brevo-oasis-nps-day3.html`](../brevo-oasis-emails/lifecycle/brevo-oasis-nps-day3.html) | [`brevo-oasis-nps-day3-plain-text.txt`](../brevo-oasis-emails/lifecycle/brevo-oasis-nps-day3-plain-text.txt) |
| 5 | `pmf_day10` | **Oasis PMF** | Help us understand how Oasis fits your workflow | [`brevo-oasis-pmf-day10.html`](../brevo-oasis-emails/lifecycle/brevo-oasis-pmf-day10.html) | [`brevo-oasis-pmf-day10-plain-text.txt`](../brevo-oasis-emails/lifecycle/brevo-oasis-pmf-day10-plain-text.txt) |

D&D specs: welcome, activation nudge, activation CS calendar (under `brevo-oasis-emails/lifecycle/`).

Copy details: [`brevo-oasis-lifecycle-emails.md`](../brevo-oasis-emails/lifecycle/brevo-oasis-lifecycle-emails.md). Previews: [Email Machine](https://oasis-analytics.vercel.app/email-machine) after `python3 reporting/build_static_site.py`.

Re-paste HTML + plain text after repo updates. Each email should show founder headshot before greeting, then `- Adam`, mantra callout, and **All my socials** + icons (see [`brevo-oasis-emails/README.md`](../brevo-oasis-emails/README.md)).

**NPS / PMF:** Follow [`brevo-oasis-nps-tally-form-setup.md`](../brevo-oasis-emails/lifecycle/brevo-oasis-nps-tally-form-setup.md). Preview with a test contact so `{{ contact.EMAIL }}` resolves.

### A.3 Automation — `Oasis Phase 1`

| Setting | Value |
|---------|--------|
| **Trigger** | Contact **added to list** → `Oasis Lifecycle` |
| **Entry** | All contacts on list (add filters when moving to production timing) |
| **Workflow** | Linear for first test; add conditionals when switching to production timing |

#### Initial test timing (same automation)

Use **1-minute waits** between steps while validating:

1. Send **Oasis Welcome**
2. Wait **1 minute** → Send **Oasis Activation Nudge**
3. Wait **1 minute** → Send **Oasis Activation CS Calendar**
4. Wait **1 minute** → Send **Oasis NPS**
5. Wait **1 minute** → Send **Oasis PMF**

Keep the workflow **inactive** until each template passes a manual test send; then **activate**.

Brevo often enforces a **1 minute** minimum wait (~4 minutes after welcome for emails 2–5).

#### Production timing (edit in place)

When QA passes, **edit the same** `Oasis Phase 1` workflow (do not clone under a new name):

| Step | Production timing | Initial test timing |
|------|-------------------|---------------------|
| Oasis Welcome | Immediate (D0) | T+0 |
| Oasis Activation Nudge | **1 day** if no `llm_usage` | T+1 min |
| Oasis Activation CS Calendar | **~2–3 days** if still stuck | T+2 min |
| Oasis NPS | Day 3 | T+3 min |
| Oasis PMF | Day 10 | T+4 min |

Add **conditions** on steps 2–3 (no usage / no training). Wire Oasis signup (see manifest `oasis_signup_integration.contract`).

**Out of scope for Phase 1 chain:** `limit_hitter_upgrade`, Paid Zen (add separate automations later).

---

## Part B — Repo enroll bridge

### Enroll after Oasis signup

```bash
.venv/bin/pip install brevo-python python-dotenv

.venv/bin/python scripts/verify_brevo_phase1.py

.venv/bin/python scripts/enroll_brevo_phase1.py --email you@example.com --dry-run

.venv/bin/python scripts/enroll_brevo_phase1.py --email adamkershnerdev1@gmail.com
```

The script:

1. Loads `BREVO_API_KEY` and list id from env or manifest  
2. Resolves the user via Supabase (`--email` and/or `--user-id`)  
3. Creates/updates the Brevo contact with `FIRSTNAME` and `OASIS_USER_ID`  
4. Adds the contact to **Oasis Lifecycle** (triggers **Oasis Phase 1**)

Shared module: `integrations.brevo_phase1.enroll_user_for_phase1`.

---

## Part C — Two-Gmail test procedure

1. **Prep:** Automation active; templates manually tested; `BREVO_LIFECYCLE_LIST_ID` in `.env` or manifest.  
2. **Clean slate** (re-test): Remove both Gmail addresses from the list / delete contacts in Brevo.  
3. **Sign up in Oasis** with `adamkershnerdev1@gmail.com` (new Supabase row).  
4. **Enroll:** `python3 scripts/enroll_brevo_phase1.py --email adamkershnerdev1@gmail.com`  
5. **Watch inbox** ~4–5 minutes (with 1-minute waits). Verify order, links, `{{ unsubscribe }}`.  
6. Repeat for `adamthewrite@gmail.com`.  
7. Fix HTML under `brevo-oasis-emails/` and refresh previews: `python3 reporting/build_static_site.py`

### Link checklist

| Link / element | URL / check |
|----------------|-------------|
| Docs | `https://kahana.co/docs` |
| Contact | `https://kahana.co/contact` |
| Slack | `https://kahanaworkspace.slack.com/archives/C0B3QDPLH4P` |
| NPS (Tally) | `https://tally.so/r/ODoBz7` / page `https://kahana.co/oasis-nps` |
| PMF (Tally) | `https://tally.so/r/EkNbXX` / page `https://kahana.co/oasis-pmf` |
| Installations | `https://kahana.co/installations` |
| Privacy | `https://kahana.co/privacy-policy` |
| Unsubscribe | Brevo `{{ unsubscribe }}` renders in preview |

---

## Risks

| Risk | Mitigation |
|------|------------|
| Re-test doesn’t re-fire | Remove from list / delete contact before re-enroll |
| Signup without script | Enroll script required until Oasis API wired |
| Nudge to active users | Add conditions when switching to production timing |
| NPS/PMF personalization | Brevo preview with test contact attributes |

---

## Related docs

- [`BREVO_NAMING.md`](BREVO_NAMING.md) — canonical template and list names  
- [USER_EMAIL_MACHINE_PROPOSAL.md](USER_EMAIL_MACHINE_PROPOSAL.md) — Phase 1 funnel  
- [OPERATIONAL_EMAIL_RUNBOOK.md](OPERATIONAL_EMAIL_RUNBOOK.md) — legal/incident (separate from lifecycle)
