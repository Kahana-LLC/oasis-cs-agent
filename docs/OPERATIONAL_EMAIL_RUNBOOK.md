# Operational email runbook

Legal/policy updates and service incidents — **not** lifecycle nurture (welcome, NPS, at-risk, etc.).

## Architecture

| Lane | Providers | Use |
|------|-----------|-----|
| **Operational pool** | **Amazon SES** (primary when production-ready) → **Resend Pro** (backup) | Privacy/terms, security, **outage** |
| **Lifecycle fallback** | Loops, Resend free tier, OmniSend, MailerLite | Nurture overflow + Phase 2 paid interim |

Manifest: [`public/email_sequences.json`](../public/email_sequences.json) → `operational_pool`, sequences `legal_notice`, `incident_notice`.

**Until SES production access:** use **Resend Pro** (~**$20/mo** · **50,000 emails/mo** · **no daily cap**) for full-list legal/incident blasts. At ~122 users today, one blast is trivial; runway to tens of thousands of users before you outgrow 50k/mo on operational alone.

## Before any blast

1. Sync audience: `python reporting/sync_operational_contacts.py` (writes `data/operational_contacts.csv`).
2. Confirm dedup key in `outreach_log` (see [PLAN.md](../PLAN.md)).
3. Edit template in [`brevo-oasis-emails/operational/`](../brevo-oasis-emails/operational/) — copy HTML on `/email-machine`.
4. Check capacity on `/email-machine#provider-capacity`.
5. Ensure **Resend account is on Pro** (or higher) if SES is still in sandbox — same `RESEND_API_KEY` as lifecycle.

**Supabase is source of truth; CSV is send-time source.** If Supabase is down, use the last exported CSV from sync.

## Legal / privacy policy update

1. Publish updated policy on `https://kahana.co/privacy-policy` (or terms URL) with effective date.
2. Optional: in-app banner on next app release.
3. Email all active users:
   ```bash
   python scripts/send_operational.py --template legal \
     --dedup-key legal_privacy_2026_05_24 \
     --dry-run
   ```
4. Remove `--dry-run` after reviewing recipient count and subject.

Dedup pattern: `legal_{policy_slug}_{effective_date}`.

## Incident / outage

1. Update status page (recommended before email).
2. Customize [`brevo-oasis-incident-notice.html`](../brevo-oasis-emails/operational/brevo-oasis-incident-notice.html) — impact, workaround, ETA.
3. Send:
   ```bash
   python scripts/send_operational.py --template incident \
     --dedup-key incident_2026_05_24_auth \
     --dry-run
   ```
4. Follow-up email only if material change; new dedup key per incident.

## Provider notes

**Account setup:** **SES** sandbox until production. **Resend Pro** is the operational backup (not Brevo — avoid stealing Phase 1 / CS agent quota). See [account setup](https://oasis-analytics.vercel.app/email-machine#provider-setup).

### Amazon SES (primary — when approved)

- **Sandbox today:** 200 emails / 24h; automated bulk to full list is **blocked** until production access.
- After approval: set `production_pending: false` on the `ses` provider in `email_sequences.json`.
- Merge tags in repo use Brevo syntax (`{{ contact.FIRSTNAME }}`); map when sending via SES API.

### Resend Pro (operational backup — default while SES sandbox)

- **~$20/mo** · **50,000 emails/month** · **no daily send cap** on Pro (per charter / pricing plan).
- `scripts/send_operational.py` **defaults to Resend** when `ses.production_pending` is true.
- **Same Resend account** as Phase 2 paid and lifecycle fallback — operational blasts share the monthly quota with lifecycle sends; plan headroom accordingly.
- Do **not** use **free-tier** Resend (100/day) for full-list legal/outage — pass `--free-tier-resend` only for small tests.
- Refuse Resend backup (SES only): `--require-ses`.

### Resend (lifecycle — free tier on same account)

- Phase 2 paid welcome, win-back, and Phase 1 overflow: **100/day · 3,000/mo** on free tier modeling.
- Upgrading to Pro for operational also removes the daily cap for lifecycle API sends on that account.

### SES production access

When AWS requests more information, include:

- **Use case:** Transactional and operational notices (policy updates, incident alerts) to Oasis browser users who created an account.
- **Audience:** Opt-in by account creation; list synced from our database (active users only).
- **Volume:** Current ~122 users; growth to 2,000+ post-launch; operational blasts are rare (few per year).
- **Bounce/complaint handling:** We monitor bounces via ESP dashboards; remove hard bounces from all lists.
- **Identity:** Sending domain `kahana.co` (or your verified domain) with SPF, DKIM, DMARC configured.
- **Sample:** Link to `brevo-oasis-incident-notice.html` or plain operational template (no marketing).

### Loops (lifecycle fallback only)

- Marketing/product-help overflow — never legal or incident.

## Anti-patterns

- Do not send outages through Beehiiv, EmailOctopus, or Loops nurture lists.
- Do not use **Brevo** for full-list operational blasts (shares 300/day with Phase 1 + CS agent).
- Do not use **Resend free tier** for full-list legal/outage (100/day).
- Do not query Supabase at send time during an outage — use pre-synced list or CSV.
- Do not reuse lifecycle `dedup_trigger_name` keys for operational sends.

## Related

- [USER_EMAIL_MACHINE_PROPOSAL.md §3b](USER_EMAIL_MACHINE_PROPOSAL.md)
- [/email-machine](https://oasis-analytics.vercel.app/email-machine) — templates + capacity
