# Brevo naming standard (Oasis)

Production-style names only: **spaces**, **Title Case**, **no em dashes**. Repo HTML paths stay `brevo-oasis-*.html`; these names are for **Brevo UI** (templates, automation steps, lists).

**Manifest:** `launch_config.brevo_phase1` in [`public/email_sequences.json`](../public/email_sequences.json)

---

## Infrastructure

| Object | Exact Brevo name |
|--------|------------------|
| Contact list | **Oasis Lifecycle** |
| Phase 1 automation | **Oasis Phase 1** |
| From name (all Adam-voiced campaigns, including PH) | **Adam from Oasis** |

**Env:** `BREVO_LIFECYCLE_LIST_ID` (numeric list id). Deprecated alias: `BREVO_PHASE1_QA_LIST_ID` (still read by enroll script during transition).

---

## Phase 1 lifecycle

Use these **exact** template names in Brevo. Wire each **Oasis Phase 1** automation step to the matching template.

| Sequence ID | Brevo template name | Repo HTML |
|-------------|---------------------|-----------|
| `welcome` | Oasis Welcome | [`brevo-oasis-emails/lifecycle/brevo-oasis-welcome.html`](../brevo-oasis-emails/lifecycle/brevo-oasis-welcome.html) |
| `activation_nudge` | Oasis Activation Nudge | [`brevo-oasis-emails/lifecycle/brevo-oasis-activation-nudge.html`](../brevo-oasis-emails/lifecycle/brevo-oasis-activation-nudge.html) |
| `activation_cs_calendar` | Oasis Activation CS Calendar | [`brevo-oasis-emails/lifecycle/brevo-oasis-activation-cs-calendar.html`](../brevo-oasis-emails/lifecycle/brevo-oasis-activation-cs-calendar.html) |
| `nps_day3` | Oasis NPS | [`brevo-oasis-emails/lifecycle/brevo-oasis-nps-day3.html`](../brevo-oasis-emails/lifecycle/brevo-oasis-nps-day3.html) |
| `pmf_day10` | Oasis PMF | [`brevo-oasis-emails/lifecycle/brevo-oasis-pmf-day10.html`](../brevo-oasis-emails/lifecycle/brevo-oasis-pmf-day10.html) |

**Automation order (production timing):** Welcome (D0) → Activation Nudge (D1, conditional) → Activation CS Calendar (D2–3, conditional) → NPS (D3) → PMF (D10).

**Initial test timing:** Same workflow **Oasis Phase 1**; set 1-minute waits between steps while validating, then edit waits/conditions in place (see [`BREVO_PHASE1_TEST_SETUP.md`](BREVO_PHASE1_TEST_SETUP.md)).

---

## Product Hunt

| Sequence ID | Brevo template name | Repo HTML |
|-------------|---------------------|-----------|
| `ph_teaser` | Oasis PH Teaser | [`brevo-oasis-emails/ph-waitlist/brevo-oasis-ph-teaser-waitlist.html`](../brevo-oasis-emails/ph-waitlist/brevo-oasis-ph-teaser-waitlist.html) |
| `ph_launch` | Oasis PH Launch | [`brevo-oasis-emails/ph-waitlist/brevo-oasis-ph-launch-waitlist.html`](../brevo-oasis-emails/ph-waitlist/brevo-oasis-ph-launch-waitlist.html) |

---

## Appendix: later lifecycle and conversion

When you add templates in Brevo, use **Oasis** + Title Case label. Repo file names unchanged.

| Brevo template name | Repo HTML |
|---------------------|-----------|
| Oasis Paid Zen Welcome | `lifecycle/brevo-oasis-paid-zen-welcome.html` |
| Oasis Limit Hitter D0 | `lifecycle/brevo-oasis-limit-hitter-upgrade.html` |
| Oasis Limit Hitter D7 | `lifecycle/brevo-oasis-limit-hitter-upgrade-d7.html` |
| Oasis Cancelled Win-back D0 | `lifecycle/brevo-oasis-cancelled-winback-d0.html` |
| Oasis Cancelled Win-back D14 | `lifecycle/brevo-oasis-cancelled-winback-d14.html` |
| Oasis At-risk D0 | `conversion/brevo-oasis-at-risk-nurture-d0.html` |
| Oasis At-risk D7 | `conversion/brevo-oasis-at-risk-nurture-d7.html` |
| Oasis At-risk D14 | `conversion/brevo-oasis-at-risk-nurture-d14.html` |
| Oasis At-risk D21 | `conversion/brevo-oasis-at-risk-nurture-d21.html` |
| Oasis Dead Resurrection D0 | `conversion/brevo-oasis-dead-resurrection-d0.html` |
| Oasis Dead Resurrection D14 | `conversion/brevo-oasis-dead-resurrection-d14.html` |
| Oasis Return Reinforcement | `conversion/brevo-oasis-return-reinforcement.html` |
| Oasis Enterprise Founder | `enterprise/brevo-oasis-enterprise-founder.html` |
| Oasis Enterprise Expansion | `enterprise/brevo-oasis-enterprise-expansion.html` |
| Oasis Legal Notice | `operational/brevo-oasis-legal-notice.html` |
| Oasis Incident Notice | `operational/brevo-oasis-incident-notice.html` |

---

## Brevo UI migration (manual)

If you already created templates under old names (`Oasis QA - Welcome`, `PH Launch`, etc.):

1. Rename templates to the exact names in the tables above (automation steps keep their template IDs).
2. Rename or recreate the list as **Oasis Lifecycle**.
3. Rename the automation as **Oasis Phase 1** (one workflow; adjust timing in place).
4. Set `BREVO_LIFECYCLE_LIST_ID` in `.env` to the **Oasis Lifecycle** list id.

---

## Related

- Setup and testing: [`BREVO_PHASE1_TEST_SETUP.md`](BREVO_PHASE1_TEST_SETUP.md)
- Enroll script: `python3 scripts/enroll_brevo_phase1.py`
- HTML templates: [`brevo-oasis-emails/README.md`](../brevo-oasis-emails/README.md)
