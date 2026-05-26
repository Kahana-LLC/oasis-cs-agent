# Baseline reporting

## View the dashboard

### Shareable link (Vercel)

Production loads live data from **`/api/snapshot`** on each page refresh (see **[../docs/VERCEL_DEPLOY.md](../docs/VERCEL_DEPLOY.md)**).

| File | Purpose |
|------|---------|
| `snapshot_service.py` | Fetch + compute (CLI + API) |
| `../api/snapshot.py` | Vercel serverless endpoint |

Offline static preview: `.venv/bin/python reporting/build_static_site.py`

### Local Streamlit (interactive)

```bash
.venv/bin/python main.py --baseline-view
```

Opens **http://localhost:8501**. Press `Ctrl+C` to stop. Requires the terminal to stay open.

Or: `.venv/bin/streamlit run reporting/dashboard.py`

## Refresh metrics from Supabase

Requires `.env` with `SUPABASE_URL` and `SUPABASE_KEY` (service role).

```bash
.venv/bin/python main.py --baseline
```

Writes `baseline_snapshot.json` and updates the optional Cursor canvas. Then rerun the dashboard (sidebar **Rerun** or restart `--baseline-view`).

## Files

| File | Purpose |
|------|---------|
| `dashboard.py` | Streamlit app (local viewer) |
| `baseline_snapshot.json` | Cached snapshot (offline / fallback) |
| `baseline_metrics.py` | Metric computation |
| `run_baseline.py` | Fetch + write snapshot + canvas |
| `snapshot_service.py` | Shared fetch/compute for API + CLI |
| `dau_model.py` | DAU bucket sizes + flow rates (User Email Machine model) |
| `launch_kpis.py` | Product Hunt launch KPI scorecard + usage cost forecast |
| `lifecycle_readiness.py` | Phase 1 milestone coverage by DAU bucket |
| `lifecycle_email_sends.py` | Phase 1 send counts per trigger (`cs_outreach_log`) for recent signups |
| `build_snapshot.py` | Rebuild from `sql_export.json` (no `.env`) |

## DAU model section

The Vercel dashboard and snapshot JSON include **`dau_model`**: seven user buckets (New, Current, Reactivated, Resurrected, At-risk WAU/MAU, Dead) and flow rates (NURR, CURR, RURR, etc.) per the [Daily Active Users diagram](../User%20Email%20Machine.txt). Engagement = `sessions` ∪ `llm_usage`. Proposed email sequences mapped to these buckets: [USER_EMAIL_MACHINE_PROPOSAL.md](../docs/USER_EMAIL_MACHINE_PROPOSAL.md). **Engineer subpage (live):** `/email-machine` on the Vercel site (`public/email-machine.html` + `public/email_sequences.json`).

## Lifecycle readiness by bucket

Snapshot keys **`lifecycle_readiness`** and **`lifecycle_email_sends`** (`lifecycle_readiness.py`, `lifecycle_email_sends.py`): cross-tab of Phase 1 milestones × DAU bucket, plus per-trigger send coverage for active signups in the last N days (default 30) from **`cs_outreach_log`**. Fetched on each `/api/snapshot` call via `db/fetch.fetch_cs_outreach_log()`. Rendered on the main dashboard at `#lifecycle-readiness` and `#lifecycle-email-sends`.

## Launch KPIs section

The dashboard includes **`launch_kpis`**: a scorecard mapped 1:1 to [`Launch KPIs.txt`](../Launch%20KPIs.txt) (activation, engagement, retention, monetization, feedback, DAU cross-links). The Vercel UI also provides editable **Gemini** and **Supabase** monthly cost inputs (stored in browser `localStorage` as `oasis_gemini_monthly_usd` / `oasis_supabase_monthly_usd`) to recalculate net ARPU and LTV proxy client-side. Server-side **`usage_cost_forecast`** extrapolates 7-day prompt volume and model-based API cost to a projected monthly figure.

## Tooltips, insights, and KPI deltas

- **`metric_glossary.py`** — plain-English definitions (hover `?` on Vercel, `help=` in Streamlit).
- **`insights.py`** — rule-based **Key insights** at the top of the report (churn / dead-user levers).
- **`metric_deltas.py`** — daily / weekly / monthly change vs prior snapshots.
- **`snapshot_history.py`** — upserts compact metrics to Supabase table **`baseline_metric_history`** (migration in [`../supabase/migrations/`](../supabase/migrations/)).

Run **`main.py --baseline` daily** (or rely on live `/api/snapshot` upserts) so deltas populate. Weekly deltas need 7 days of history; monthly needs 30.

| Module | Purpose |
|--------|---------|
| `snapshot_history.py` | Extract, upsert, fetch history |
| `metric_deltas.py` | Delta math + significance flags |
| `insights.py` | Key insights cards |
| `metric_glossary.py` | Tooltip copy (static meanings) |
| `corporate_goals.py` | Target constants (500 subs by Dec 31, 80% margin, 4.5× DAU); monthly subscriber milestones |
| `goal_progress.py` | Progress + trend phrases |
| `goals_state.py` | DAU launch-week baseline in `corporate_goals_state` |
| `goal_aware_tooltips.py` | Meaning + trend + goals per metric |

See [`../Corporate Goals.txt`](../Corporate%20Goals.txt) for team-facing goal definitions.

**Paid subscribers:** baseline 1 plus distinct `user_plans` users with `start_date >= 2026-05-24`. Year-end goal 500; dashboard shows current vs this month’s cumulative target.

**Gross margin:** `100 × (total_revenue_usd − estimated_api_cost_usd − 25) / total_revenue_usd` (Supabase default $25/mo).

**DAU 4.5× goal:** Compared to the average DAU during the 7 days after Product Hunt launch (May 27, 2026 ET), not calendar year-over-year until 12 months of data exist.

## Optional: Cursor canvas

See [`../canvases/README.md`](../canvases/README.md).

## Guide for building similar dashboards

Shareable walkthrough for other teams: [`../docs/BUILDING_A_SNAPSHOT_DASHBOARD.md`](../docs/BUILDING_A_SNAPSHOT_DASHBOARD.md).
