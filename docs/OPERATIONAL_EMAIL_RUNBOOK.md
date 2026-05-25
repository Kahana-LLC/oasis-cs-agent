# Operational email runbook

Legal/policy updates and service incidents — **not** lifecycle nurture (welcome, NPS, at-risk, etc.).

## Architecture

| Lane | Providers | Use |
|------|-----------|-----|
| **Operational pool** | Resend (primary) → Amazon SES → Brevo (emergency) | Privacy/terms, security, **outage** |
| **Lifecycle fallback** | MailerLite, OmniSend, Brevo, **Loops** | Marketing / product-help overflow only |

Manifest: [`public/email_sequences.json`](../public/email_sequences.json) → `operational_pool`, sequences `legal_notice`, `incident_notice`.

## Before any blast

1. Sync audience: `python reporting/sync_operational_contacts.py` (writes CSV + optional Resend audience when `RESEND_API_KEY` is set).
2. Confirm dedup key in `outreach_log` (see [PLAN.md](../PLAN.md)).
3. Edit template in [`brevo-oasis-emails/operational/`](../brevo-oasis-emails/operational/) — copy HTML on `/email-machine`.
4. Check capacity on `/email-machine#provider-capacity` (Resend 100/day, 3,000/mo).

**Supabase is source of truth; ESP list is send-time source.** If Supabase is down, use the last exported CSV from sync.

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

**Account setup (2026-05-21):** Resend and Loops are marked **ready** on the Email Machine [account setup](https://oasis-analytics.vercel.app/email-machine#provider-setup) table; Amazon SES is **sandbox** (200/day) until production access is approved. See `account_setup` in `public/email_sequences.json`.

### Resend (primary)

- Free tier: **3,000 emails/month**, **100/day**.
- At ~122 users, one blast fits in a day. At 500+ users, plan **ceil(users/100)** days or SES failover.
- Merge tags in repo use Brevo syntax (`{{ contact.FIRSTNAME }}`); map to Resend variables when sending via API.

### Amazon SES

- **Sandbox:** 200 emails / 24h; recipients must be verified. Automated bulk is **blocked** until production access.
- After approval: set `production_pending: false` on the `ses` provider in `email_sequences.json`.

### SES production access

When AWS requests more information, include:

- **Use case:** Transactional and operational notices (policy updates, incident alerts) to Oasis browser users who created an account.
- **Audience:** Opt-in by account creation; list synced from our database (active users only).
- **Volume:** Current ~122 users; growth to 2,000+ post-launch; operational blasts are rare (few per year).
- **Bounce/complaint handling:** We monitor bounces via ESP dashboards; remove hard bounces from all lists.
- **Identity:** Sending domain `kahana.co` (or your verified domain) with SPF, DKIM, DMARC configured.
- **Sample:** Link to `brevo-oasis-incident-notice.html` or plain operational template (no marketing).

### Loops (lifecycle fallback only)

- Early Stage: **1,000 subscribers**, **4,000 sends/month**, “Powered by Loops” footer.
- Use for **marketing/product-help** when Beehiiv/EmailOctopus overflow — **never** legal or incident.

## Anti-patterns

- Do not send outages through Beehiiv, EmailOctopus, or Loops nurture lists.
- Do not use Loops for legal/privacy notices (footer + wrong list semantics).
- Do not query Supabase at send time during an outage — use pre-synced list or CSV.
- Do not reuse lifecycle `dedup_trigger_name` keys for operational sends.

## Related

- [USER_EMAIL_MACHINE_PROPOSAL.md §3b](USER_EMAIL_MACHINE_PROPOSAL.md)
- [/email-machine](https://oasis-analytics.vercel.app/email-machine) — templates + capacity
