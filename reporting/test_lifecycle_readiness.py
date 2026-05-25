"""Tests for lifecycle readiness by DAU bucket."""

from __future__ import annotations

import unittest
from datetime import date, datetime, timedelta

import pandas as pd

from reporting.lifecycle_readiness import compute_lifecycle_readiness_by_bucket


def _users_df(user_specs: list[tuple[str, date]]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "user_id": uid,
                "created_at": pd.Timestamp(datetime.combine(signup, datetime.min.time())),
                "signup_date": signup,
                "plan_id": "Free",
                "status": "active",
            }
            for uid, signup in user_specs
        ]
    )


class LifecycleReadinessTests(unittest.TestCase):
    def test_product_milestones_by_bucket(self) -> None:
        today = date(2026, 5, 24)
        signup = today - timedelta(days=10)

        users_df = _users_df(
            [("u1", signup), ("u2", signup), ("u3", signup - timedelta(days=40))]
        )

        activity_df = pd.DataFrame(
            [
                {"user_id": "u1", "activity_date": today},
                {"user_id": "u2", "activity_date": today - timedelta(days=20)},
                {"user_id": "u3", "activity_date": today - timedelta(days=35)},
            ]
        )

        usage_df = pd.DataFrame(
            [
                {
                    "user_id": "u1",
                    "timestamp": pd.Timestamp(datetime.combine(today, datetime.min.time())),
                    "activity_date": today,
                },
                {
                    "user_id": "u2",
                    "timestamp": pd.Timestamp(
                        datetime.combine(today - timedelta(days=5), datetime.min.time())
                    ),
                    "activity_date": today - timedelta(days=5),
                },
            ]
        )

        result = compute_lifecycle_readiness_by_bucket(
            users_df=users_df,
            activity_df=activity_df,
            usage_df=usage_df,
            daily_df=pd.DataFrame(columns=["user_id", "usage_date", "total_tokens"]),
            feedback=[],
            plans=[],
            overrides=[],
            today=today,
        )

        self.assertEqual(result["product_milestone_count"], 3)
        self.assertEqual(len(result["milestones"]), 6)
        pending = [m for m in result["milestones"] if m["status"] == "pending"]
        self.assertEqual(len(pending), 3)

        by_bucket = result["by_bucket"]
        bucket_sum = (
            by_bucket["new"]["users"]
            + by_bucket["dead"]["users"]
            + by_bucket["at_risk_mau"]["users"]
        )
        self.assertEqual(bucket_sum, 3)

        new_prompt = by_bucket["new"]["milestones"]["first_ai_prompt"]
        self.assertEqual(new_prompt["count"], 1)
        self.assertEqual(new_prompt["pct"], 100.0)

        totals = result["totals"]
        self.assertEqual(totals["milestones"]["first_ai_prompt"]["count"], 2)
        self.assertEqual(totals["max_score"], 3)

    def test_email_milestones_live_with_outreach_log(self) -> None:
        today = date(2026, 5, 24)
        users_df = _users_df([("u1", today - timedelta(days=1))])
        activity_df = pd.DataFrame([{"user_id": "u1", "activity_date": today}])

        result = compute_lifecycle_readiness_by_bucket(
            users_df=users_df,
            activity_df=activity_df,
            usage_df=pd.DataFrame(columns=["user_id", "timestamp", "activity_date"]),
            daily_df=pd.DataFrame(columns=["user_id", "usage_date", "total_tokens"]),
            feedback=[],
            plans=[],
            overrides=[],
            today=today,
            outreach_log=[{"user_id": "u1", "trigger_name": "welcome_email"}],
        )

        live = [m for m in result["milestones"] if m["status"] == "live"]
        self.assertEqual(len(live), 6)
        welcome = result["by_bucket"]["new"]["milestones"].get("welcome_sent")
        self.assertIsNotNone(welcome)
        assert welcome is not None
        self.assertEqual(welcome["count"], 1)


if __name__ == "__main__":
    unittest.main()
