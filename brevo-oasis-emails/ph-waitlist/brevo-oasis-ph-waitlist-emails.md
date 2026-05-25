# Oasis Product Hunt waitlist emails (Brevo)

Oasis waitlist contacts (Tally form `w8V8GA` → Brevo list).

## Primary path: drag-and-drop editor

| Spec | Send date | Purpose |
|------|-----------|---------|
| [`brevo-oasis-ph-teaser-dnd-spec.md`](brevo-oasis-ph-teaser-dnd-spec.md) | **May 26, 2026** | Tease PH launch + transparency story |
| [`brevo-oasis-ph-launch-dnd-spec.md`](brevo-oasis-ph-launch-dnd-spec.md) | **May 27, 2026** | Live on PH (duplicate teaser first) |

## Standalone HTML (paste into D&D HTML block: single root `<table>`)

| File | Notes |
|------|-------|
| [`brevo-oasis-ph-teaser-waitlist.html`](brevo-oasis-ph-teaser-waitlist.html) | Full teaser email |
| [`brevo-oasis-ph-launch-waitlist.html`](brevo-oasis-ph-launch-waitlist.html) | Full launch email |
| [`brevo-oasis-ph-founder-intro-snippet.html`](brevo-oasis-ph-founder-intro-snippet.html) | Adam headshot + founder voice copy |
| [`brevo-oasis-ph-founder-signoff-snippet.html`](brevo-oasis-ph-founder-signoff-snippet.html) | PH intro + `- Adam` + mantra + socials |
| [`brevo-oasis-ph-theme-gallery-snippet.html`](brevo-oasis-ph-theme-gallery-snippet.html) | Bottom theme gallery toss-in |
| [`brevo-oasis-ph-payload-snippets.html`](brevo-oasis-ph-payload-snippets.html) | Privacy section + JSON only (D&D Text block) |
| [`brevo-oasis-ph-tally-form-snippet.html`](brevo-oasis-ph-tally-form-snippet.html) | In-email Tally form buttons (teaser) |
| [`brevo-oasis-ph-tally-form-setup.md`](brevo-oasis-ph-tally-form-setup.md) | Tally hidden-field setup for pre-fill |
| [`brevo-oasis-ph-product-card-snippet.html`](brevo-oasis-ph-product-card-snippet.html) | PH product card for launch (replaces hero) |
| [`brevo-oasis-ph-zen-gift-teaser-snippet.html`](brevo-oasis-ph-zen-gift-teaser-snippet.html) | Launch-day surprise hint (teaser only) |
| [`brevo-oasis-ph-zen-gift-launch-snippet.html`](brevo-oasis-ph-zen-gift-launch-snippet.html) | Full Zen gift offer + claim steps (launch) |
| [`brevo-oasis-ph-waitlist-early-access-snippet.html`](brevo-oasis-ph-waitlist-early-access-snippet.html) | Chromium / Windows / Linux early access card (launch) |
| [`brevo-oasis-ph-zen-bonus-callout-snippet.html`](brevo-oasis-ph-zen-bonus-callout-snippet.html) | 3-month PH feedback bonus callout (launch, after upvote badge) |
| [`brevo-oasis-ph-zen-gift-terms-snippet.html`](brevo-oasis-ph-zen-gift-terms-snippet.html) | Gift fine print |
| [`brevo-oasis-ph-zen-gift-emails.md`](brevo-oasis-ph-zen-gift-emails.md) | Offer spec + redemption ops runbook |
| [`brevo-oasis-ph-teaser-plain-text.txt`](brevo-oasis-ph-teaser-plain-text.txt) | Teaser plain-text tab paste |
| [`brevo-oasis-ph-launch-plain-text.txt`](brevo-oasis-ph-launch-plain-text.txt) | Launch plain-text tab paste |
| [`brevo-oasis-support-links-snippet.html`](../shared/brevo-oasis-support-links-snippet.html) | Docs · Slack · Contact footer row (both emails) |

---

## Launch-day Zen gift (May 26–27)

Genuine comment on the Product Hunt launch page unlocks **6 months of Oasis Zen** (1,000,000 tokens per day, ~$120 value). Teaser hints only; launch email reveals full offer and claim steps (reply with screenshot).

Ops runbook: [`brevo-oasis-ph-zen-gift-emails.md`](brevo-oasis-ph-zen-gift-emails.md)  
Link constants: [`brevo-oasis-email-links.js`](../brevo-oasis-email-links.js) (`productHuntSignup`, `productHuntLaunchComment`, `zenGiftTokensPerDay`, `zenGiftMonths`)

---

## Email 1: Teaser (May 26)

**Brevo template name:** `Oasis PH Teaser`  
**Subject:** `Tomorrow on Product Hunt (+ a launch-day surprise)`

**Preheader:** `Privacy-first AI browser. Something special for genuine launch-day feedback.`

**From name:** `Adam from Oasis`

**Single CTA button:** Follow us on Product Hunt (no Mac download button)

### Plain text

Paste [`brevo-oasis-ph-teaser-plain-text.txt`](brevo-oasis-ph-teaser-plain-text.txt) into Brevo Plain-text tab.

---

## Email 2: Launch (May 27)

**Brevo template name:** `Oasis PH Launch`  
**Subject:** `We're live on Product Hunt: 6 months of Zen, on us`

**Preheader:** `Leave genuine feedback on our launch page. Reply with a screenshot to claim 1M tokens/day.`

**From name:** `Adam from Oasis`

**Primary CTA:** Comment on Product Hunt (orange `#ff6154`, UTM URL)

**Secondary CTA:** Create Product Hunt account (`https://www.producthunt.com/`)

**Early access CTA:** Get early access for Chromium / Windows / Linux (`https://kahana.co/oasis-waitlist`) — card after PH buttons, before privacy JSON. Snippet: [`brevo-oasis-ph-waitlist-early-access-snippet.html`](brevo-oasis-ph-waitlist-early-access-snippet.html)

**Send:** Manual once PH listing is live: see [Launch day runbook](#launch-day-runbook-may-27) below.

### Plain text

Paste [`brevo-oasis-ph-launch-plain-text.txt`](brevo-oasis-ph-launch-plain-text.txt) into Brevo Plain-text tab.

---

## Launch day runbook (May 27)

Use this on launch day. Do **not** schedule the campaign in advance.

### Before you send

1. **Confirm PH is live**: open [Product Hunt listing](https://www.producthunt.com/products/kahana) in a browser; post and product page load.
2. **Re-check assets** (verified May 23, 2026: re-check morning of launch):
   - Adam linktree: `https://kahana.co/adam-kershner`
   - Adam headshot: `https://kahana.co/images/about/adam-kershner.jpg`
   - Theme images: `https://kahana.co/images/oasis/assistant-themes/01-stargazer.png` through `07-desert.png`
   - PH thumbnail: `https://ph-files.imgix.net/b83aefb0-b6c2-408e-b4b8-9e4a0360e1d6.png` (200 OK)
   - PH badge: `https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=1146179&theme=light` (200 OK)
   - Doc: `https://kahana.co/docs/technical-and-interaction-data` (200 OK)
   - Assistant themes: `https://kahana.co/docs/assistant-themes`
3. **Build template in Brevo** (if not already done):
   - Duplicate saved May 26 teaser → name `Oasis PH Launch: May 27`
   - Follow [`brevo-oasis-ph-launch-dnd-spec.md`](brevo-oasis-ph-launch-dnd-spec.md) block checklist
   - Paste plain text from [`brevo-oasis-ph-launch-plain-text.txt`](brevo-oasis-ph-launch-plain-text.txt)
4. **Test send** to yourself: verify links, JSON blocks, orange button, headshot, theme gallery, mobile layout.

### Send

1. Open Brevo campaign (draft).
2. Audience: Oasis waitlist segment.
3. **Send now** (manual: do not schedule).
4. Monitor Brevo for bounces and spam complaints.

### Teaser vs launch quick diff

| Element | Teaser | Launch |
|---------|--------|--------|
| Headline | "tomorrow" | "live today" |
| Zen gift | Hint only (no claim steps) | Full offer + 3 steps + screenshot reply |
| Hero | None (founder intro leads) | PH product card |
| Founder voice | Future tense ("launching tomorrow") | Present tense ("just launched") |
| Theme gallery | Bottom toss-in after signoff | Bottom toss-in after signoff |
| Signoff | Journey to the Oasis + `- Adam` + mantra + All my socials | Same |
| Tally form | In-email engine buttons | Replaced by early-access card → `kahana.co/oasis-waitlist` |
| Early access | N/A | Card: Chromium / Windows / Linux waitlist |
| Button color | `#4A6200` (Follow PH) | `#ff6154` comment + `#4A6200` PH signup |
| PH URL | Plain product URL | UTM badge URL for comments |
| Personal close | Feedback ask + thanks | Feedback ask + thanks |
| Closing | "stay in the loop on launch day" | PH badge only (no duplicate Follow button) |

---

## Links reference

| Label | URL |
|-------|-----|
| Product Hunt signup | https://www.producthunt.com/ |
| Product Hunt (teaser) | https://www.producthunt.com/products/kahana |
| Product Hunt (launch comment + UTM) | https://www.producthunt.com/products/kahana?embed=true&utm_source=badge-featured&utm_medium=badge&utm_campaign=badge-oasis-browser-for-mac |
| Interaction data doc | https://kahana.co/docs/technical-and-interaction-data |
| Assistant themes doc | https://kahana.co/docs/assistant-themes |
| Early access waitlist (Chromium, Windows, Linux) | https://kahana.co/oasis-waitlist |
| Choose your version (Tally, teaser only) | https://tally.so/r/w8V8GA |
| Adam linktree (social hub) | https://kahana.co/adam-kershner |
| Adam headshot | https://kahana.co/images/about/adam-kershner.jpg |
| Theme images | https://kahana.co/images/oasis/assistant-themes/01-stargazer.png (through 07-desert.png) |
| PH thumbnail (launch card) | https://ph-files.imgix.net/b83aefb0-b6c2-408e-b4b8-9e4a0360e1d6.png |
| PH badge image | https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=1146179&theme=light |
| Docs | https://kahana.co/docs |
| Join Slack | https://kahanaworkspace.slack.com/archives/C0B3QDPLH4P |
| Contact | https://kahana.co/contact |

Payload examples source: [`data/docs/interaction-payload-examples.js`](../../data/docs/interaction-payload-examples.js)

---

## QA checklist (both emails)

- [ ] No em dashes in copy
- [ ] Adam headshot loads
- [ ] Adam linktree loads: `https://kahana.co/adam-kershner`
- [ ] All 7 theme thumbnails load and link to assistant themes doc
- [ ] PH signup link works: `https://www.producthunt.com/`
- [ ] Two JSON `<pre>` blocks readable on mobile preview
- [ ] Doc link: `https://kahana.co/docs/technical-and-interaction-data`
- [ ] Tally link: `https://tally.so/r/w8V8GA`
- [ ] `{{ unsubscribe }}` and `{{ mirror }}` render in Brevo preview
- [ ] Plain-text version matches HTML intent
- [ ] Footer includes docs, Slack, and contact links
- [ ] No "acts on tabs/history/pages" phrasing
- [ ] Test send completed before bulk send

## QA checklist (teaser only)

- [ ] Zen gift hint present; **no** full claim steps or token numbers
- [ ] PH account nudge links to producthunt.com
- [ ] One green Follow PH button

## QA checklist (launch only)

- [ ] Zen gift: 1M tokens/day, 6 months, $20/mo value, 3 steps, screenshot reply, 7-day window
- [ ] Primary **Comment on Product Hunt** (orange, UTM URL)
- [ ] Secondary **Create Product Hunt account** (green)
- [ ] No duplicate Follow button at bottom
