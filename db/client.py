"""Supabase PostgREST client (httpx — small bundle for Vercel serverless)."""

from __future__ import annotations

import os
from typing import Any
from urllib.parse import quote

import httpx

_PAGE_SIZE = 1000
_client: httpx.Client | None = None


def _base_url() -> str:
    url = os.environ.get("SUPABASE_URL", "").rstrip("/")
    if not url:
        raise RuntimeError("SUPABASE_URL is not set")
    return f"{url}/rest/v1"


def _api_key() -> str:
    key = os.environ.get("SUPABASE_KEY", "")
    if not key:
        raise RuntimeError("SUPABASE_KEY is not set")
    return key


def _headers(range_start: int, range_end: int) -> dict[str, str]:
    key = _api_key()
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Range": f"{range_start}-{range_end}",
        "Prefer": "count=exact",
    }


def get_http_client() -> httpx.Client:
    global _client
    if _client is None:
        _client = httpx.Client(timeout=60.0)
    return _client


def paginate_table(table: str, filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Fetch all rows from a table via PostgREST range pagination."""
    client = get_http_client()
    rows: list[dict[str, Any]] = []
    start = 0
    table_path = quote(table, safe="")

    while True:
        end = start + _PAGE_SIZE - 1
        params: dict[str, str] = {"select": "*"}
        if filters:
            for col, val in filters.items():
                params[col] = f"eq.{val}"

        resp = client.get(
            f"{_base_url()}/{table_path}",
            headers=_headers(start, end),
            params=params,
        )
        resp.raise_for_status()
        batch = resp.json()
        if not isinstance(batch, list):
            raise RuntimeError(f"Unexpected response for {table}: {type(batch)}")
        rows.extend(batch)
        if len(batch) < _PAGE_SIZE:
            break
        start += _PAGE_SIZE

    return rows


def call_rpc(
    function_name: str,
    params: dict[str, Any] | None = None,
    *,
    limit: int = 500,
) -> list[dict[str, Any]]:
    """Invoke a Postgres RPC via PostgREST (e.g. lifecycle cohort functions)."""
    client = get_http_client()
    key = _api_key()
    body = dict(params or {})
    if "p_limit" not in body:
        body["p_limit"] = limit
    resp = client.post(
        f"{_base_url()}/rpc/{quote(function_name, safe='')}",
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        },
        json=body,
    )
    resp.raise_for_status()
    data = resp.json()
    if not isinstance(data, list):
        raise RuntimeError(f"Unexpected RPC response for {function_name}: {type(data)}")
    return data
