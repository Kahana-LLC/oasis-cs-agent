# Oasis enterprise outreach emails (HubSpot)

Adam-voiced check-ins for highly engaged users on non-consumer email domains. **Copy treats each recipient as an individual** (workflow, use case, honest product feedback). Do not mention company email, teams, seats, or procurement in the template.

Backend segmentation still uses `company_domain`; that is not surfaced in the email.

**From name:** `Adam from Oasis`

## Templates

| Touch | HubSpot / Brevo name | Day | HTML | Plain text |
|-------|----------------------|-----|------|------------|
| Founder | Oasis Enterprise Founder | D55 | [`brevo-oasis-enterprise-founder.html`](brevo-oasis-enterprise-founder.html) | [`brevo-oasis-enterprise-founder-plain-text.txt`](brevo-oasis-enterprise-founder-plain-text.txt) |
| Expansion | Oasis Enterprise Expansion | D85 | [`brevo-oasis-enterprise-expansion.html`](brevo-oasis-enterprise-expansion.html) | [`brevo-oasis-enterprise-expansion-plain-text.txt`](brevo-oasis-enterprise-expansion-plain-text.txt) |

## Campaign copy

### D55 — Founder (Brevo #71)

| Field | Value |
|-------|--------|
| Header title | Your honest take matters |
| Subject | What would make Oasis indispensable to you? |
| Preheader | We are problem solvers — your input drives what we build and fix next. |
| Primary CTA | **Reply to this email** (feedback callout in body) |
| Secondary | **Book time** → https://go.oncehub.com/AdamKershner (text link) |
| Footer | You're receiving this because you use Oasis. |

### D85 — Expansion (Brevo #72)

| Field | Value |
|-------|--------|
| Header title | Help us see around corners |
| Subject | What should Oasis become next? |
| Preheader | Even a short reply helps us ship features and fixes faster. |
| Primary CTA | **Reply to this email** (feedback callout in body) |
| Secondary | **Book time** → https://go.oncehub.com/AdamKershner (text link) |
| Footer | You're receiving this because you use Oasis. |

## Regenerate

```bash
python3 brevo-oasis-emails/generate_missing_templates.py
python3 reporting/patch_email_preview_meta.py
python3 reporting/build_static_site.py
```

## HubSpot rollout

1. Paste full HTML (single root `<table role="presentation">`).
2. Paste plain-text tab.
3. Set subject and preheader from the table above.
4. Test send before enabling workflows.

Previews: `/emails/enterprise_founder_d55.html`, `/emails/enterprise_expansion_d85.html` on [Email Machine](https://oasis-analytics.vercel.app/email-machine).
