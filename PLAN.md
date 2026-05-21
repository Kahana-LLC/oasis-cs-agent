# Kahana CS Agent — Engineering Plan

> Engineering reference for the Oasis CS Agent. Single source of truth for build decisions,
> folder structure, data models, trigger logic, and open items.
> Last updated: Phase 0 complete + db/fetch.py done. Next: pipeline/metrics.py (Phase 1).

---

## 1. What We're Building

A Python daily batch job that runs once every 24 hours and processes every Oasis user through
a pipeline:

1. Pull data from Supabase (`users`, `llm_usage`, `llm_daily_usage`, `sessions`)
2. Compute per-user metrics (lifecycle day, session count, session gap, command diversity, etc.)
3. Classify each user into one of 4 segments: Healthy / At-Risk / High-Value / Inactive
4. Evaluate lifecycle triggers against the trigger map (keyed to phase + metric thresholds)
5. Check the outreach log to prevent duplicate contacts
6. Select and execute the correct playbook (email, in-app nudge, or team alert)
7. Log every action taken
8. Emit a daily cohort health report

The intelligence is primarily **rule-based** (deterministic thresholds). Claude is used only for
generating personalised outreach copy — the trigger logic never delegates to the model.

---

## 2. Stack

| Layer              | Tool                                      |
|--------------------|-------------------------------------------|
| Language           | Python 3.12                               |
| Database           | Supabase (`supabase-py`)                  |
| Agent framework    | Pydantic AI (`pydantic-ai[anthropic]`)    |
| Message generation | Claude claude-sonnet-4-6 via Pydantic AI  |
| Email delivery     | Brevo                                     |
| In-app messages    | Write to Supabase → Oasis frontend reads  |
| Team alerts        | Email via Brevo to `ALERT_EMAIL`          |
| Package manager    | uv                                        |
| Scheduling         | GitHub Actions cron                       |

---

## 3. Folder Structure

```
csagent/
├── .env                          # never committed
├── .env.example                  # committed, no real values
├── pyproject.toml
├── main.py                       # orchestrates all phases
├── db/
│   ├── __init__.py
│   ├── client.py                 # shared Supabase client singleton
│   ├── fetch.py                  # fetch_users(), fetch_usage(), fetch_daily_usage(), fetch_sessions()
│   └── outreach_log.py           # was_triggered(), log_outreach()
├── models/
│   ├── __init__.py
│   ├── db.py                     # User, LLMUsage, LLMDailyUsage, Session, Plan
│   ├── metrics.py                # UserMetrics, UserSegment
│   └── actions.py                # TriggerResult, EmailContent, OutreachLogEntry
├── pipeline/
│   ├── __init__.py
│   └── metrics.py                # compute_metrics() → UserMetrics per user
├── classifier/
│   ├── __init__.py
│   └── segment.py                # classify_segment() → UserSegment
├── triggers/
│   ├── __init__.py
│   └── evaluate.py               # one function per trigger, each returns bool
├── actions/
│   ├── __init__.py
│   ├── message_gen.py            # Pydantic AI agent → EmailContent
│   ├── email.py                  # send_email() via Brevo
│   ├── inapp.py                  # write to cs_inapp_messages
│   └── alert.py                  # send team alert email via Brevo
├── reporting/
│   ├── __init__.py
│   └── cohort_report.py          # daily cohort health summary
└── .github/
    └── workflows/
        └── daily_run.yml
```

> Note: `pipeline/join_rows.py` and `pipeline/sessions.py` from the original plan are
> **removed**. Session tracking is a real table (`sessions`) and `command_type` is a direct
> column on `llm_usage` — no row-pair joining required.

---

## 4. Dependencies

```bash
uv add pydantic-ai[anthropic] supabase brevo-python python-dotenv pandas
```

---

## 5. Environment Variables

```bash
# .env — never commit this file
SUPABASE_URL=
SUPABASE_KEY=            # service_role key, not anon — bypasses RLS
ANTHROPIC_API_KEY=
BREVO_API_KEY=
ALERT_EMAIL=             # internal team email for high-value alerts and cohort report
FROM_EMAIL=              # verified Brevo sending address e.g. hello@useoasis.co
FROM_NAME=               # e.g. "Archit from Oasis"
```

---

## 6. Database

### 6.1 Existing Tables (read-only)

#### `users` — 122 rows (as of 2026-05-21)
| Column                       | Type             | Notes                                          |
|------------------------------|------------------|------------------------------------------------|
| user_id                      | uuid PK          |                                                |
| name                         | varchar nullable | **100% populated** — use this for outreach     |
| full_name                    | text nullable    | Only 60% populated — fallback only             |
| email                        | varchar not null | Used for outreach and company_domain check     |
| created_at                   | timestamp (no tz)| **Day 0 anchor** — treat as UTC, 100% populated|
| last_login                   | timestamp (no tz)| nullable                                       |
| status                       | varchar          | `'active'` \| `'suspended'` — filter to active |
| payment_status               | text nullable    |                                                |
| plan_id                      | text nullable FK | `'Free'` or `'Plus'`                           |
| opt_in_personalized_training | boolean          | default false                                  |

#### `plan` — 2 rows (referenced by `users.plan_id`)
| plan_id | price_monthly | price_yearly | limit_daily   | limit_monthly |
|---------|---------------|--------------|---------------|---------------|
| Free    | 0             | 0            | 100,000 tokens| 150,000 tokens|
| Plus    | 20            | 200          | 1,000,000 tokens | 3,000,000 tokens |

> Note: A separate `plans` table (UUID PKs) exists linked via `user_plans` — this appears to be
> a Stripe/billing system. For CS agent segmentation, use `users.plan_id → plan` (text IDs).

#### `sessions` — 1,616 rows (as of 2026-05-21)
| Column     | Type             | Notes                          |
|------------|------------------|--------------------------------|
| session_id | uuid PK          |                                |
| user_id    | uuid FK          |                                |
| started_at | timestamp (no tz)|                                |
| ended_at   | timestamp (no tz)| nullable — null = still active |
| device_info| jsonb nullable   |                                |

> **This eliminates the need for 30-minute inactivity inference.** Session count and session
> gap are computed directly from this table.

#### `llm_usage` — 3,618 rows (as of 2026-05-21, active, still being written to)
| Column          | Type       | Notes                                                    |
|-----------------|------------|----------------------------------------------------------|
| usage_id        | uuid PK    |                                                          |
| user_id         | uuid FK    |                                                          |
| timestamp       | timestamp  | When the command was run                                 |
| usage_date      | date       | Date portion for easy grouping                           |
| model_used      | varchar    | e.g. `gemini-2.5-flash`                                  |
| command_type    | text       | **Direct column** — see enum values below                |
| user_intent     | text       | nullable — free text description of user's goal          |
| tokens_used     | int        |                                                          |
| input_tokens    | bigint     |                                                          |
| output_tokens   | bigint     |                                                          |
| total_tokens    | bigint     |                                                          |
| usage_count     | int        |                                                          |
| success         | boolean    | nullable                                                 |
| latency_ms      | int        | nullable                                                 |
| prompt_summary  | text       | nullable                                                 |
| interaction_id  | uuid       | nullable — links related rows within one interaction     |
| interaction_data| jsonb      | nullable                                                 |

**`command_type` enum values** (from live data):
| Value             | Count |
|-------------------|-------|
| navigation        | 274   |
| system            | 252   |
| search            | 219   |
| info_retrieval    | 197   |
| other             | 181   |
| organization      | 178   |
| content_transform | 170   |
| help              | 60    |
| automation        | 7     |

> No two-row join needed. `command_type` is a direct column. `interaction_id` links
> related rows within a single interaction but is not required for metric computation.

#### `llm_daily_usage` — 58 rows (as of 2026-05-21)
| Column        | Type      | Notes                                    |
|---------------|-----------|------------------------------------------|
| user_id       | uuid PK   | Composite PK with usage_date             |
| usage_date    | date PK   |                                          |
| input_tokens  | bigint    | default 0                                |
| output_tokens | bigint    | default 0                                |
| total_tokens  | bigint    | default 0                                |
| request_count | int       | Commands run that day — key metric       |
| updated_at    | timestamp |                                          |

> **No command_type here** — daily aggregates only. Use `llm_usage` for command diversity
> and dominant command type. Use `llm_daily_usage` for weekly_requests and token trends.

#### `feedback_events` — 311 rows (as of 2026-05-21)
| Column          | Type      | Notes                                           |
|-----------------|-----------|-------------------------------------------------|
| feedback_id     | uuid PK   |                                                 |
| user_id         | uuid FK   |                                                 |
| session_id      | uuid FK   |                                                 |
| negative_rating | boolean   | **At-risk signal** — user explicitly rated bad  |
| category        | text      | nullable                                        |
| reported_at     | timestamptz |                                               |

> Useful as an at-risk signal not in the original plan. Users with `negative_rating = true`
> in the last 7 days should be flagged at-risk regardless of session frequency.

### 6.2 New Tables (create before first run)

Run in Supabase SQL Editor:

```sql
-- Dedup gate: checked before every send, written after every send
create table cs_outreach_log (
  id               uuid default gen_random_uuid() primary key,
  user_id          uuid not null,
  trigger_name     text not null,
  channel          text not null,   -- 'email' | 'in_app' | 'alert'
  sent_at          timestamptz default now(),
  message_preview  text
);

-- In-app nudges: written by CS agent, read by Oasis frontend
create table cs_inapp_messages (
  id           uuid default gen_random_uuid() primary key,
  user_id      uuid not null,
  message      text not null,
  trigger_name text,
  created_at   timestamptz default now(),
  read_at      timestamptz
);

-- RLS policy: frontend reads own messages only
alter table cs_inapp_messages enable row level security;
create policy "users read own messages"
  on cs_inapp_messages for select
  using (auth.uid() = user_id);
```

---

## 7. Data Models

### `models/db.py`

```python
class User(BaseModel):
    model_config = ConfigDict(extra='allow')
    user_id: UUID
    email: str
    name: str | None = None          # 100% populated — use for outreach
    full_name: str | None = None     # 60% populated — fallback
    created_at: datetime             # Day 0 anchor, treat as UTC
    status: str | None = None
    payment_status: str | None = None
    plan_id: str | None = None       # 'Free' | 'Plus'

class Plan(BaseModel):
    plan_id: str                     # 'Free' | 'Plus'
    price_monthly: int
    limit_daily: int | None = None
    limit_monthly: int | None = None

class Session(BaseModel):
    model_config = ConfigDict(extra='allow')
    session_id: UUID
    user_id: UUID
    started_at: datetime
    ended_at: datetime | None = None

class LLMUsage(BaseModel):
    model_config = ConfigDict(extra='allow')
    usage_id: UUID
    user_id: UUID
    timestamp: datetime
    usage_date: date | None = None
    model_used: str | None = None
    command_type: str | None = None
    user_intent: str | None = None
    total_tokens: int | None = None
    success: bool | None = None

class LLMDailyUsage(BaseModel):
    model_config = ConfigDict(extra='allow')
    user_id: UUID
    usage_date: date
    request_count: int = 0
    total_tokens: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
```

### `models/metrics.py`

```python
class UserSegment(str, Enum):
    healthy    = "healthy"
    at_risk    = "at_risk"
    high_value = "high_value"
    inactive   = "inactive"

class UserMetrics(BaseModel):
    user_id:                UUID
    lifecycle_day:          int        # today - created_at
    active_days_total:      int        # distinct usage_date in llm_daily_usage
    active_days_last_7:     int
    active_days_last_30:    int
    session_count:          int        # from sessions table (started_at)
    session_gap:            int        # days since last session.started_at
    days_since_last_active: int
    last_active_date:       date | None
    command_diversity:      int        # distinct command_type in llm_usage
    weekly_requests:        int        # sum request_count last 7 days
    weekly_requests_prev:   int        # sum request_count prior 7 days (WoW)
    total_commands:         int        # count of llm_usage rows
    command_type_breakdown: dict[str, int]
    dominant_command_type:  str | None # highest count command_type
    total_tokens_used:      int
    plan_id:                str | None
    company_domain:         bool
    has_recent_negative_feedback: bool  # negative_rating in last 7 days
    segment:                UserSegment | None = None
```

### `models/actions.py`

```python
class EmailContent(BaseModel):
    subject: str
    body: str               # under 150 words, plain text

class TriggerResult(BaseModel):
    trigger_name: str
    fired: bool
    channel: Literal['email', 'in_app', 'alert'] | None = None

class OutreachLogEntry(BaseModel):
    user_id:         UUID
    trigger_name:    str
    channel:         str
    message_preview: str | None = None
```

---

## 8. Build Phases

### Phase 0 — Project Setup ✅ DONE
- [x] Create folder skeleton + `__init__.py` files
- [x] `uv add` all dependencies
- [x] Create `.env` and `.env.example`
- [x] `db/client.py` — Supabase singleton using service_role key
- [x] `models/db.py` with confirmed column names
- [x] Minimal `main.py` — fetch users, print count, confirm connection
- [ ] Create `cs_outreach_log` and `cs_inapp_messages` in Supabase ← **pending**

### Phase 1 — Data Pipeline (IN PROGRESS)
- [x] `db/fetch.py` — `fetch_users()`, `fetch_usage()`, `fetch_daily_usage()`, `fetch_sessions()` (pagination working, verified counts: users=121, sessions=1590, llm_usage=3524, llm_daily_usage=57)
- [ ] `pipeline/metrics.py` — `compute_metrics()` → `UserMetrics` per user ← **next**
  - Session count + gap from `sessions` table directly
  - Command diversity + breakdown from `llm_usage`
  - Weekly requests from `llm_daily_usage`
  - Negative feedback flag from `feedback_events`

### Phase 2 — Segment Classifier (est. 1–2 hrs)
- [ ] `classifier/segment.py` — `classify_segment(metrics) -> UserSegment`

### Phase 3 — Trigger Evaluation ✅ DONE
- [x] `triggers/evaluate.py` — one function per trigger, registered in `_TRIGGERS` list
- [x] Stubs for non-buildable triggers (`day_0_guided_modal`, `day_75_referral`)
- [x] `models/actions.py` — `TriggerResult`, `EmailContent`, `OutreachLogEntry`
- Verified against live data (2026-05-21): 113 triggers fired across 122 users
  - `ongoing_gap_21d/email`: 73 — 60% of users haven't sessioned in 21+ days (long-churned)
  - `ongoing_gap_14d/email`: 23 — early at-risk users between day 14–60
  - `ongoing_dropoff`: 3 — weekly request drop >50% with prior baseline
  - `day_90_churn`: 2 — inactive users at the 90-day mark
  - `day_0_welcome`: 1 — new signup caught by ±1 day range window

### Phase 4 — Outreach Log (est. 1 hr)
- [ ] `db/outreach_log.py`
  - `was_triggered(user_id, trigger_name) -> bool`
  - `log_outreach(entry: OutreachLogEntry) -> None`

### Phase 5 — Action Engine (est. 3–4 hrs)
- [ ] `actions/message_gen.py` — Pydantic AI agent → `EmailContent`
  - Input: user name, trigger name, segment, command_type_breakdown, lifecycle_day, plan_id
  - Output: structured `EmailContent` (subject + body ≤150 words)
- [ ] `actions/email.py` — send via Brevo; log errors, never crash the run
- [ ] `actions/inapp.py` — write row to `cs_inapp_messages`
- [ ] `actions/alert.py` — plain-text email to `ALERT_EMAIL` via Brevo

### Phase 6 — Daily Cohort Report (est. 1 hr)
- [ ] `reporting/cohort_report.py`
  - Date + total users processed
  - Segment breakdown (count per segment)
  - Triggers fired (count per trigger)
  - Sends by channel
  - Skipped (already triggered) count
  - Alert flags: activation rate < 55%, second-session rate < 35% by Day 5

### Phase 7 — Main Entry Point (est. 1 hr)
- [ ] `main.py` — orchestrate all phases, `--dry-run` flag skips all sends/writes

### Phase 8 — Scheduling (est. 1 hr)
- [ ] `.github/workflows/daily_run.yml` — cron `0 8 * * *` (8am UTC)
- [ ] Add all `.env` values as GitHub repository secrets

---

## 9. Segment Classification Rules

Applied in priority order — first match wins.

| Priority | Segment    | Conditions                                                                                    |
|----------|------------|-----------------------------------------------------------------------------------------------|
| 1        | High-Value | `active_days_last_7 >= 5` AND `session_count >= 8` AND `company_domain == True`              |
| 2        | Healthy    | `active_days_last_7 >= 3` AND `days_since_last_active <= 7`                                  |
| 3        | At-Risk    | `active_days_total > 0` AND (`days_since_last_active > 7` OR `has_recent_negative_feedback`) |
| 4        | Inactive   | `session_gap > 14` (if `lifecycle_day` 14–60) OR `session_gap > 21` (if `lifecycle_day > 60`) OR `active_days_total == 0` |

---

## 10. Trigger Map

Each function in `triggers/evaluate.py` returns `True` or `False`. A user can match multiple
triggers in one run. Non-buildable triggers are coded as stubs that always return `False`.

**Range convention:** All lifecycle day triggers use a ±1 day window (`N <= lifecycle_day <= N+1`)
instead of an exact match. This means a missed cron run doesn't permanently lose the window.
The outreach log dedup (`was_triggered`) prevents double-sends if the job runs twice in the window.

### Day 0 — Onboarding
| Trigger             | Condition                                        | Channel | Buildable          |
|---------------------|--------------------------------------------------|---------|--------------------|
| day_0_welcome       | `lifecycle_day <= 1`                             | In-app  | Yes                |
| day_0_guided_modal  | stub — requires product layer (no command success in session) | In-app | No |

### Day 1–7 — Early Exploration
| Trigger              | Condition                                                                     | Channel       | Buildable |
|----------------------|-------------------------------------------------------------------------------|---------------|-----------|
| day_3_checkin        | `3 <= lifecycle_day <= 4 AND session_count < 2`                               | Email         | Yes       |
| day_5_nudge          | `5 <= lifecycle_day <= 6 AND session_count == 1`                              | In-app        | Yes       |
| day_7_no_commands    | `5 <= lifecycle_day <= 8 AND session_count >= 1 AND total_commands == 0`      | Email         | Yes (new) |
| day_7_highvalue_flag | `7 <= lifecycle_day <= 8 AND (session_count >= 4 OR command_diversity >= 3)`  | In-app, Email | Yes       |
| day_7_no_session     | `7 <= lifecycle_day <= 8 AND session_count == 0`                              | Alert         | Yes       |

### Day 8–14 — Value Confirmation
| Trigger        | Condition                                                                                     | Channel | Buildable |
|----------------|-----------------------------------------------------------------------------------------------|---------|-----------|
| day_10_email   | `10 <= lifecycle_day <= 11 AND session_count in {2, 3}`                                       | Email   | Yes       |
| day_12_survey  | `12 <= lifecycle_day <= 13 AND weekly_requests_prev >= 3 AND weekly_requests < weekly_requests_prev` | In-app | Yes |
| day_14_at_risk | `14 <= lifecycle_day <= 15 AND segment == at_risk`                                            | Email   | Yes       |

### Day 15–30 — Habit Formation
| Trigger           | Condition                                                                        | Channel        | Buildable |
|-------------------|----------------------------------------------------------------------------------|----------------|-----------|
| day_21_diversity  | `21 <= lifecycle_day <= 22 AND total_commands > 0 AND breakdown[dominant] / total_commands > 0.70` | Email, In-app | Yes |
| day_28_community  | `28 <= lifecycle_day <= 29 AND session_count >= 5`                               | Email          | Yes       |
| day_30_milestone  | `30 <= lifecycle_day <= 31 AND segment == healthy`                               | Email          | Yes       |
| day_30_inactive   | `30 <= lifecycle_day <= 31 AND segment == inactive`                              | Email          | Yes       |

### Day 31–60 — Engagement Deepening
| Trigger        | Condition                                                                  | Channel    | Buildable |
|----------------|----------------------------------------------------------------------------|------------|-----------|
| day_45_winback | `45 <= lifecycle_day <= 46 AND 10 <= session_gap <= 14`                    | Email      | Yes       |
| day_55_founder | `55 <= lifecycle_day <= 56 AND company_domain AND session_count >= 8`      | Alert      | Yes       |
| day_60_winback | `60 <= lifecycle_day <= 61 AND segment == inactive`                        | Email      | Yes       |

### Day 61–90 — Retention & Expansion
| Trigger           | Condition                                                               | Channel       | Buildable                      |
|-------------------|-------------------------------------------------------------------------|---------------|--------------------------------|
| day_75_referral   | stub — referral system not built yet                                    | Email         | No                             |
| day_85_enterprise | `85 <= lifecycle_day <= 86 AND company_domain AND session_count >= 10`  | Alert         | Yes                            |
| day_90_churn      | `90 <= lifecycle_day <= 91 AND segment == inactive`                     | Email, Alert  | Yes                            |

### Ongoing — Fire Any Time
| Trigger                | Condition                                                                                               | Channel        | Buildable | Notes |
|------------------------|---------------------------------------------------------------------------------------------------------|----------------|-----------|-------|
| ongoing_dropoff        | `lifecycle_day > 7 AND session_count >= 2 AND weekly_requests_prev > 0 AND weekly_requests < weekly_requests_prev * 0.5` | In-app, Email | Yes | |
| ongoing_gap_14d        | `14 <= lifecycle_day <= 60 AND session_gap > 14`                                                        | Email          | Yes       | Mutually exclusive with gap_21d by lifecycle range |
| ongoing_gap_21d        | `lifecycle_day > 60 AND session_gap > 21`                                                               | Email          | Yes       | |
| ongoing_healthy_nudge  | `segment == healthy`                                                                                    | In-app, Alert  | Yes       | **Cooldown: Phase 4 `was_triggered` must check within 14 days, not all-time** |
| ongoing_upgrade_nudge  | `plan_id == 'Free' AND weekly_requests >= 5 AND total_tokens_used >= 50_000`                            | Email          | Yes (new) | |

---

## 11. Trigger Design Decisions

Changes made from the original implementation plan, with justification from live data and
production CS system patterns.

| Decision | Original | Final | Why |
|----------|----------|-------|-----|
| Lifecycle day matching | `lifecycle_day == N` (exact) | `N <= lifecycle_day <= N+1` (range) | A single missed cron run permanently loses the window. 73/122 users are already churned — we can't afford to drop onboarding triggers on a deploy failure. Outreach log dedup prevents double-sends within the window. |
| `day_12_survey` baseline | `weekly_requests < weekly_requests_prev` | Added `weekly_requests_prev >= 3` floor | Without a floor, a drop from 1 → 0 requests fires the survey. That's noise, not signal. A user needs at least 3 prior-week commands before a decline is meaningful. |
| New trigger: `day_7_no_commands` | Not in original plan | `5 <= lifecycle_day <= 8 AND session_count >= 1 AND total_commands == 0` / email | Logged in but never ran a command is a distinct failure mode from total ghosts (`day_7_no_session`). These users showed intent but hit a wall — different copy, different intervention. |
| New trigger: `ongoing_upgrade_nudge` | Not in original plan | `plan_id == 'Free' AND weekly_requests >= 5 AND total_tokens_used >= 50_000` / email | Highest-ROI trigger in any SaaS CS system. Free users with strong engagement are primed for a Plus pitch. Fully buildable from existing `plan_id` and usage data. |
| `ongoing_healthy_nudge` cooldown | Not specified | Cooldown enforced in Phase 4 `was_triggered` (14-day window, not all-time) | Without a cooldown, this fires every single daily run for any healthy user, spamming them indefinitely. The trigger condition itself is correct; the dedup window is where the frequency is controlled. |
| `ongoing_dropoff` baseline guard | Not explicit | Added `weekly_requests_prev > 0` | Prevents `0 < 0 * 0.5` from being evaluated as a dropoff. Mathematically False either way, but explicit intent is clearer and avoids confusion when reading the condition. |

---

## 12. Known Data Limitations

| Issue                       | Severity | Impact                                            | Workaround                                      |
|-----------------------------|----------|---------------------------------------------------|-------------------------------------------------|
| No `first_command_at`       | High     | Lifecycle clock anchored to signup, not first use | Use `created_at` as Day 0; accept ±2 day drift  |
| `prompt_summary` always null| Medium   | No "you were researching X" personalisation       | Use `command_type_breakdown` for copy instead   |
| `llm_daily_usage` has no `command_type` | Low | Can't see command mix in daily aggregates | Use `llm_usage` for command metrics          |

> Note: The planning doc flagged "no session tracking" and "two-row join required" as Critical
> issues. Both are resolved — `sessions` table exists, and `command_type` is a direct column.

---

## 12. Open Items

Remaining unknowns before Phase 5 (Action Engine) can be fully built.

| # | Item | Needed For |
|---|------|------------|
| 1 | Verified Brevo sending domain (e.g. `hello@useoasis.co`) | `FROM_EMAIL` env var, all outbound email |
| 2 | `FROM_NAME` for outreach emails (e.g. "Archit from Oasis") | All outbound email |
| 3 | Does the Oasis frontend already have a notification/banner system? | In-app nudges — if not, frontend team must build the reader |
| 4 | Does the frontend use Supabase Realtime or polling for messages? | Determines nudge delivery latency |
| 5 | Is there a consumer domain list in the codebase already? | If not, default: `gmail, yahoo, outlook, hotmail, icloud, protonmail, me, mac, live` |
