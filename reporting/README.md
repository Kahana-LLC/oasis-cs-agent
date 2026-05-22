# Baseline reporting

## View the dashboard (Streamlit)

```bash
.venv/bin/python main.py --baseline-view
```

Opens **http://localhost:8501** in your browser. Press `Ctrl+C` in the terminal to stop the server.

Or run Streamlit directly:

```bash
.venv/bin/streamlit run reporting/dashboard.py
```

## Refresh metrics from Supabase

Requires `.env` with `SUPABASE_URL` and `SUPABASE_KEY` (service role).

```bash
.venv/bin/python main.py --baseline
```

Writes `baseline_snapshot.json` and updates the optional Cursor canvas. Then rerun the dashboard (sidebar **Rerun** or restart `--baseline-view`).

## Files

| File | Purpose |
|------|---------|
| `dashboard.py` | Streamlit app (primary viewer) |
| `baseline_snapshot.json` | Metric data snapshot |
| `baseline_metrics.py` | Metric computation |
| `run_baseline.py` | Fetch + snapshot + canvas |
| `build_snapshot.py` | Rebuild from `sql_export.json` (no `.env`) |

## Optional: Cursor canvas

See [`../canvases/README.md`](../canvases/README.md).

## Guide for building similar dashboards

Shareable walkthrough for other teams: [`../docs/BUILDING_A_SNAPSHOT_DASHBOARD.md`](../docs/BUILDING_A_SNAPSHOT_DASHBOARD.md).
