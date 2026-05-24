# Brevo drag-and-drop spec: Product Hunt launch (May 27)

Edit by **duplicating** the saved May 26 teaser template in Brevo D&D v3.0.1. Do **not** paste full HTML into the raw-html block unless the block checklist fails.

**Audience:** Oasis waitlist (Tally `w8V8GA` → Brevo list)  
**Send:** **Manual** once the Product Hunt listing is live (May 27, 2026)  
**Prerequisite:** Teaser template saved per [`brevo-oasis-ph-teaser-dnd-spec.md`](brevo-oasis-ph-teaser-dnd-spec.md)

**Reference files:**

| File | Use |
|------|-----|
| [`brevo-oasis-ph-launch-waitlist.html`](brevo-oasis-ph-launch-waitlist.html) | Full table-only HTML |
| [`brevo-oasis-ph-product-card-snippet.html`](brevo-oasis-ph-product-card-snippet.html) | PH product card (replaces hero image) |
| [`brevo-oasis-ph-zen-gift-launch-snippet.html`](brevo-oasis-ph-zen-gift-launch-snippet.html) | Full Zen gift offer + 3-step claim |
| [`brevo-oasis-ph-zen-gift-terms-snippet.html`](brevo-oasis-ph-zen-gift-terms-snippet.html) | Gift fine print (included in launch snippet) |
| [`brevo-oasis-ph-zen-gift-emails.md`](brevo-oasis-ph-zen-gift-emails.md) | Offer spec + redemption ops runbook |
| [`brevo-oasis-ph-founder-intro-snippet.html`](brevo-oasis-ph-founder-intro-snippet.html) | Founder headshot + opening copy |
| [`brevo-oasis-ph-founder-signoff-snippet.html`](brevo-oasis-ph-founder-signoff-snippet.html) | Parting remark + Connect with me link |
| [`brevo-oasis-ph-theme-gallery-snippet.html`](brevo-oasis-ph-theme-gallery-snippet.html) | Bottom theme thumbnail grid |
| [`brevo-oasis-ph-payload-snippets.html`](brevo-oasis-ph-payload-snippets.html) | Privacy + JSON section |
| [`brevo-oasis-ph-launch-plain-text.txt`](brevo-oasis-ph-launch-plain-text.txt) | Plain-text tab paste |

---

## Campaign setup (Setup step)

| Field | Value |
|-------|--------|
| Subject | `We're live on Product Hunt: 6 months of Zen, on us` |
| Preheader | `Upvote Oasis on Product Hunt and leave feedback. Reply with a screenshot to claim 1M tokens/day.` |
| From name | `Oasis by Kahana` |
| Schedule | **Do not schedule**: save as draft; send manually when live |

---

## Global styles (Styles panel)

| Style token | Property | Value |
|-------------|----------|-------|
| `default-button` | `background-color`, `border-color` | `#ff6154` (launch only, Product Hunt orange) |
| `default-link` | `color` | `#4A6200` |
| `default-heading2` | `color` | `#313A00` |
| `default` | `color` | `#4A5745` |

---

## Block checklist

### Keep as-is (from teaser duplicate)

| Block | Notes |
|-------|-------|
| View in browser | Uses `{{ mirror }}` |
| Logo | Brevo CDN Kahana logo |
| Social | LinkedIn, YouTube, Instagram, website, Discord |
| Footer | Waitlist disclaimer, contact, privacy, unsubscribe |
| Theme gallery | Re-paste at **bottom** after signoff: `brevo-oasis-ph-theme-gallery-snippet.html` |
| Payload Text block | Same JSON section as teaser, or re-paste `brevo-oasis-ph-payload-snippets.html` |

### Update content

| Block | Action |
|-------|--------|
| Title | `We're live on Product Hunt today` |
| Image (hero) | **Add** PH upvote badge + linked product card at top (see below) |
| Body opening | Replace teaser copy with launch founder intro (see below) |
| Zen gift (full) | Paste [`brevo-oasis-ph-zen-gift-launch-snippet.html`](brevo-oasis-ph-zen-gift-launch-snippet.html) after platform paragraph, **before** privacy JSON |
| Founder signoff | Paste after PH badge: `brevo-oasis-ph-founder-signoff-snippet.html` |
| Theme gallery | Paste at bottom after signoff, before fallback links |
| Personal close | Feedback ask + thanks (see below) |
| Closing line | Upvotes + comments ask (see below) |
| Button 1 | Orange `#ff6154`, label **Comment on Product Hunt**, UTM PH URL |
| Button 2 | Green `#4A6200`, label **Create Product Hunt account**, `https://www.producthunt.com/` |
| Zen gift | Full offer card before privacy JSON |
| Optional Image | PH featured badge SVG, linked to same UTM URL |

### Remove

| Block | Action |
|-------|--------|
| Download for Mac button | **Delete**: no Mac download CTA |
| Tally form card | **Delete** from body (keep Tally link in footer) |
| raw-html block | **Delete** unless using full-HTML fallback |
| Navigation placeholders | **Delete** |

---

## PH product card (replaces hero image)

Paste into a **Text block** (source mode) or use two Image + Text blocks in D&D:

[`brevo-oasis-ph-product-card-snippet.html`](brevo-oasis-ph-product-card-snippet.html)

Or set Image block URL to:

`https://ph-files.imgix.net/b83aefb0-b6c2-408e-b4b8-9e4a0360e1d6.png`

…and add title/subtitle text beside it: **Oasis Browser for Mac** · Mac desktop · Firefox engine · Apple Silicon and Intel

---

## Body opening: paste into Text block

Use the launch variant from [`brevo-oasis-ph-founder-intro-snippet.html`](brevo-oasis-ph-founder-intro-snippet.html). Or paste this after `Hi {{ contact.FIRSTNAME }},`:

```html
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="margin: 0 0 16px;">
  <tr>
    <td width="56" valign="top" style="padding-right: 12px;">
      <img src="https://kahana.co/images/about/adam-kershner.jpg" alt="Adam Kershner" width="56" height="56" style="display: block; width: 56px; height: 56px; border-radius: 50%; object-fit: cover;" />
    </td>
    <td valign="middle">
      <p style="margin: 0; font-size: 15px; font-weight: 700; color: #313A00; line-height: 1.3;">Adam Kershner</p>
      <p style="margin: 2px 0 0; font-size: 13px; color: #6b7355; line-height: 1.3;">Founder, Oasis</p>
    </td>
  </tr>
</table>
<p>We just launched Oasis on Product Hunt and I could not be more excited to share it with you directly.</p>
<p>Chrome was never built for privacy, and the AI in today's "private" browsers still lags behind. Oasis is a privacy-first AI browser <strong>you can train</strong>. Your personal data is sacred, and all interaction data is anonymized by default.</p>
<p>The launch build is <strong>Oasis for Mac</strong>, <strong>desktop only</strong>, built on <strong>Firefox</strong>, for <strong>Apple Silicon and Intel</strong>.</p>
<p><strong>Mobile</strong> and a <strong>Chromium</strong>-engine build for <strong>Windows, Mac, and Linux</strong> are coming soon. <a href="https://tally.so/r/w8V8GA">Choose your version</a> so we know what to notify you about.</p>
```

**Zen gift block:** paste [`brevo-oasis-ph-zen-gift-launch-snippet.html`](brevo-oasis-ph-zen-gift-launch-snippet.html) after the platform/Tally paragraph, before the privacy JSON section.

**Founder signoff:** paste [`brevo-oasis-ph-founder-signoff-snippet.html`](brevo-oasis-ph-founder-signoff-snippet.html) after PH badge. Links to `https://kahana.co/adam-kershner`.

**Theme gallery:** paste [`brevo-oasis-ph-theme-gallery-snippet.html`](brevo-oasis-ph-theme-gallery-snippet.html) at the bottom after signoff.

---

## PH CTAs (launch)

| Priority | Button | URL |
|----------|--------|-----|
| Primary | Upvote and comment on Product Hunt | UTM launch URL (see [`brevo-oasis-email-links.js`](../brevo-oasis-email-links.js) `productHuntLaunchComment`) |
| Secondary | Create Product Hunt account | `https://www.producthunt.com/` |

Place both buttons immediately after the Zen gift card. Remove the duplicate "Follow us on Product Hunt" button at the bottom; keep the PH featured badge image only.

---

## Personal close (after privacy JSON)

```html
<p>I would really love your thoughts and feedback if you get a chance to check it out. We are genuinely trying to build something meaningful that helps people with both privacy and productivity.</p>
<p>Thanks so much for the consideration. It means a lot.</p>
```

---

## Button 1 (primary)

| Field | Value |
|-------|--------|
| Label | Upvote and comment on Product Hunt |
| URL | `https://www.producthunt.com/products/kahana?embed=true&utm_source=badge-featured&utm_medium=badge&utm_campaign=badge-oasis-browser-for-mac` |
| Background | `#ff6154` |
| Text color | `#ffffff` |

## Button 2 (secondary, optional)

| Field | Value |
|-------|--------|
| Label | Create Product Hunt account |
| URL | `https://www.producthunt.com/` |
| Background | `#4A6200` |
| Text color | `#ffffff` |

---

## Optional PH badge image (below button)

| Field | Value |
|-------|--------|
| Image URL | `https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=1146179&theme=light` |
| Link URL | Same UTM URL as button |
| Alt | Oasis Browser for Mac on Product Hunt |

---

## Fallback links (optional Text block)

```html
<p style="font-size:14px;color:#6b7355;text-align:center;">
  <a href="https://tally.so/r/w8V8GA" style="color:#4A6200;font-weight:600;text-decoration:underline;">Choose your version (Mac, Windows, Linux · Chromium or Firefox)</a>
</p>
<p style="font-size:14px;color:#6b7355;">If the button doesn't work: <a href="https://www.producthunt.com/products/kahana?embed=true&utm_source=badge-featured&utm_medium=badge&utm_campaign=badge-oasis-browser-for-mac">Product Hunt</a> · <a href="https://kahana.co/adam-kershner">Connect with me</a> · <a href="https://kahana.co/docs">Browse docs</a> · <a href="https://kahanaworkspace.slack.com/archives/C0B3QDPLH4P">Join Slack</a> · <a href="https://kahana.co/contact">Contact us</a> · <a href="https://kahana.co/docs/technical-and-interaction-data">Interaction data doc</a> · <a href="https://tally.so/r/w8V8GA">Choose your version</a></p>
```

**Footer support links:** paste [`brevo-oasis-support-links-snippet.html`](../shared/brevo-oasis-support-links-snippet.html) in the footer area above Privacy Policy.

---

## Plain-text version

Paste entire contents of [`brevo-oasis-ph-launch-plain-text.txt`](brevo-oasis-ph-launch-plain-text.txt) into Brevo **Plain-text** tab.

---

## Full-HTML fallback

If D&D blocks conflict, paste [`brevo-oasis-ph-launch-waitlist.html`](brevo-oasis-ph-launch-waitlist.html) into a single HTML block. Must start with `<table role="presentation"`: no `<!DOCTYPE>`, `<html>`, or sibling wrapper elements before the table.

---

## Asset verification (May 23, 2026)

| Asset | URL | Status |
|-------|-----|--------|
| Adam headshot | `https://kahana.co/images/about/adam-kershner.jpg` | Re-check before send |
| Adam linktree | `https://kahana.co/adam-kershner` | Re-check before send |
| Theme images (01–07) | `https://kahana.co/images/oasis/assistant-themes/` | Re-check before send |
| PH thumbnail | `https://ph-files.imgix.net/b83aefb0-b6c2-408e-b4b8-9e4a0360e1d6.png` | 200 OK |
| PH badge SVG | `https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=1146179&theme=light` | 200 OK |
| Interaction data doc | `https://kahana.co/docs/technical-and-interaction-data` | 200 OK |
| Assistant themes doc | `https://kahana.co/docs/assistant-themes` | Re-check before send |
| PH product URL (UTM) | `https://www.producthunt.com/products/kahana?embed=true&utm_source=badge-featured&utm_medium=badge&utm_campaign=badge-oasis-browser-for-mac` | Opens in browser (curl may 403) |

Re-check all assets on launch morning before send.

---

## QA before send

- [ ] No em dashes in copy
- [ ] Adam headshot loads in preview
- [ ] All 7 theme thumbnails load and link to assistant themes doc
- [ ] Zen gift card: 1M tokens/day, 6 months, $20/mo value line, 3 claim steps, screenshot reply
- [ ] Teaser does **not** include full claim steps (hint only)
- [ ] PH upvote badge at top links to UTM product page
- [ ] Primary button: **Upvote and comment on Product Hunt** (orange, UTM URL)
- [ ] Secondary button: **Create Product Hunt account** (green, producthunt.com)
- [ ] No duplicate "Follow us" button at bottom
- [ ] Copy says **"live today"**: not "tomorrow"
- [ ] Orange `#ff6154` primary button with UTM PH URL
- [ ] **No Mac download** links or `/oasis-pricing` CTAs
- [ ] PH product card thumbnail loads in preview
- [ ] PH badge image loads (if included)
- [ ] Two JSON `<pre>` blocks readable on mobile preview
- [ ] Doc link: `https://kahana.co/docs/technical-and-interaction-data`
- [ ] Tally link: `https://tally.so/r/w8V8GA`
- [ ] `{{ unsubscribe }}` and `{{ mirror }}` render in Brevo preview
- [ ] Plain-text version pasted from `brevo-oasis-ph-launch-plain-text.txt`
- [ ] No "acts on tabs/history/pages" phrasing
- [ ] Test send to yourself before bulk send

Payload source: [`data/docs/interaction-payload-examples.js`](../../data/docs/interaction-payload-examples.js)
