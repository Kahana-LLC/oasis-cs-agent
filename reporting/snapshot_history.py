"""Persist and load compact daily baseline metrics for KPI deltas."""

from __future__ import annotations

import logging
from datetime import date, datetime, timedelta, timezone
from typing import Any
from urllib.parse import quote

from db.client import get_http_client, _api_key, _base_url

log = logging.getLogger(__name__)

TABLE = "baseline_metric_history"
HISTORY_OFFSETS = {"daily": 1, "weekly": 7, "monthly": 30}


def extract_compact_metrics(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Extract scalar metrics for history storage (~50 fields)."""
    launch = snapshot.get("launch_kpis") or {}
    headlines = launch.get("headlines") or {}
    churn = (snapshot.get("retention") or {}).get("churn_pct") or {}
    overall = (snapshot.get("retention") or {}).get("overall_retention_pct") or {}
    mon = snapshot.get("monetization") or {}
    dau = snapshot.get("dau_model") or {}
    totals = dau.get("totals") or {}
    buckets = dau.get("bucket_counts") or {}
    flow_pct = dau.get("flow_rates_pct") or {}

    metrics: dict[str, Any] = {
        "total_users": snapshot.get("total_users"),
        "active_users": snapshot.get("active_users"),
        "activation_24h_pct": headlines.get("activation_24h_pct"),
        "retention_d7_pct": headlines.get("retention_d7_pct") or overall.get("D7"),
        "latest_wau": headlines.get("latest_wau"),
        "premium_conversion_pct": headlines.get("premium_conversion_pct"),
        "feedback_submission_rate_pct": headlines.get("feedback_submission_rate_pct"),
        "arpu_net_usd": headlines.get("arpu_net_usd"),
        "churn_7d_pct": churn.get("churn_7d_pct"),
        "churn_14d_pct": churn.get("churn_14d_pct"),
        "churn_30d_pct": churn.get("churn_30d_pct"),
        "dau": totals.get("dau"),
        "wau": totals.get("wau"),
        "mau": totals.get("mau"),
        "token_limit_hit_rate_pct": mon.get("token_limit_hit_rate_pct"),
        "limit_hitter_conversion_pct": mon.get(
            "premium_conversion_among_limit_hitters_pct"
        ),
        "median_days_to_first_limit": mon.get("median_days_to_first_limit"),
    }

    for key in (
        "new",
        "current",
        "reactivated",
        "resurrected",
        "at_risk_wau",
        "at_risk_mau",
        "dead",
    ):
        metrics[f"bucket_{key}"] = buckets.get(key)

    for rate_key, pct in flow_pct.items():
        metrics[f"flow_{rate_key}"] = pct

    return metrics


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


def upsert_history_row(snapshot_date: date, metrics: dict[str, Any]) -> None:
    """Upsert one day's compact metrics (service role)."""
    now = datetime.now(timezone.utc).isoformat()
    row = {
        "snapshot_date": str(snapshot_date),
        "metrics": metrics,
        "updated_at": now,
    }
    client = get_http_client()
    path = quote(TABLE, safe="")
    resp = client.post(
        f"{_base_url()}/{path}",
        headers=_write_headers(prefer="resolution=merge-duplicates"),
        json=row,
    )
    if resp.status_code >= 400:
        raise RuntimeError(
            f"upsert {TABLE} failed ({resp.status_code}): {resp.text[:500]}"
        )


def fetch_history_rows(dates: list[date]) -> dict[str, dict[str, Any]]:
    """Return {snapshot_date_str: metrics} for rows that exist."""
    if not dates:
        return {}
    date_strs = [str(d) for d in dates]
    in_filter = "(" + ",".join(date_strs) + ")"
    client = get_http_client()
    path = quote(TABLE, safe="")
    resp = client.get(
        f"{_base_url()}/{path}",
        headers=_write_headers(),
        params={
            "select": "snapshot_date,metrics",
            "snapshot_date": f"in.{in_filter}",
        },
    )
    if resp.status_code == 404:
        log.warning("%s table not found — apply baseline_metric_history migration", TABLE)
        return {}
    resp.raise_for_status()
    out: dict[str, dict[str, Any]] = {}
    for row in resp.json():
        out[str(row["snapshot_date"])] = row.get("metrics") or {}
    return out


def fetch_history_for_deltas(today: date) -> dict[str, dict[str, Any] | None]:
    """Load prior compact metrics for daily (T-1), weekly (T-7), monthly (T-30)."""
    targets = {
        period: today - timedelta(days=offset)
        for period, offset in HISTORY_OFFSETS.items()
    }
    by_date = fetch_history_rows(list(targets.values()))
    return {
        period: by_date.get(str(target_date))
        for period, target_date in targets.items()
    }


def enrich_snapshot_with_history(
    snapshot: dict[str, Any],
    *,
    persist: bool = True,
) -> dict[str, Any]:
    """Upsert today, attach deltas, goals, insights, and goal-aware tooltips."""
    from reporting.goal_aware_tooltips import build_all_tooltips
    from reporting.goal_progress import compute_goal_progress
    from reporting.goals_state import load_goals_state, maybe_lock_dau_baseline, save_goals_state
    from reporting.insights import generate_key_insights
    from reporting.launch_kpis import attach_tooltips_to_kpi_rows
    from reporting.metric_deltas import build_all_period_deltas

    today = date.fromisoformat(snapshot["snapshot_date"])
    current = extract_compact_metrics(snapshot)

    if persist:
        try:
            upsert_history_row(today, current)
        except Exception as exc:
            log.warning("failed to upsert metric history: %s", exc)

    priors = fetch_history_for_deltas(today)
    snapshot["deltas"] = build_all_period_deltas(current, priors, today)

    goals_state: dict = {}
    try:
        goals_state = load_goals_state()
        goals_state = maybe_lock_dau_baseline(today, goals_state)
        if persist:
            save_goals_state(goals_state)
    except Exception as exc:
        log.warning("goals state skipped: %s", exc)

    snapshot["corporate_goals"] = compute_goal_progress(
        snapshot, snapshot["deltas"], goals_state, today=today
    )

    try:
        from reporting.email_provider_capacity import compute_email_provider_capacity

        snapshot["email_provider_capacity"] = compute_email_provider_capacity(snapshot)
    except Exception as exc:
        log.warning("email provider capacity skipped: %s", exc)
        snapshot.setdefault("email_provider_capacity", {"providers": [], "any_near_limit": False})

    snapshot["key_insights"] = generate_key_insights(
        snapshot, snapshot["deltas"], snapshot["corporate_goals"]
    )
    snapshot["metric_tooltips"] = build_all_tooltips(
        snapshot, snapshot["deltas"], snapshot["corporate_goals"]
    )

    launch = snapshot.get("launch_kpis")
    if launch and launch.get("kpi_rows"):
        launch["kpi_rows"] = attach_tooltips_to_kpi_rows(
            launch["kpi_rows"], snapshot.get("metric_tooltips")
        )

    return snapshot
