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

**https://oasis-analytics.vercel.app** — reload the page for live Supabase metrics via `/api/snapshot`.

Set `SUPABASE_URL` and `SUPABASE_KEY` in Vercel project env vars (see **[docs/VERCEL_DEPLOY.md](docs/VERCEL_DEPLOY.md)**).

```bash
vercel dev          # local: live API + static UI (applies vercel.json rewrites)
python3 reporting/serve_public.py --port 3456   # static UI + /email-machine rewrite
npx serve public    # static UI; serve.json applies /email-machine rewrite
```

## Docs

- [reporting/README.md](reporting/README.md) — operator commands
- [docs/BUILDING_A_SNAPSHOT_DASHBOARD.md](docs/BUILDING_A_SNAPSHOT_DASHBOARD.md) — pattern guide for other teams
- [docs/VERCEL_DEPLOY.md](docs/VERCEL_DEPLOY.md) — Vercel deployment
