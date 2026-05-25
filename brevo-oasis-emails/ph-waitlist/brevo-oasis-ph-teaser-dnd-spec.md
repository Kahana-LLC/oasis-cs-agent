# Brevo drag-and-drop spec: Product Hunt teaser (May 26)

Edit your **existing** Brevo D&D template (v3.0.1) in the visual editor. Do **not** paste full HTML into the raw-html block.

**Audience:** Oasis waitlist (Tally `w8V8GA` → Brevo list)  
**Send:** May 26, 2026 (morning PDT)  
**Full HTML reference:** `brevo-oasis-ph-teaser-waitlist.html`  
**Payload-only paste:** `brevo-oasis-ph-payload-snippets.html`  
**Founder intro:** `brevo-oasis-ph-founder-intro-snippet.html`  
**Founder signoff:** `brevo-oasis-ph-founder-signoff-snippet.html`  
**Theme gallery (bottom):** `brevo-oasis-ph-theme-gallery-snippet.html`  
**Tally form (in-email):** `brevo-oasis-ph-tally-form-snippet.html`: see [`brevo-oasis-ph-tally-form-setup.md`](brevo-oasis-ph-tally-form-setup.md)  
**Zen gift teaser:** [`brevo-oasis-ph-zen-gift-teaser-snippet.html`](brevo-oasis-ph-zen-gift-teaser-snippet.html) (hint only; paste after platform paragraph, before Tally)

---

## Campaign setup (Setup step)

| Field | Value |
|-------|--------|
| Brevo template name | `Oasis PH Teaser` |
| Subject | `Tomorrow on Product Hunt (+ a launch-day surprise)` |
| Preheader | `Privacy-first AI browser. Something special for genuine launch-day feedback.` |
| From name | `Adam from Oasis` |

---

## Global styles (Styles panel)

| Style token | Property | Value |
|-------------|----------|-------|
| `default-button` | `background-color`, `border-color` | `#4A6200` |
| `default-link` | `color` | `#4A6200` |
| `default-heading2` | `color` | `#313A00` |
| `default` | `color` | `#4A5745` |

---

## Block checklist

### Keep as-is

| Block | Notes |
|-------|-------|
| View in browser | Uses `{{ mirror }}` |
| Logo | Brevo CDN Kahana logo |
| Social | LinkedIn, YouTube, Instagram, website, Discord |
| Spacer | Optional |

### Update content

| Block | Action |
|-------|-------|
| Title | `Oasis launches on Product Hunt tomorrow` |
| Image (hero) | **Delete** old hero screenshot and top theme gallery |
| Body | Founder intro + platform + Tally + JSON + personal close + PH CTA + signoff + bottom theme gallery |
| Founder intro | Paste [`brevo-oasis-ph-founder-intro-snippet.html`](brevo-oasis-ph-founder-intro-snippet.html) first in body (includes founder row, then `Hi {{ contact.FIRSTNAME }},`) |
| Zen gift teaser | Paste [`brevo-oasis-ph-zen-gift-teaser-snippet.html`](brevo-oasis-ph-zen-gift-teaser-snippet.html) after Mac platform paragraph, before Tally |
| Founder signoff | Paste [`brevo-oasis-ph-founder-signoff-snippet.html`](brevo-oasis-ph-founder-signoff-snippet.html) after PH button |
| Theme gallery | Paste [`brevo-oasis-ph-theme-gallery-snippet.html`](brevo-oasis-ph-theme-gallery-snippet.html) at bottom, before footer |
| Tally form | Paste [`brevo-oasis-ph-tally-form-snippet.html`](brevo-oasis-ph-tally-form-snippet.html) after platform paragraph |
| Button 1 | **Only button:** Follow us on Product Hunt → `https://www.producthunt.com/products/kahana` |

**Body opening**: paste founder snippet at top of body (photo/name, then greeting):

Use the teaser variant from [`brevo-oasis-ph-founder-intro-snippet.html`](brevo-oasis-ph-founder-intro-snippet.html) (headshot table + opening paragraphs). Or paste this:

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
<p>Thanks for joining the Oasis waitlist. Tomorrow, <strong>Wednesday, May 27</strong>, we're launching Oasis on Product Hunt and I wanted to share it with you directly.</p>
<p>Chrome was never built for privacy, and the AI in today's "private" browsers still lags behind. Oasis is a privacy-first AI browser <strong>you can train</strong>. Your personal data is sacred, and all interaction data is anonymized by default.</p>
<p>The version launching on Product Hunt is <strong>Oasis for Mac</strong>, <strong>desktop only</strong>, built on <strong>Firefox</strong>, for <strong>Apple Silicon and Intel</strong>.</p>
<p><strong>Mobile</strong> and a <strong>Chromium</strong>-engine build for <strong>Windows, Mac, and Linux</strong> are coming soon. Tell us what to notify you about:</p>
```

Then paste [`brevo-oasis-ph-tally-form-snippet.html`](brevo-oasis-ph-tally-form-snippet.html) into a **Text block** (source mode). Configure Tally hidden fields first: see [`brevo-oasis-ph-tally-form-setup.md`](brevo-oasis-ph-tally-form-setup.md).

**Note:** Email clients cannot embed a live Tally iframe. The snippet uses tappable buttons that open a pre-filled form in the browser (Tally's recommended approach).

**Theme gallery:** paste [`brevo-oasis-ph-theme-gallery-snippet.html`](brevo-oasis-ph-theme-gallery-snippet.html) at the **bottom** of the body (after signoff), before fallback links.

**Founder signoff:** paste [`brevo-oasis-ph-founder-signoff-snippet.html`](brevo-oasis-ph-founder-signoff-snippet.html) after the PH button. Links to `https://kahana.co/adam-kershner`.

**Transparent by default + JSON**: paste contents of [`brevo-oasis-ph-payload-snippets.html`](brevo-oasis-ph-payload-snippets.html) into a second Text block (source mode).

**Personal close** (before PH CTA):

```html
<p>I would really love your thoughts and feedback if you get a chance to check it out. We are genuinely trying to build something meaningful that helps people with both privacy and productivity.</p>
<p>Thanks so much for the consideration. It means a lot.</p>
<p>To stay in the loop on launch day, new versions, and new features, <strong>follow us on Product Hunt</strong>. It's the best way to get updates as we ship.</p>
```

### Remove

| Block | Action |
|-------|--------|
| Download for Mac button | **Delete**: no Mac download CTA |
| raw-html block | **Delete** unless using inline fallback below |
| Navigation placeholders | **Delete** |
| Old hero screenshot | **Delete** |
| Top theme gallery | **Delete** if present |

**Fallback links** (optional Text block):

```html
<p style="font-size:14px;color:#6b7355;">If the button doesn't work: <a href="https://www.producthunt.com/products/kahana">Product Hunt</a> · <a href="https://kahana.co/adam-kershner">All my socials</a> · <a href="https://kahana.co/docs">Browse docs</a> · <a href="https://kahanaworkspace.slack.com/archives/C0B3QDPLH4P">Join Slack</a> · <a href="https://kahana.co/contact">Contact us</a> · <a href="https://kahana.co/docs/technical-and-interaction-data">Interaction data doc</a> · <a href="https://tally.so/r/w8V8GA">Choose your version</a></p>
```

**Footer support links:** paste [`brevo-oasis-support-links-snippet.html`](../shared/brevo-oasis-support-links-snippet.html) in the footer area above Privacy Policy.

---

## Plain-text version

Paste entire contents of [`brevo-oasis-ph-teaser-plain-text.txt`](brevo-oasis-ph-teaser-plain-text.txt) into Brevo **Plain-text** tab.

Payload source: `data/docs/interaction-payload-examples.js`

---

## QA before send

- [ ] No em dashes in copy
- [ ] Adam headshot loads: `https://kahana.co/images/about/adam-kershner.jpg`
- [ ] All 7 theme thumbnails load and link to assistant themes doc
- [ ] No "acts on tabs/history/pages" phrasing
- [ ] Single button only (Product Hunt)
- [ ] JSON `<pre>` blocks render in preview
- [ ] Doc link works: `https://kahana.co/docs/technical-and-interaction-data`
- [ ] Copy says "tomorrow": not "we're live"
- [ ] Tally form card pasted; hidden fields configured in Tally (see `brevo-oasis-ph-tally-form-setup.md`)
- [ ] Test email: each Browser Engine button opens pre-filled Tally form

---

## After teaser ships

Duplicate in Brevo and follow `brevo-oasis-ph-launch-dnd-spec.md` for May 27.
