"""Load/save corporate goals state and lock DAU launch-week baseline."""

from __future__ import annotations

import logging
from datetime import date, timedelta
from typing import Any
from urllib.parse import quote

from db.client import get_http_client, _api_key, _base_url
from reporting.corporate_goals import (
    DAU_BASELINE_WINDOW_DAYS,
    PRODUCT_HUNT_LAUNCH_DATE,
)
from reporting.snapshot_history import fetch_history_rows

log = logging.getLogger(__name__)

TABLE = "corporate_goals_state"
STATE_ID = 1


def _write_headers(*, prefer: str | None = None) -> dict[str, str]:
    key = _api_key()
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    if prefer:
        headers["Prefer"] = prefer
    return headers


def load_goals_state() -> dict[str, Any]:
    """Return goals state dict (empty if table missing or no row)."""
    client = get_http_client()
    path = quote(TABLE, safe="")
    resp = client.get(
        f"{_base_url()}/{path}",
        headers=_write_headers(),
        params={"select": "state", "id": f"eq.{STATE_ID}"},
    )
    if resp.status_code == 404:
        log.warning("%s table not found — apply corporate_goals_state migration", TABLE)
        return {}
    resp.raise_for_status()
    rows = resp.json()
    if not rows:
        return {}
    return rows[0].get("state") or {}


def save_goals_state(state: dict[str, Any]) -> None:
    """Upsert single goals state row."""
    from datetime import datetime, timezone

    client = get_http_client()
    path = quote(TABLE, safe="")
    row = {
        "id": STATE_ID,
        "state": state,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    resp = client.post(
        f"{_base_url()}/{path}",
        headers=_write_headers(prefer="resolution=merge-duplicates"),
        json=row,
    )
    if resp.status_code >= 400:
        raise RuntimeError(
            f"upsert {TABLE} failed ({resp.status_code}): {resp.text[:500]}"
        )


def _launch_week_dates() -> list[date]:
    start = PRODUCT_HUNT_LAUNCH_DATE
    return [start + timedelta(days=i) for i in range(DAU_BASELINE_WINDOW_DAYS)]


def maybe_lock_dau_baseline(today: date, state: dict[str, Any]) -> dict[str, Any]:
    """After launch+7d, set dau_yoy_baseline from avg DAU in first 7 days post-launch."""
    if state.get("dau_yoy_baseline") is not None:
        return state

    lock_after = PRODUCT_HUNT_LAUNCH_DATE + timedelta(days=DAU_BASELINE_WINDOW_DAYS)
    if today < lock_after:
        return state

    week_dates = _launch_week_dates()
    by_date = fetch_history_rows(week_dates)
    dau_vals = []
    for d in week_dates:
        m = by_date.get(str(d)) or {}
        if m.get("dau") is not None:
            dau_vals.append(float(m["dau"]))

    if not dau_vals:
        log.info("DAU baseline not locked yet — no history for launch week")
        return state

    baseline = round(sum(dau_vals) / len(dau_vals), 2)
    state = dict(state)
    state["dau_yoy_baseline"] = baseline
    state["dau_yoy_baseline_locked_at"] = str(today)
    state["dau_yoy_baseline_days_used"] = len(dau_vals)
    log.info("locked DAU launch-week baseline: %s (from %d days)", baseline, len(dau_vals))
    return state
