# Dual-repo sync (canonical → mirror)

Two GitHub remotes carry the same Oasis Analytics codebase. **AdamKershner/oasis-analytics is canonical** (Vercel deploy + primary development). **Kahana-LLC/oasis-cs-agent** is the org mirror and must match `analytics/main` on every ship.

| Remote | Repository | Role |
|--------|------------|------|
| `analytics` | [AdamKershner/oasis-analytics](https://github.com/AdamKershner/oasis-analytics) | **Source of truth** · Vercel → [oasis-analytics.vercel.app](https://oasis-analytics.vercel.app) |
| `origin` | [Kahana-LLC/oasis-cs-agent](https://github.com/Kahana-LLC/oasis-cs-agent) | **Mirror** · same `main` as `analytics` |

## Remotes (one-time)

```bash
git remote -v
# analytics  https://github.com/AdamKershner/oasis-analytics.git
# origin     https://github.com/Kahana-LLC/oasis-cs-agent.git
```

If `analytics` is missing:

```bash
git remote add analytics https://github.com/AdamKershner/oasis-analytics.git
```

## Ship workflow (after every meaningful change)

```bash
# From repo root on main
git push analytics main    # Vercel + canonical
git push origin main       # Kahana mirror (must match analytics)
```

Or:

```bash
./scripts/push_both_remotes.sh
```

**Conflict rule:** If `origin/main` and `analytics/main` diverge, **reset Kahana to Adam’s branch** (never the other way around):

```bash
git fetch analytics origin
git checkout main
git reset --hard analytics/main
git push origin main
```

Only use `--force` on `origin` when you intentionally overwrite Kahana with canonical history.

## Verify both repos match

```bash
git fetch analytics origin
git rev-parse analytics/main origin/main
# Same 40-char SHA = in sync
```

## What does not sync automatically

- Vercel project (wired to **AdamKershner/oasis-analytics** only)
- GitHub Issues / Actions / branch protection (per repo)
- Brevo templates and Supabase Edge (operational, not git)

See also [`VERCEL_EMAIL_COPY_SYNC.md`](VERCEL_EMAIL_COPY_SYNC.md) for deploy + preview checks after email copy changes.
