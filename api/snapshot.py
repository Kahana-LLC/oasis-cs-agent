"""Vercel serverless: fresh baseline metrics from Supabase on each GET."""

from __future__ import annotations

import json
import logging
import os
import sys
import time
import traceback
from http.server import BaseHTTPRequestHandler
from pathlib import Path

# Repo root on sys.path for Vercel Python functions
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

log = logging.getLogger(__name__)

_cache: dict | None = None
_cache_at: float = 0.0


def _cache_seconds() -> int:
    try:
        return int(os.environ.get("SNAPSHOT_CACHE_SECONDS", "0"))
    except ValueError:
        return 0


def _get_snapshot() -> dict:
    global _cache, _cache_at
    ttl = _cache_seconds()
    now = time.time()
    if ttl > 0 and _cache is not None and (now - _cache_at) < ttl:
        return _cache

    from reporting.snapshot_service import build_snapshot_dict

    data = build_snapshot_dict()
    if ttl > 0:
        _cache = data
        _cache_at = now
    return data


def _json_response(handler: BaseHTTPRequestHandler, status: int, body: dict) -> None:
    payload = json.dumps(body).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
    handler.send_header("Content-Length", str(len(payload)))
    handler.end_headers()
    handler.wfile.write(payload)


class handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path.split("?", 1)[0].rstrip("/") not in ("", "/api/snapshot", "/snapshot"):
            _json_response(self, 404, {"error": "Not found"})
            return

        for key in ("SUPABASE_URL", "SUPABASE_KEY"):
            if not os.environ.get(key):
                _json_response(
                    self,
                    500,
                    {"error": f"Missing environment variable: {key}"},
                )
                return

        try:
            data = _get_snapshot()
            _json_response(self, 200, data)
        except Exception as exc:
            log.exception("snapshot API failed")
            body: dict = {"error": str(exc)}
            if os.environ.get("SNAPSHOT_DEBUG", "").lower() in ("1", "true", "yes"):
                body["detail"] = traceback.format_exc()
            _json_response(self, 500, body)

    def log_message(self, format: str, *args) -> None:
        log.info("%s - %s", self.address_string(), format % args)
