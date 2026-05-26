"""Tests for lifecycle email delivery gaps."""

from __future__ import annotations

import unittest
from datetime import date, datetime, timedelta

import pandas as pd

from reporting.lifecycle_email_delivery import compute_lifecycle_email_delivery


def _users_df(specs: list[tuple[str, date]]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "user_id": uid,
                "created_at": pd.Timestamp(datetime.combine(d, datetime.min.time())),
                "signup_date": d,
                "plan_id": "Free",
                "status": "active",
                "email": f"{uid}@test.com",
            }
            for uid, d in specs
        ]
    )


class LifecycleEmailDeliveryTests(unittest.TestCase):
    def test_missed_welcome(self) -> None:
        today = date(2026, 5, 26)
        signup = today - timedelta(days=1)
        users_df = _users_df([("u1", signup)])
        result = compute_lifecycle_email_delivery(
            users_df=users_df,
            usage_df=pd.DataFrame(),
            feedback_user_ids=set(),
            outreach_log=[],
            outreach_log_available=True,
            rpc_fetcher=None,
            today=today,
            window_days=30,
        )
        by_name = {t["dedup_trigger_name"]: t for t in result["triggers"]}
        self.assertEqual(by_name["welcome_email"]["missed_overdue"], 1)

    def test_sent_in_window(self) -> None:
        today = date(2026, 5, 26)
        signup = today - timedelta(days=5)
        users_df = _users_df([("u1", signup), ("u2", signup)])
        outreach = [{"user_id": "u1", "trigger_name": "welcome_email", "sent_at": "2026-05-20T12:00:00Z"}]
        result = compute_lifecycle_email_delivery(
            users_df=users_df,
            usage_df=pd.DataFrame(),
            feedback_user_ids=set(),
            outreach_log=outreach,
            outreach_log_available=True,
            today=today,
            window_days=30,
        )
        by_name = {t["dedup_trigger_name"]: t for t in result["triggers"]}
        self.assertEqual(by_name["welcome_email"]["sent_in_window"], 1)


if __name__ == "__main__":
    unittest.main()
