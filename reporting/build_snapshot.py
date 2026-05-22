"""Build baseline snapshot from Supabase SQL export (no .env required).

Run via Supabase MCP execute_sql, save result to reporting/sql_snapshot.json,
then: python -m reporting.build_snapshot
"""

from __future__ import annotations

import json
import sys
from datetime import date, datetime
from pathlib import Path
from uuid import UUID

from models.db import (
    FeedbackEvent,
    LLMDailyUsage,
    LLMUsage,
    Payment,
    Plan,
    PlanOverride,
    Session,
    User,
    UserPlan,
)
from reporting.baseline_metrics import compute_baseline_snapshot
from reporting.run_baseline import CANVAS_PATH, SNAPSHOT_PATH, _write_canvas

ROOT = Path(__file__).resolve().parents[1]
SQL_EXPORT = ROOT / "reporting" / "sql_export.json"


def _parse_dt(v: str | None) -> datetime:
    if not v:
        return datetime.utcnow()
    s = v.replace("Z", "").split("+")[0]
    if "." in s:
        base, frac = s.split(".", 1)
        frac = (frac + "000000")[:6]
        s = f"{base}.{frac}"
    return datetime.fromisoformat(s)


def _load_export() -> dict:
    if not SQL_EXPORT.exists():
        raise FileNotFoundError(
            f"Missing {SQL_EXPORT}. Export tables via MCP first."
        )
    return json.loads(SQL_EXPORT.read_text(encoding="utf-8"))


def main() -> None:
    data = _load_export()

    users = [
        User(
            user_id=UUID(r["user_id"]),
            email=r["email"],
            name=r.get("name"),
            created_at=_parse_dt(r["created_at"]),
            status=r.get("status"),
            plan_id=r.get("plan_id"),
        )
        for r in data.get("users", [])
    ]
    sessions = [
        Session(
            session_id=UUID(r["session_id"]),
            user_id=UUID(r["user_id"]),
            started_at=_parse_dt(r["started_at"]),
            ended_at=_parse_dt(r["ended_at"]) if r.get("ended_at") else None,
        )
        for r in data.get("sessions", [])
    ]
    usage = []
    for r in data.get("llm_usage", []):
        uid = r.get("user_id")
        if not uid:
            continue
        usage.append(
            LLMUsage(
                usage_id=UUID(r["usage_id"]),
                user_id=UUID(uid),
                timestamp=_parse_dt(r["timestamp"]),
                command_type=r.get("command_type"),
                total_tokens=r.get("total_tokens"),
                input_tokens=r.get("input_tokens"),
                output_tokens=r.get("output_tokens"),
                model_used=r.get("model_used"),
            )
        )
    daily = [
        LLMDailyUsage(
            user_id=UUID(r["user_id"]),
            usage_date=date.fromisoformat(str(r["usage_date"])[:10]),
            request_count=r.get("request_count", 0),
            total_tokens=r.get("total_tokens", 0),
        )
        for r in data.get("llm_daily_usage", [])
    ]
    feedback = []
    for r in data.get("feedback_events", []):
        uid = r.get("user_id")
        if not uid:
            continue
        feedback.append(
            FeedbackEvent(
                feedback_id=UUID(r["feedback_id"]),
                user_id=UUID(uid),
                negative_rating=r.get("negative_rating"),
                category=r.get("category"),
                reported_at=_parse_dt(r["reported_at"]),
            )
        )
    plans = [Plan(**r) for r in data.get("plan", [])]
    overrides = [
        PlanOverride(
            user_id=UUID(r["user_id"]),
            limit_daily_override=r.get("limit_daily_override"),
            limit_monthly_override=r.get("limit_monthly_override"),
        )
        for r in data.get("plan_override", [])
    ]
    payments = []
    for r in data.get("payments", []):
        uid = r.get("user_id")
        payments.append(
            Payment(
                payment_id=UUID(r["payment_id"]),
                user_id=UUID(uid) if uid else None,
                amount=float(r["amount"]),
                status=r.get("status"),
                timestamp=_parse_dt(r["timestamp"]) if r.get("timestamp") else None,
            )
        )
    user_plans = []
    for r in data.get("user_plans", []):
        uid = r.get("user_id")
        user_plans.append(
            UserPlan(
                user_plan_id=UUID(r["user_plan_id"]),
                user_id=UUID(uid) if uid else None,
                start_date=_parse_dt(r["start_date"]),
                is_active=r.get("is_active", True),
            )
        )

    snapshot = compute_baseline_snapshot(
        users=users,
        sessions=sessions,
        usage=usage,
        daily=daily,
        feedback=feedback,
        plans=plans,
        overrides=overrides,
        payments=payments,
        user_plans=user_plans,
    )
    out = snapshot.to_dict()
    SNAPSHOT_PATH.write_text(json.dumps(out, indent=2), encoding="utf-8")
    _write_canvas(out)
    print(f"Wrote {SNAPSHOT_PATH} and {CANVAS_PATH}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)
