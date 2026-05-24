"""Sync Brevo email HTML fragments into public/emails/ for /email-machine previews."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MERGE_TAG_SAMPLES = {
    r"\{\{\s*contact\.FIRSTNAME\s*\}\}": "Alex",
    r"\{\{\s*contact\.EMAIL\s*\}\}": "alex@example.com",
    r"\{\{\s*mirror\s*\}\}": "",
    r"\{\{\s*unsubscribe\s*\}\}": "#unsubscribe-preview",
}


def substitute_preview_tags(html: str) -> str:
    """Replace Brevo merge tags with sample values for browser preview."""
    out = html
    for pattern, replacement in MERGE_TAG_SAMPLES.items():
        out = re.sub(pattern, replacement, out, flags=re.IGNORECASE)
    return out


def wrap_brevo_fragment(html: str, *, title: str = "Email preview") -> str:
    """Wrap a Brevo table fragment in a minimal HTML document for iframe display."""
    return (
        "<!DOCTYPE html>\n"
        f'<html lang="en"><head><meta charset="utf-8">'
        f"<title>{title}</title></head>\n"
        '<body style="margin:0;padding:0;">\n'
        f"{html}\n"
        "</body></html>"
    )


def _preview_source(seq: dict) -> str | None:
    preview = seq.get("preview")
    if isinstance(preview, dict) and preview.get("source"):
        return str(preview["source"])
    legacy = seq.get("preview_path")
    if legacy:
        return None
    return None


def _preview_out_path(seq: dict) -> Path | None:
    preview = seq.get("preview")
    if isinstance(preview, dict) and preview.get("path"):
        rel = str(preview["path"]).lstrip("/")
        if rel.startswith("emails/"):
            return Path(rel)
    seq_id = seq.get("id")
    if seq_id and isinstance(preview, dict) and preview.get("source"):
        return Path("emails") / f"{seq_id}.html"
    return None


def sync_previews(
    manifest_path: Path | None = None,
    out_dir: Path | None = None,
    *,
    repo_root: Path | None = None,
) -> int:
    """Copy and wrap preview HTML from brevo-oasis-emails into public/emails/."""
    repo_root = repo_root or ROOT
    manifest_path = manifest_path or repo_root / "public" / "email_sequences.json"
    out_dir = out_dir or repo_root / "public" / "emails"

    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    sequences = data.get("sequences") or []
    synced = 0
    out_dir.mkdir(parents=True, exist_ok=True)

    for seq in sequences:
        source_rel = _preview_source(seq)
        out_rel = _preview_out_path(seq)
        if not source_rel or not out_rel:
            continue

        source_path = repo_root / source_rel
        if not source_path.is_file():
            raise FileNotFoundError(f"Preview source missing for {seq.get('id')}: {source_path}")

        fragment = source_path.read_text(encoding="utf-8")
        fragment = substitute_preview_tags(fragment)
        wrapped = wrap_brevo_fragment(fragment, title=str(seq.get("name", "Preview")))
        dest = out_dir / out_rel.name
        dest.write_text(wrapped, encoding="utf-8")
        synced += 1

    return synced
