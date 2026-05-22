# Oasis Analytics

Baseline activation, retention, monetization, and feedback metrics for Oasis.

## Quick start (local)

```bash
python -m venv .venv
.venv/bin/pip install -e .

# Copy secrets (never commit .env)
cp .env.example .env

# Refresh snapshot from Supabase
.venv/bin/python main.py --baseline

# Interactive dashboard (localhost:8501)
.venv/bin/python main.py --baseline-view
```

## Shareable link (Vercel)

Static dashboard from the same JSON snapshot. See **[docs/VERCEL_DEPLOY.md](docs/VERCEL_DEPLOY.md)** for Framework Preset, build settings, and environment variables.

```bash
.venv/bin/python reporting/build_static_site.py   # copies JSON into public/
```

## Docs

- [reporting/README.md](reporting/README.md) — operator commands
- [docs/BUILDING_A_SNAPSHOT_DASHBOARD.md](docs/BUILDING_A_SNAPSHOT_DASHBOARD.md) — pattern guide for other teams
- [docs/VERCEL_DEPLOY.md](docs/VERCEL_DEPLOY.md) — Vercel deployment
