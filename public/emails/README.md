# Email HTML previews (generated)

**Do not edit files in this folder directly.** They are built from canonical sources in [`brevo-oasis-emails/`](../../brevo-oasis-emails/) at deploy time.

## How it works

1. Edit HTML in `brevo-oasis-emails/` (lifecycle, ph-waitlist, etc.).
2. Set or update the sequence’s `preview` object in [`public/email_sequences.json`](../email_sequences.json):

   ```json
   "preview": {
     "source": "brevo-oasis-emails/lifecycle/brevo-oasis-welcome.html",
     "path": "/emails/welcome.html",
     "subject": "Welcome to Oasis",
     "preheader": "Docs, Slack, and support links to get started.",
     "from_name": "Adam from Oasis"
   }
   ```

3. Run the build script — it wraps Brevo table fragments in a minimal HTML document, substitutes sample merge tags (e.g. `Alex`), and writes `public/emails/<sequence_id>.html`:

   ```bash
   python reporting/build_static_site.py
   ```

4. Open [`/email-machine`](../email-machine.html) — project charter with DAU buckets, sequence reference, capacity panel, preview gallery, and **Copy HTML** buttons (raw Brevo fragments from `copy_manifest.json`).

`public/emails/*.html` and `copy_manifest.json` are gitignored; Vercel runs the build on every deploy so previews never drift from source.

## Copy manifest

`copy_manifest.json` maps sequence IDs to raw HTML (with Brevo merge tags intact) and optional plain text for clipboard copy on `/email-machine`. Generated alongside preview HTML by `sync_copy_manifest()` in [`reporting/sync_email_previews.py`](../../reporting/sync_email_previews.py).

## Shipped previews (6)

| Output file | Sequence ID | Source |
|-------------|-------------|--------|
| `welcome.html` | `welcome` | `lifecycle/brevo-oasis-welcome.html` |
| `nps_day3.html` | `nps_day3` | `lifecycle/brevo-oasis-nps-day3.html` |
| `pmf_day10.html` | `pmf_day10` | `lifecycle/brevo-oasis-pmf-day10.html` |
| `upgrade_thank_you.html` | `upgrade_thank_you` | `lifecycle/brevo-oasis-paid-zen-welcome.html` |
| `ph_teaser.html` | `ph_teaser` | `ph-waitlist/brevo-oasis-ph-teaser-waitlist.html` |
| `ph_launch.html` | `ph_launch` | `ph-waitlist/brevo-oasis-ph-launch-waitlist.html` |

Sequences without `preview.source` show a placeholder on `/email-machine` until a Brevo template exists.
