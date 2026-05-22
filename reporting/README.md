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
| `build_snapshot.py` | Rebuild from `sql_export.json` (no `.env`) |

## Optional: Cursor canvas

See [`../canvases/README.md`](../canvases/README.md).

## Guide for building similar dashboards

Shareable walkthrough for other teams: [`../docs/BUILDING_A_SNAPSHOT_DASHBOARD.md`](../docs/BUILDING_A_SNAPSHOT_DASHBOARD.md).
