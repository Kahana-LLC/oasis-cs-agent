# Supabase (Oasis project)

Migrations and Edge Functions for lifecycle email. Deploy against the **Oasis app** Supabase project (not the analytics Vercel site).

| Path | Purpose |
|------|---------|
| [`migrations/20260525140000_cs_outreach_log.sql`](migrations/20260525140000_cs_outreach_log.sql) | Email dedup table |
| [`functions/lifecycle-send/`](functions/lifecycle-send/) | Invoke send by `user_id` / `email` |
| [`functions/lifecycle-on-signup/`](functions/lifecycle-on-signup/) | `users` INSERT webhook → welcome |
| [`functions/lifecycle-daily-cron/`](functions/lifecycle-daily-cron/) | Daily cohorts → activation nudge (more triggers later) |
| [`functions/_shared/`](functions/_shared/) | Brevo + outreach helpers |

**Welcome runbook:** [`docs/LIFECYCLE_WELCOME.md`](../docs/LIFECYCLE_WELCOME.md)

## Deploy Edge Functions (CLI)

### 1. Install and log in

If `supabase: command not found`, use **one** of these on your Mac:

```bash
# Option A — Homebrew (if brew install fails on Xcode, update Xcode or use Option B)
brew install supabase/tap/supabase

# Option B — npm global
npm install -g supabase

# Option C — no global install (prefix every command with npx)
npx supabase@latest --version
```

Log in:

```bash
supabase login
# or: npx supabase@latest login
```

Opens the browser to authenticate.

**Repo path** (note the space in `CS Agent`):

```bash
cd "/Users/adamkershner/Documents/CS Agent/oasis-cs-agent"
```

### 2. Link this repo to the **Oasis** Supabase project

From the repo root (or `supabase/`):

```bash
cd "/Users/adamkershner/Documents/CS Agent/oasis-cs-agent"
supabase link --project-ref wvclepquxxczgrukfqyr
```

Replace with your ref if different (Dashboard → Project Settings → General → Reference ID). Oasis project ref used in dev: `wvclepquxxczgrukfqyr`.

### 3. Set secrets (same as `.env`)

```bash
supabase secrets set \
  BREVO_API_KEY="xkeysib-..." \
  BREVO_TEMPLATE_ID_WELCOME="54" \
  LIFECYCLE_SENDER_EMAIL="your@verified-sender.com" \
  LIFECYCLE_SENDER_NAME="Adam from Oasis"
```

`SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` are injected automatically in functions — do not set them manually.

List secrets: `supabase secrets list`

### 4. Deploy

```bash
supabase functions deploy lifecycle-send --no-verify-jwt
supabase functions deploy lifecycle-on-signup --no-verify-jwt
supabase functions deploy lifecycle-daily-cron --no-verify-jwt
```

`--no-verify-jwt` matches `verify_jwt = false` in [`config.toml`](config.toml) so **database webhooks** can call `lifecycle-on-signup` with `Authorization: Bearer <service_role_key>`.

### 5. Verify URLs

Dashboard → **Edge Functions** — you should see:

- `https://YOUR_PROJECT_REF.supabase.co/functions/v1/lifecycle-send`
- `https://YOUR_PROJECT_REF.supabase.co/functions/v1/lifecycle-on-signup`

Test:

```bash
curl -X POST "https://YOUR_PROJECT_REF.supabase.co/functions/v1/lifecycle-send" \
  -H "Authorization: Bearer YOUR_SERVICE_ROLE_KEY" \
  -H "Content-Type: application/json" \
  -d '{"trigger_name":"welcome_email","email":"you@example.com","dry_run":true}'
```

### If functions live in the Oasis **app** repo instead

Copy `supabase/functions/` and `supabase/config.toml` into that repo, run `supabase link` there, then the same `secrets set` + `functions deploy` commands.
