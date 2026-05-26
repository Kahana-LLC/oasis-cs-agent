# Vercel site sync — lifecycle email copy (post–Brevo paste)

Runbook after updating all Brevo HTML templates in the repo. **Vercel is documentation + previews + live dashboard**; sends run on Oasis Supabase + Brevo.

**Site:** [oasis-analytics.vercel.app](https://oasis-analytics.vercel.app/) · **QA handbook:** [`LIFECYCLE_QA_PRE_LAUNCH.md`](LIFECYCLE_QA_PRE_LAUNCH.md)

---

## What auto-updates on deploy (no hand-editing)

| Artifact | How |
|----------|-----|
| `public/emails/*.html` | `build_static_site.py` wraps each `preview.source` HTML from `brevo-oasis-emails/` |
| `public/emails/copy_manifest.json` | Raw HTML + plain text for Email Machine **Copy** buttons |
| `public/email_sequences.json` | Committed manifest (subjects/preheaders for UI) |
| `reporting/email_sequences.json` | Copied at build for `/api/snapshot` |
| `public/email-machine.html` + route | Synced from repo |

**Does not auto-update:** Brevo production templates (you pasted those). Live send content = Brevo, not Vercel.

---

## Pre-deploy checklist (repo)

- [ ] All `brevo-oasis-emails/**` changes committed (Phase 2 conversion, enterprise, paid Zen, win-back, etc.)
- [ ] `public/email_sequences.json` subjects/preheaders match Brevo (spot-check table below)
- [ ] `{{ params.GREETING }}` in every lifecycle HTML opener

---

## Deploy steps

```bash
# From repo root
python3 reporting/build_static_site.py

# Verify previews regenerated
ls -la public/emails/*.html | wc -l   # expect ~23

# Commit if build touched public/emails/ or reporting/email_sequences.json
git add brevo-oasis-emails/ public/email_sequences.json public/emails/ reporting/email_sequences.json
git status

git push analytics main   # canonical + Vercel
git push origin main      # Kahana-LLC mirror (must match analytics)
# Or: ./scripts/push_both_remotes.sh
```

Vercel **Build Command** (already in `vercel.json`): `python3 reporting/build_static_site.py` · **Output:** `public/`

---

## Post-deploy smoke test (5 min)

| Check | URL / action | Pass |
|-------|----------------|------|
| Dashboard loads | [/](https://oasis-analytics.vercel.app/) | Live source caption |
| Launch QA strip | [/#launch-qa](https://oasis-analytics.vercel.app/#launch-qa) | Phase 1+2 copy |
| Email Machine | [/email-machine](https://oasis-analytics.vercel.app/email-machine) | 19 Edge triggers |
| Preview: Paid Zen | Open `upgrade_thank_you` preview | Celebratory header, 1M tokens, **Book time with me** → OnceHub (not Open Oasis) |
| Preview: Enterprise | `enterprise_founder_d55`, `enterprise_expansion_d85` | New feedback copy |
| Preview: At-risk / Dead | Sample D0/D14 | No “haven’t seen you” / days-since |
| API triggers | `curl -sS https://oasis-analytics.vercel.app/api/snapshot \| jq '.lifecycle_email_delivery.triggers \| length'` | **19** |

---

## Subject / preheader reference (manifest = Email Machine)

Sync these in Brevo if manifest was updated after your paste.

### Paid & lifecycle

| Touch | Subject | Preheader |
|-------|---------|-----------|
| upgrade_thank_you | You're in — welcome to Oasis Zen | 1 million tokens per day, elite support, and a direct line to shape Oasis. |
| cancelled_winback D0 | Thank you — what could we change for you to resubscribe? | We sincerely value your input. Thank you for trusting Oasis Zen. |
| cancelled_winback D14 | We'd still love your input on Oasis Zen | What could we change or add for you to consider resubscribing? |

### Conversion (feedback tone)

| Touch | Subject | Preheader |
|-------|---------|-----------|
| at_risk D0 | What could we improve in Oasis? | Your suggestions help us ship features and fixes quickly. |
| at_risk D7 | Do you have suggestions for Oasis? | What could we change or improve? We genuinely want your input. |
| at_risk D14 | What would make Oasis ideal for you? | What would you ideally want in Oasis to make your life easier? |
| at_risk D21 | Your input helps us improve Oasis | We are problem solvers — your feedback shapes what we build next. |
| dead D0 | What could we improve in Oasis? | Your suggestions help us ship features and fixes quickly. |
| dead D14 | We'd still love your input on Oasis | What would you ideally want in Oasis to make your life easier? |
| return_reinforcement | How can we make Oasis better for you? | We genuinely want your feedback — we build from what you say. |

### Enterprise

| Touch | Subject | Preheader |
|-------|---------|-----------|
| enterprise_founder | What would make Oasis indispensable to you? | We are problem solvers — your input drives what we build and fix next. |
| enterprise_expansion | What should Oasis become next? | Even a short reply helps us ship features and fixes faster. |

---

## Optional manifest-only tweaks (no Brevo re-paste)

If you only change `preview.subject` / `preheader` in `email_sequences.json`, redeploy Vercel — Email Machine labels update; Brevo sends unchanged until you edit templates there.

---

## Out of scope for Vercel

- Oasis app signup / Stripe webhooks
- Supabase Edge deploy & secrets
- Brevo template paste (templates 54–72)
- PH waitlist manual sends

See [`LIFECYCLE_QA_PRE_LAUNCH.md`](LIFECYCLE_QA_PRE_LAUNCH.md) for execution QA.
