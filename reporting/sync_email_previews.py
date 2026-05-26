"""Sync Brevo email HTML fragments into public/emails/ for /email-machine previews."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterator

ROOT = Path(__file__).resolve().parents[1]

MERGE_TAG_SAMPLES = {
    r"\{\{\s*contact\.FIRSTNAME\s*\}\}": "Alex",
    r"\{\{\s*contact\.EMAIL\s*\}\}": "alex@example.com",
    r"\{\{\s*params\.GREETING\s*\}\}": "Hi Alex,",
    r"\{\{\s*params\.EMAIL\s*\}\}": "alex@example.com",
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


def _preview_key_from_path(path: str | None) -> str | None:
    if not path:
        return None
    name = str(path).lstrip("/").split("/")[-1]
    if name.endswith(".html"):
        return name[: -len(".html")]
    return name or None


def iter_preview_jobs(
    sequences: list[dict],
) -> Iterator[tuple[str, dict, str]]:
    """Yield (output_key, preview_dict, title) for sequence- and touch-level previews."""
    for seq in sequences:
        seq_name = str(seq.get("name") or "Preview")
        touches = seq.get("touches") or []
        touch_jobs = [
            (str(t["touch_id"]), t["preview"], str(t.get("name") or seq_name))
            for t in touches
            if t.get("touch_id")
            and isinstance(t.get("preview"), dict)
            and t["preview"].get("source")
        ]
        if touch_jobs:
            for key, preview, title in touch_jobs:
                yield key, preview, title
            continue

        preview = seq.get("preview")
        if not isinstance(preview, dict) or not preview.get("source"):
            continue
        key = _preview_key_from_path(preview.get("path")) or str(seq.get("id") or "")
        if not key:
            continue
        yield key, preview, seq_name


def _preview_out_path(preview: dict, key: str) -> Path:
    if preview.get("path"):
        rel = str(preview["path"]).lstrip("/")
        if rel.startswith("emails/"):
            return Path(rel)
    return Path("emails") / f"{key}.html"


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

    for key, preview, title in iter_preview_jobs(sequences):
        source_rel = str(preview["source"])
        source_path = repo_root / source_rel
        if not source_path.is_file():
            raise FileNotFoundError(f"Preview source missing for {key}: {source_path}")

        fragment = source_path.read_text(encoding="utf-8")
        fragment = substitute_preview_tags(fragment)
        wrapped = wrap_brevo_fragment(fragment, title=title)
        dest = out_dir / _preview_out_path(preview, key).name
        dest.write_text(wrapped, encoding="utf-8")
        synced += 1

    return synced


def sync_copy_manifest(
    manifest_path: Path | None = None,
    out_dir: Path | None = None,
    *,
    repo_root: Path | None = None,
) -> int:
    """Write raw HTML/plain-text sources for Copy buttons on /email-machine."""
    repo_root = repo_root or ROOT
    manifest_path = manifest_path or repo_root / "public" / "email_sequences.json"
    out_dir = out_dir or repo_root / "public" / "emails"

    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    sequences = data.get("sequences") or []
    copy_data: dict[str, dict[str, str]] = {}

    for key, preview, _title in iter_preview_jobs(sequences):
        source_path = repo_root / str(preview["source"])
        if not source_path.is_file():
            raise FileNotFoundError(f"Copy source missing for {key}: {source_path}")

        entry: dict[str, str] = {
            "html": source_path.read_text(encoding="utf-8"),
            "source_path": str(preview["source"]),
        }
        for meta_key in ("subject", "preheader", "deploy_provider", "from_name"):
            val = preview.get(meta_key)
            if val:
                entry[meta_key] = str(val)
        plain_rel = preview.get("plain_text_source")
        if plain_rel:
            plain_path = repo_root / str(plain_rel)
            if plain_path.is_file():
                entry["plain_text"] = plain_path.read_text(encoding="utf-8")
        copy_data[key] = entry

    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "copy_manifest.json"
    dest.write_text(json.dumps(copy_data, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(copy_data)
