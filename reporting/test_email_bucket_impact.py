"""Tests for email bucket impact (V1 exposure comparison)."""

from __future__ import annotations

import unittest
from datetime import date, datetime, timedelta

import pandas as pd

from reporting.email_bucket_impact import compute_email_bucket_impact


class EmailBucketImpactTests(unittest.TestCase):
    def test_exposed_vs_not(self) -> None:
        today = date(2026, 5, 26)
        signup = today - timedelta(days=3)
        users_df = pd.DataFrame(
            [
                {
                    "user_id": "u1",
                    "created_at": pd.Timestamp(datetime.combine(signup, datetime.min.time())),
                    "signup_date": signup,
                    "plan_id": "Free",
                    "status": "active",
                    "email": "a@test.com",
                },
                {
                    "user_id": "u2",
                    "created_at": pd.Timestamp(datetime.combine(signup, datetime.min.time())),
                    "signup_date": signup,
                    "plan_id": "Free",
                    "status": "active",
                    "email": "b@test.com",
                },
            ]
        )
        activity_df = pd.DataFrame(
            [
                {"user_id": "u1", "activity_date": today},
                {"user_id": "u1", "activity_date": today - timedelta(days=1)},
            ]
        )
        outreach = [{"user_id": "u1", "trigger_name": "welcome_email"}]
        result = compute_email_bucket_impact(
            users_df=users_df,
            activity_df=activity_df,
            outreach_log=outreach,
            today=today,
            window_days=30,
        )
        self.assertEqual(result["cohort_users"], 2)
        welcome = next(
            t for t in result["by_trigger"] if t["dedup_trigger_name"] == "welcome_email"
        )
        self.assertEqual(welcome["exposed"]["users"], 1)
        self.assertEqual(welcome["not_exposed"]["users"], 1)


if __name__ == "__main__":
    unittest.main()
