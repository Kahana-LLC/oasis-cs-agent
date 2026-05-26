"""Tests for lifecycle email send coverage."""

from __future__ import annotations

import unittest
from datetime import date, datetime, timedelta

import pandas as pd

from reporting.lifecycle_email_sends import compute_lifecycle_email_sends


def _users_df(user_specs: list[tuple[str, date, str]]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "user_id": uid,
                "created_at": pd.Timestamp(datetime.combine(signup, datetime.min.time())),
                "signup_date": signup,
                "plan_id": "Free",
                "status": status,
            }
            for uid, signup, status in user_specs
        ]
    )


class LifecycleEmailSendsTests(unittest.TestCase):
    def test_cohort_send_counts(self) -> None:
        today = date(2026, 5, 26)
        signup = today - timedelta(days=5)
        old_signup = today - timedelta(days=40)

        users_df = _users_df(
            [
                ("u1", signup, "active"),
                ("u2", signup, "active"),
                ("u3", old_signup, "active"),
            ]
        )
        activity_df = pd.DataFrame(
            [
                {"user_id": "u1", "activity_date": today},
                {"user_id": "u2", "activity_date": today - timedelta(days=20)},
            ]
        )
        outreach_log = [
            {"user_id": "u1", "trigger_name": "welcome_email"},
            {"user_id": "u1", "trigger_name": "nps_day3"},
            {"user_id": "u2", "trigger_name": "welcome_email"},
            {"user_id": "u3", "trigger_name": "welcome_email"},
        ]

        result = compute_lifecycle_email_sends(
            users_df=users_df,
            activity_df=activity_df,
            outreach_log=outreach_log,
            outreach_log_available=True,
            today=today,
            window_days=30,
        )

        cohort = result["cohort"]
        self.assertEqual(cohort["users"], 2)
        by_trigger = {t["dedup_trigger_name"]: t for t in cohort["triggers"]}
        self.assertEqual(by_trigger["welcome_email"]["sent_count"], 2)
        self.assertEqual(by_trigger["welcome_email"]["pct_of_cohort"], 100.0)
        self.assertEqual(by_trigger["nps_day3"]["sent_count"], 1)
        self.assertEqual(by_trigger["nps_day3"]["pct_of_cohort"], 50.0)
        self.assertEqual(cohort["users_with_any_lifecycle_email"], 2)

    def test_outreach_unavailable(self) -> None:
        today = date(2026, 5, 26)
        users_df = _users_df([("u1", today - timedelta(days=3), "active")])
        result = compute_lifecycle_email_sends(
            users_df=users_df,
            activity_df=pd.DataFrame(),
            outreach_log=[],
            outreach_log_available=False,
            today=today,
        )
        self.assertFalse(result["outreach_log_available"])
        self.assertEqual(result["cohort"]["users"], 1)
        for t in result["cohort"]["triggers"]:
            self.assertEqual(t["sent_count"], 0)


if __name__ == "__main__":
    unittest.main()
