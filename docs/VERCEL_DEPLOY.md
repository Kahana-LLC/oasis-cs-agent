# Deploy the baseline dashboard on Vercel

## Important: Streamlit vs Vercel

**You cannot run `streamlit run` on Vercel.** Streamlit needs a long-lived Python server and WebSockets; Vercel uses short-lived serverless functions.

This repo ships two viewers for the same `baseline_snapshot.json`:

| Viewer | Where | Shareable link |
|--------|--------|----------------|
| **Streamlit** (local) | `main.py --baseline-view` | Only while your laptop/server is running |
| **Static site** (Vercel) | `public/index.html` + JSON | Yes — `https://your-project.vercel.app` |

Workflow: refresh metrics locally (or in CI), commit/push, Vercel rebuilds the static dashboard.

---

## Vercel project settings (recommended)

Use these in the Vercel UI when importing **AdamKershner/oasis-analytics** (or override with the repo’s `vercel.json`).

| Setting | Value | Why |
|---------|--------|-----|
| **Framework Preset** | **Other** | Not a Streamlit/Python server app — static HTML output |
| **Root Directory** | `./` | Repo root |
| **Build Command** | `python reporting/build_static_site.py` | Copies `reporting/baseline_snapshot.json` → `public/` |
| **Output Directory** | `public` | Static files Vercel serves |
| **Install Command** | *(leave empty)* | No pip install needed for default deploy |

`vercel.json` in the repo already sets build command and output directory. If the UI conflicts with the file, **prefer `vercel.json`**.

Do **not** use Framework Preset **Python** with `pip install -r requirements.txt` unless you enable the optional “refresh on deploy” flow below.

---

## Environment variables

### Default deploy (snapshot baked into git)

**No environment variables required.**

The build only copies the committed `reporting/baseline_snapshot.json`. Update metrics locally, commit the JSON, push, redeploy.

### Optional: refresh from Supabase on every deploy

Only if you want production to pull live data during `vercel build`:

| Key | Value | Environments |
|-----|--------|----------------|
| `SUPABASE_URL` | `https://xxxx.supabase.co` | Production (and Preview if you want) |
| `SUPABASE_KEY` | Supabase **service role** key | Production |

**Build Command** (replace default):

```bash
pip install -r requirements-vercel.txt && python main.py --baseline && python reporting/build_static_site.py
```

**Install Command:**

```bash
pip install -r requirements-vercel.txt
```

Never put secrets in `.env` committed to git. In Vercel: **Project → Settings → Environment Variables**, paste the same names as your local `.env`.

---

## Local `.env` (not used by Vercel static deploy)

Keep secrets only on your machine:

```bash
# .env (gitignored)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
```

| Task | Command |
|------|---------|
| Refresh snapshot | `.venv/bin/python main.py --baseline` |
| Interactive Streamlit | `.venv/bin/python main.py --baseline-view` |
| Build static files for Vercel | `.venv/bin/python reporting/build_static_site.py` |
| Preview static site locally | `npx serve public` → open the URL shown |

---

## Deploy steps

1. Ensure `reporting/baseline_snapshot.json` exists (`main.py --baseline` if needed).
2. Commit and push to GitHub.
3. Vercel → **Add New Project** → import **oasis-analytics**.
4. Confirm build/output settings (table above).
5. Deploy → share `https://<project>.vercel.app`.

---

## Updating the live link

1. Run `.venv/bin/python main.py --baseline` locally (with `.env`).
2. Commit updated `reporting/baseline_snapshot.json`.
3. Push → Vercel auto-redeploys.

Or use the optional Supabase env vars and refresh-on-build command.

---

## If you need full Streamlit in the cloud

Use **[Streamlit Community Cloud](https://streamlit.io/cloud)** (free public apps): point at `reporting/dashboard.py`, add `SUPABASE_*` only if you add live DB calls later (current dashboard is snapshot-only).

Vercel remains the right choice for a **read-only, shareable** metrics link with no server to maintain.
