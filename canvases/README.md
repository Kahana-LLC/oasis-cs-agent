# Baseline report (optional Cursor canvas)

**Primary viewer:** Streamlit — see [`../reporting/README.md`](../reporting/README.md).

```bash
.venv/bin/python main.py --baseline-view
```

This folder’s `oasis-baseline-report.canvas.tsx` is an optional Cursor canvas mirror. It may only render as a visual dashboard when opened from Cursor’s managed `.cursor/projects/.../canvases/` path, not always from this repo copy.

Regenerate data:

```bash
.venv/bin/python main.py --baseline
```

Data source: `reporting/baseline_snapshot.json`.
