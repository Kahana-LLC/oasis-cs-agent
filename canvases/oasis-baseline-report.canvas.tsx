import {
  BarChart,
  LineChart,
  Callout,
  Card,
  CardBody,
  CardHeader,
  CollapsibleSection,
  Divider,
  Grid,
  H1,
  H2,
  H3,
  Row,
  Stack,
  Stat,
  Table,
  Text,
  useHostTheme,
} from "cursor/canvas";

const BASELINE = {
  "generated_at": "2026-05-26T02:36:41.987379Z",
  "snapshot_date": "2026-05-25",
  "total_users": 122,
  "active_users": 122,
  "limitations": [
    "Small sample size (122 users) \u2014 percentages are directional.",
    "First AI command inferred from llm_usage.timestamp (no first_command_at column).",
    "Token limits inferred from llm_daily_usage vs plan limits, not UX events.",
    "NULL plan_id treated as Free (121/122 users historically).",
    "CAC unavailable \u2014 user_acquisition and events tables empty.",
    "Feedback quality requires manual review of sampled rows.",
    "DAU buckets use sessions \u222a llm_usage; flow rates are 7-day average daily transitions."
  ],
  "activation": {
    "total_users": 122,
    "users_with_first_prompt": 70,
    "activation_rate_pct": {
      "1h": 27.0,
      "24h": 31.1,
      "3d": 32.8,
      "7d": 37.7
    },
    "time_to_first_hours": {
      "median": 5.54,
      "mean": 421.82
    }
  },
  "engagement": {
    "prompts_per_active_day_by_cohort": [
      {
        "cohort": "2025-08-18/2025-08-24",
        "avg_prompts_per_active_day": 0.0
      },
      {
        "cohort": "2025-10-13/2025-10-19",
        "avg_prompts_per_active_day": 0.0
      },
      {
        "cohort": "2025-10-20/2025-10-26",
        "avg_prompts_per_active_day": 7.95
      },
      {
        "cohort": "2025-10-27/2025-11-02",
        "avg_prompts_per_active_day": 32.6
      },
      {
        "cohort": "2025-11-03/2025-11-09",
        "avg_prompts_per_active_day": 13.94
      },
      {
        "cohort": "2025-11-17/2025-11-23",
        "avg_prompts_per_active_day": 0.0
      },
      {
        "cohort": "2025-12-01/2025-12-07",
        "avg_prompts_per_active_day": 8.4
      },
      {
        "cohort": "2025-12-08/2025-12-14",
        "avg_prompts_per_active_day": 0.0
      },
      {
        "cohort": "2025-12-15/2025-12-21",
        "avg_prompts_per_active_day": 0.0
      },
      {
        "cohort": "2025-12-22/2025-12-28",
        "avg_prompts_per_active_day": 3.19
      },
      {
        "cohort": "2025-12-29/2026-01-04",
        "avg_prompts_per_active_day": 8.17
      },
      {
        "cohort": "2026-01-05/2026-01-11",
        "avg_prompts_per_active_day": 9.24
      },
      {
        "cohort": "2026-01-12/2026-01-18",
        "avg_prompts_per_active_day": 6.11
      },
      {
        "cohort": "2026-01-19/2026-01-25",
        "avg_prompts_per_active_day": 3.11
      },
      {
        "cohort": "2026-01-26/2026-02-01",
        "avg_prompts_per_active_day": 5.26
      },
      {
        "cohort": "2026-02-02/2026-02-08",
        "avg_prompts_per_active_day": 9.62
      },
      {
        "cohort": "2026-02-09/2026-02-15",
        "avg_prompts_per_active_day": 3.29
      },
      {
        "cohort": "2026-02-16/2026-02-22",
        "avg_prompts_per_active_day": 3.08
      },
      {
        "cohort": "2026-02-23/2026-03-01",
        "avg_prompts_per_active_day": 0.25
      },
      {
        "cohort": "2026-03-02/2026-03-08",
        "avg_prompts_per_active_day": 3.11
      },
      {
        "cohort": "2026-03-09/2026-03-15",
        "avg_prompts_per_active_day": 3.67
      },
      {
        "cohort": "2026-03-16/2026-03-22",
        "avg_prompts_per_active_day": 5.0
      },
      {
        "cohort": "2026-03-23/2026-03-29",
        "avg_prompts_per_active_day": 8.26
      },
      {
        "cohort": "2026-03-30/2026-04-05",
        "avg_prompts_per_active_day": 2.11
      },
      {
        "cohort": "2026-04-06/2026-04-12",
        "avg_prompts_per_active_day": 17.17
      },
      {
        "cohort": "2026-04-13/2026-04-19",
        "avg_prompts_per_active_day": 3.29
      },
      {
        "cohort": "2026-04-20/2026-04-26",
        "avg_prompts_per_active_day": 1.0
      },
      {
        "cohort": "2026-04-27/2026-05-03",
        "avg_prompts_per_active_day": 0.0
      },
      {
        "cohort": "2026-05-11/2026-05-17",
        "avg_prompts_per_active_day": 2.5
      },
      {
        "cohort": "2026-05-18/2026-05-24",
        "avg_prompts_per_active_day": 3.0
      },
      {
        "cohort": "2026-05-25/2026-05-31",
        "avg_prompts_per_active_day": 0.0
      }
    ],
    "power_users_day0_pct": 6.6,
    "power_users_week0_pct": 13.1,
    "multi_day_ai_first_7d_pct": 12.3
  },
  "retention": {
    "overall_retention_pct": {
      "D1": 10.7,
      "D3": 4.1,
      "D7": 11.9,
      "D14": 4.4,
      "D30": 2.7
    },
    "cohort_retention": [
      {
        "cohort": "2025-08-18/2025-08-24",
        "D1": 50.0,
        "D3": 0.0,
        "D7": 0.0,
        "D14": 0.0,
        "D30": 0.0
      },
      {
        "cohort": "2025-10-13/2025-10-19",
        "D1": 0.0,
        "D3": 0.0,
        "D7": 0.0,
        "D14": 0.0,
        "D30": 0.0
      },
      {
        "cohort": "2025-10-20/2025-10-26",
        "D1": 66.7,
        "D3": 33.3,
        "D7": 33.3,
        "D14": 0.0,
        "D30": 0.0
      },
      {
        "cohort": "2025-10-27/2025-11-02",
        "D1": 100.0,
        "D3": 0.0,
        "D7": 0.0,
        "D14": 0.0,
        "D30": 0.0
      },
      {
        "cohort": "2025-11-03/2025-11-09",
        "D1": 0.0,
        "D3": 0.0,
        "D7": 0.0,
        "D14": 0.0,
        "D30": 0.0
      },
      {
        "cohort": "2025-11-17/2025-11-23",
        "D1": 0.0,
        "D3": 0.0,
        "D7": 0.0,
        "D14": 0.0,
        "D30": 0.0
      },
      {
        "cohort": "2025-12-01/2025-12-07",
        "D1": 0.0,
        "D3": 0.0,
        "D7": 0.0,
        "D14": 0.0,
        "D30": 0.0
      },
      {
        "cohort": "2025-12-08/2025-12-14",
        "D1": 0.0,
        "D3": 0.0,
        "D7": 0.0,
        "D14": 0.0,
        "D30": 0.0
      },
      {
        "cohort": "2025-12-15/2025-12-21",
        "D1": 0.0,
        "D3": 0.0,
        "D7": 0.0,
        "D14": 0.0,
        "D30": 0.0
      },
      {
        "cohort": "2025-12-22/2025-12-28",
        "D1": 0.0,
        "D3": 0.0,
        "D7": 0.0,
        "D14": 0.0,
        "D30": 0.0
      },
      {
        "cohort": "2025-12-29/2026-01-04",
        "D1": 0.0,
        "D3": 0.0,
        "D7": 0.0,
        "D14": 0.0,
        "D30": 0.0
      },
      {
        "cohort": "2026-01-05/2026-01-11",
        "D1": 0.0,
        "D3": 0.0,
        "D7": 25.0,
        "D14": 0.0,
        "D30": 0.0
      },
      {
        "cohort": "2026-01-12/2026-01-18",
        "D1": 0.0,
        "D3": 0.0,
        "D7": 22.2,
        "D14": 0.0,
        "D30": 22.2
      },
      {
        "cohort": "2026-01-19/2026-01-25",
        "D1": 25.0,
        "D3": 0.0,
        "D7": 12.5,
        "D14": 12.5,
        "D30": 0.0
      },
      {
        "cohort": "2026-01-26/2026-02-01",
        "D1": 0.0,
        "D3": 0.0,
        "D7": 33.3,
        "D14": 0.0,
        "D30": 0.0
      },
      {
        "cohort": "2026-02-02/2026-02-08",
        "D1": 16.7,
        "D3": 16.7,
        "D7": 33.3,
        "D14": 16.7,
        "D30": 0.0
      },
      {
        "cohort": "2026-02-09/2026-02-15",
        "D1": 0.0,
        "D3": 9.1,
        "D7": 18.2,
        "D14": 9.1,
        "D30": 0.0
      },
      {
        "cohort": "2026-02-16/2026-02-22",
        "D1": 0.0,
        "D3": 20.0,
        "D7": 0.0,
        "D14": 0.0,
        "D30": 0.0
      },
      {
        "cohort": "2026-02-23/2026-03-01",
        "D1": 0.0,
        "D3": 0.0,
        "D7": 0.0,
        "D14": 0.0,
        "D30": 0.0
      },
      {
        "cohort": "2026-03-02/2026-03-08",
        "D1": 0.0,
        "D3": 0.0,
        "D7": 14.3,
        "D14": 0.0,
        "D30": 0.0
      },
      {
        "cohort": "2026-03-09/2026-03-15",
        "D1": 0.0,
        "D3": 0.0,
        "D7": 33.3,
        "D14": 0.0,
        "D30": 0.0
      },
      {
        "cohort": "2026-03-16/2026-03-22",
        "D1": 50.0,
        "D3": 0.0,
        "D7": 0.0,
        "D14": 0.0,
        "D30": 50.0
      },
      {
        "cohort": "2026-03-23/2026-03-29",
        "D1": 33.3,
        "D3": 0.0,
        "D7": 0.0,
        "D14": 33.3,
        "D30": 0.0
      },
      {
        "cohort": "2026-03-30/2026-04-05",
        "D1": 0.0,
        "D3": 0.0,
        "D7": 0.0,
        "D14": 50.0,
        "D30": 0.0
      },
      {
        "cohort": "2026-04-06/2026-04-12",
        "D1": 33.3,
        "D3": 0.0,
        "D7": 33.3,
        "D14": 0.0,
        "D30": 0.0
      },
      {
        "cohort": "2026-04-13/2026-04-19",
        "D1": 7.7,
        "D3": 0.0,
        "D7": 0.0,
        "D14": 0.0,
        "D30": 0.0
      },
      {
        "cohort": "2026-04-20/2026-04-26",
        "D1": 0.0,
        "D3": 0.0,
        "D7": 0.0,
        "D14": 0.0,
        "D30": 0.0
      },
      {
        "cohort": "2026-04-27/2026-05-03",
        "D1": 0.0,
        "D3": 0.0,
        "D7": 0.0,
        "D14": 0.0,
        "D30": null
      },
      {
        "cohort": "2026-05-11/2026-05-17",
        "D1": 20.0,
        "D3": 20.0,
        "D7": 20.0,
        "D14": null,
        "D30": null
      },
      {
        "cohort": "2026-05-18/2026-05-24",
        "D1": 33.3,
        "D3": 0.0,
        "D7": null,
        "D14": null,
        "D30": null
      },
      {
        "cohort": "2026-05-25/2026-05-31",
        "D1": null,
        "D3": null,
        "D7": null,
        "D14": null,
        "D30": null
      }
    ],
    "wau_by_week": [
      {
        "week": "2026-03-09/2026-03-15",
        "week_start": "2026-03-09",
        "wau": 7,
        "wow_pct": null
      },
      {
        "week": "2026-03-16/2026-03-22",
        "week_start": "2026-03-16",
        "wau": 7,
        "wow_pct": 0.0
      },
      {
        "week": "2026-03-23/2026-03-29",
        "week_start": "2026-03-23",
        "wau": 7,
        "wow_pct": 0.0
      },
      {
        "week": "2026-03-30/2026-04-05",
        "week_start": "2026-03-30",
        "wau": 4,
        "wow_pct": -42.9
      },
      {
        "week": "2026-04-06/2026-04-12",
        "week_start": "2026-04-06",
        "wau": 4,
        "wow_pct": 0.0
      },
      {
        "week": "2026-04-13/2026-04-19",
        "week_start": "2026-04-13",
        "wau": 17,
        "wow_pct": 325.0
      },
      {
        "week": "2026-04-20/2026-04-26",
        "week_start": "2026-04-20",
        "wau": 14,
        "wow_pct": -17.6
      },
      {
        "week": "2026-04-27/2026-05-03",
        "week_start": "2026-04-27",
        "wau": 7,
        "wow_pct": -50.0
      },
      {
        "week": "2026-05-04/2026-05-10",
        "week_start": "2026-05-04",
        "wau": 9,
        "wow_pct": 28.6
      },
      {
        "week": "2026-05-11/2026-05-17",
        "week_start": "2026-05-11",
        "wau": 15,
        "wow_pct": 66.7
      },
      {
        "week": "2026-05-18/2026-05-24",
        "week_start": "2026-05-18",
        "wau": 17,
        "wow_pct": 13.3
      },
      {
        "week": "2026-05-25/2026-05-31",
        "week_start": "2026-05-25",
        "wau": 2,
        "wow_pct": -88.2
      }
    ],
    "churn_pct": {
      "churn_7d_pct": 76.4,
      "churn_14d_pct": 70.8,
      "churn_30d_pct": 63.9
    },
    "session_frequency_by_week": [
      {
        "week": "2025-10-27/2025-11-02",
        "sessions_per_active_user": 67.0
      },
      {
        "week": "2026-04-13/2026-04-19",
        "sessions_per_active_user": 20.47
      },
      {
        "week": "2026-04-20/2026-04-26",
        "sessions_per_active_user": 15.21
      },
      {
        "week": "2026-04-27/2026-05-03",
        "sessions_per_active_user": 10.0
      },
      {
        "week": "2026-05-04/2026-05-10",
        "sessions_per_active_user": 31.56
      },
      {
        "week": "2026-05-11/2026-05-17",
        "sessions_per_active_user": 16.2
      },
      {
        "week": "2026-05-18/2026-05-24",
        "sessions_per_active_user": 10.24
      },
      {
        "week": "2026-05-25/2026-05-31",
        "sessions_per_active_user": 4.0
      }
    ]
  },
  "monetization": {
    "token_limit_hit_rate_pct": 4.5,
    "users_hit_limit": 1,
    "limit_hit_days": 2,
    "limit_hits_by_lifecycle_day": [
      {
        "lifecycle_day": 114,
        "hit_count": 1
      },
      {
        "lifecycle_day": 122,
        "hit_count": 1
      }
    ],
    "median_days_to_first_limit": 118,
    "median_hours_to_first_limit": 2832.0,
    "premium_conversion_among_limit_hitters_pct": 0.0,
    "premium_conversion_pct": 0.8,
    "premium_users": 1,
    "paid_subscribers": 1,
    "active_paid_subscribers": 0,
    "cancelled_paid_subscribers": 0,
    "conversion_velocity_hours": {
      "median": null,
      "mean": null
    },
    "arpu_gross_usd": 1.02,
    "arpu_net_usd": 1.01,
    "total_revenue_usd": 124.0,
    "estimated_api_cost_usd": 0.38,
    "gross_margin_pct": 79.5,
    "ltv_proxy_usd": 12.12,
    "cac_ltv": {
      "cac_available": false,
      "ltv_proxy_usd": 12.12,
      "note": "user_acquisition and events tables empty \u2014 provide marketing spend externally"
    }
  },
  "feedback": {
    "submission_rate_pct": 23.8,
    "median_hours_to_first": 672.29,
    "distribution": [
      {
        "bucket": "0",
        "users": 93
      },
      {
        "bucket": "1",
        "users": 6
      },
      {
        "bucket": "2-5",
        "users": 12
      },
      {
        "bucket": "6-10",
        "users": 5
      },
      {
        "bucket": "10+",
        "users": 6
      }
    ],
    "anomalies": [
      {
        "user_id": "b3eaaa88-1c97-426c-819e-1e3d8dcb4ed0",
        "minutes_after_signup": 2.1
      },
      {
        "user_id": "38412c06-264d-4e0d-bd94-9db9bfb042b5",
        "minutes_after_signup": 7.6
      },
      {
        "user_id": "8845c0f5-da2b-4fcc-bc46-d674f4a1d9e3",
        "minutes_after_signup": 7.2
      },
      {
        "user_id": "91f195ba-eeee-46d9-9f80-56e68ef2b2a7",
        "minutes_after_signup": 2.1
      },
      {
        "user_id": "d24f0dda-8911-4fad-84c3-2a4d95d35fe0",
        "minutes_after_signup": 12.7
      },
      {
        "user_id": "e2c6f468-355e-4800-b866-4467999b65c7",
        "minutes_after_signup": 5.1
      }
    ],
    "review_samples": [
      {
        "feedback_id": "818f8fdd-866a-432e-aaec-08f969d0a22d",
        "category": "Suggestion",
        "negative_rating": true,
        "reported_at": "2026-02-04 21:50:36.342000",
        "tag": "fast_submitter"
      },
      {
        "feedback_id": "60d1349b-c2a4-430d-8931-6e2f7e491aa3",
        "category": "Helpful",
        "negative_rating": false,
        "reported_at": "2026-02-04 22:03:47.009000",
        "tag": "fast_submitter"
      },
      {
        "feedback_id": "1d542756-9017-49ab-840d-fc50452c4567",
        "category": "Helpful",
        "negative_rating": false,
        "reported_at": "2026-02-04 22:04:01.580000",
        "tag": "fast_submitter"
      },
      {
        "feedback_id": "b7885727-9971-4fcd-9a80-4164d64d1b94",
        "category": "Clear",
        "negative_rating": false,
        "reported_at": "2026-01-26 07:19:49.458000",
        "tag": "by_category"
      },
      {
        "feedback_id": "45ac589e-8896-4ee8-960a-e3eef9b53428",
        "category": "Not helpful",
        "negative_rating": true,
        "reported_at": "2026-01-26 07:21:16.192000",
        "tag": "by_category"
      },
      {
        "feedback_id": "655bec61-5d30-461c-b339-b4eec86f3511",
        "category": "Accurate",
        "negative_rating": false,
        "reported_at": "2026-01-28 16:11:16.330000",
        "tag": "by_category"
      },
      {
        "feedback_id": "b4b1ae3d-8bdb-476f-bb6d-069f2e375105",
        "category": "Incorrect",
        "negative_rating": true,
        "reported_at": "2026-01-28 19:04:17.933000",
        "tag": "by_category"
      },
      {
        "feedback_id": "50f765b3-209d-48a7-8cad-7518e78ec274",
        "category": "Other",
        "negative_rating": true,
        "reported_at": "2026-01-28 23:19:11.284000",
        "tag": "by_category"
      }
    ]
  },
  "dau_model": {
    "as_of": "2026-05-25",
    "bucket_counts": {
      "new": 0,
      "current": 1,
      "reactivated": 1,
      "resurrected": 0,
      "at_risk_wau": 12,
      "at_risk_mau": 12,
      "dead": 96
    },
    "bucket_rows": [
      {
        "bucket": "New users",
        "key": "new",
        "users": 0,
        "pct_of_total": 0.0
      },
      {
        "bucket": "Current users",
        "key": "current",
        "users": 1,
        "pct_of_total": 0.8
      },
      {
        "bucket": "Reactivated users",
        "key": "reactivated",
        "users": 1,
        "pct_of_total": 0.8
      },
      {
        "bucket": "Resurrected users",
        "key": "resurrected",
        "users": 0,
        "pct_of_total": 0.0
      },
      {
        "bucket": "At-risk WAU",
        "key": "at_risk_wau",
        "users": 12,
        "pct_of_total": 9.8
      },
      {
        "bucket": "At-risk MAU",
        "key": "at_risk_mau",
        "users": 12,
        "pct_of_total": 9.8
      },
      {
        "bucket": "Dead users",
        "key": "dead",
        "users": 96,
        "pct_of_total": 78.7
      }
    ],
    "totals": {
      "dau": 2,
      "wau": 14,
      "mau": 26,
      "total_users": 122
    },
    "flow_rates_pct": {
      "NURR": 50.0,
      "1-NURR": 50.0,
      "CURR": 36.5,
      "1-CURR": 63.5,
      "RURR": 0.0,
      "1-RURR": 100.0,
      "SURR": 0.0,
      "1-SURR": 100.0,
      "iWAURR": 13.4,
      "WAU_Loss_Rate": 8.8,
      "iMAURR": 1.3,
      "MAU_Loss_Rate": 7.0,
      "Resurrection_Rate": 0.1
    },
    "flow_rate_rows": [
      {
        "rate": "NURR",
        "transition": "New \u2192 Current",
        "pct": 50.0
      },
      {
        "rate": "1-NURR",
        "transition": "New \u2192 At-risk WAU",
        "pct": 50.0
      },
      {
        "rate": "CURR",
        "transition": "Current \u2192 Current",
        "pct": 36.5
      },
      {
        "rate": "1-CURR",
        "transition": "Current \u2192 At-risk WAU",
        "pct": 63.5
      },
      {
        "rate": "RURR",
        "transition": "Reactivated \u2192 Current",
        "pct": 0.0
      },
      {
        "rate": "1-RURR",
        "transition": "Reactivated \u2192 At-risk WAU",
        "pct": 100.0
      },
      {
        "rate": "SURR",
        "transition": "Resurrected \u2192 Current",
        "pct": 0.0
      },
      {
        "rate": "1-SURR",
        "transition": "Resurrected \u2192 At-risk WAU",
        "pct": 100.0
      },
      {
        "rate": "iWAURR",
        "transition": "At-risk WAU \u2192 Current",
        "pct": 13.4
      },
      {
        "rate": "WAU_Loss_Rate",
        "transition": "At-risk WAU \u2192 At-risk MAU",
        "pct": 8.8
      },
      {
        "rate": "iMAURR",
        "transition": "At-risk MAU \u2192 Reactivated",
        "pct": 1.3
      },
      {
        "rate": "MAU_Loss_Rate",
        "transition": "At-risk MAU \u2192 Dead",
        "pct": 7.0
      },
      {
        "rate": "Resurrection_Rate",
        "transition": "Dead \u2192 Resurrected",
        "pct": 0.1
      }
    ],
    "flow_window_days": 7,
    "definitions": {
      "new": "First day of engagement ever",
      "current": "Active today and at least one other day in the prior 7 days",
      "reactivated": "First day back after 7\u201329 days away",
      "resurrected": "First day back after 30+ days away",
      "at_risk_wau": "Inactive today, active on at least one of the prior 6 days",
      "at_risk_mau": "Inactive today and prior 6 days, active 7\u201329 days ago",
      "dead": "No activity in the last 30 days"
    }
  },
  "launch_kpis": {
    "kpi_rows": [
      {
        "category": "Activation",
        "metric": "AI activation rate (1h)",
        "value": "27.0%",
        "status": "live",
        "metric_key": "activation_24h_pct",
        "tooltip": "What it means: Share of all users who sent their first AI prompt within 24 hours of signing up. Higher means onboarding is working quickly.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Context: 176 on waitlist. Product Hunt launch may add 200\u20132000 signups in ~2 days \u2014 activation and conversion drive the 500 subscriber goal by Dec 31. Goal: 500 paid subscribers by Dec 31, 2026; May 2026 target: 17 (behind pace). You have 1 (0.2% of year-end goal). Gap to year-end: 499 subscribers."
      },
      {
        "category": "Activation",
        "metric": "AI activation rate (24h)",
        "value": "31.1%",
        "status": "live",
        "metric_key": "activation_24h_pct",
        "tooltip": "What it means: Share of all users who sent their first AI prompt within 24 hours of signing up. Higher means onboarding is working quickly.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Context: 176 on waitlist. Product Hunt launch may add 200\u20132000 signups in ~2 days \u2014 activation and conversion drive the 500 subscriber goal by Dec 31. Goal: 500 paid subscribers by Dec 31, 2026; May 2026 target: 17 (behind pace). You have 1 (0.2% of year-end goal). Gap to year-end: 499 subscribers."
      },
      {
        "category": "Activation",
        "metric": "AI activation rate (3d)",
        "value": "32.8%",
        "status": "live",
        "metric_key": "activation_24h_pct",
        "tooltip": "What it means: Share of all users who sent their first AI prompt within 24 hours of signing up. Higher means onboarding is working quickly.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Context: 176 on waitlist. Product Hunt launch may add 200\u20132000 signups in ~2 days \u2014 activation and conversion drive the 500 subscriber goal by Dec 31. Goal: 500 paid subscribers by Dec 31, 2026; May 2026 target: 17 (behind pace). You have 1 (0.2% of year-end goal). Gap to year-end: 499 subscribers."
      },
      {
        "category": "Activation",
        "metric": "AI activation rate (7d)",
        "value": "37.7%",
        "status": "live",
        "metric_key": "activation_24h_pct",
        "tooltip": "What it means: Share of all users who sent their first AI prompt within 24 hours of signing up. Higher means onboarding is working quickly.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Context: 176 on waitlist. Product Hunt launch may add 200\u20132000 signups in ~2 days \u2014 activation and conversion drive the 500 subscriber goal by Dec 31. Goal: 500 paid subscribers by Dec 31, 2026; May 2026 target: 17 (behind pace). You have 1 (0.2% of year-end goal). Gap to year-end: 499 subscribers."
      },
      {
        "category": "Activation",
        "metric": "Time to first AI command (median h)",
        "value": "5.54 h",
        "status": "live",
        "tooltip": "Median hours from account creation to first AI prompt."
      },
      {
        "category": "Activation",
        "metric": "Time to first AI command (mean h)",
        "value": "421.82 h",
        "status": "live",
        "tooltip": "Median hours from account creation to first AI prompt."
      },
      {
        "category": "Engagement",
        "metric": "Power users \u2014 10+ prompts day 0",
        "value": "6.6%",
        "status": "live",
        "tooltip": "Engagement metric tracked for Product Hunt launch. See section charts below for trend detail."
      },
      {
        "category": "Engagement",
        "metric": "Power users \u2014 10+ prompts week 0",
        "value": "13.1%",
        "status": "live",
        "tooltip": "Engagement metric tracked for Product Hunt launch. See section charts below for trend detail."
      },
      {
        "category": "Engagement",
        "metric": "Multi-day AI in first 7 days",
        "value": "12.3%",
        "status": "live",
        "tooltip": "Engagement metric tracked for Product Hunt launch. See section charts below for trend detail."
      },
      {
        "category": "Engagement",
        "metric": "Avg prompts / active day (latest cohort)",
        "value": "0.0",
        "status": "live",
        "tooltip": "Engagement metric tracked for Product Hunt launch. See section charts below for trend detail."
      },
      {
        "category": "Retention",
        "metric": "D1 retention",
        "value": "10.7%",
        "status": "live",
        "metric_key": "retention_d7_pct",
        "tooltip": "What it means: Share of users who came back on day 7 after signup (session or AI usage). A leading indicator of whether new users stick.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Context: 176 on waitlist. Product Hunt launch may add 200\u20132000 signups in ~2 days \u2014 activation and conversion drive the 500 subscriber goal by Dec 31. Goal: 500 paid subscribers by Dec 31, 2026; May 2026 target: 17 (behind pace). You have 1 (0.2% of year-end goal). Gap to year-end: 499 subscribers."
      },
      {
        "category": "Retention",
        "metric": "D3 retention",
        "value": "4.1%",
        "status": "live",
        "tooltip": "Retention metric tracked for Product Hunt launch. See section charts below for trend detail."
      },
      {
        "category": "Retention",
        "metric": "D7 retention",
        "value": "11.9%",
        "status": "live",
        "metric_key": "retention_d7_pct",
        "tooltip": "What it means: Share of users who came back on day 7 after signup (session or AI usage). A leading indicator of whether new users stick.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Context: 176 on waitlist. Product Hunt launch may add 200\u20132000 signups in ~2 days \u2014 activation and conversion drive the 500 subscriber goal by Dec 31. Goal: 500 paid subscribers by Dec 31, 2026; May 2026 target: 17 (behind pace). You have 1 (0.2% of year-end goal). Gap to year-end: 499 subscribers."
      },
      {
        "category": "Retention",
        "metric": "D14 retention",
        "value": "4.4%",
        "status": "live",
        "tooltip": "Retention metric tracked for Product Hunt launch. See section charts below for trend detail."
      },
      {
        "category": "Retention",
        "metric": "D30 retention",
        "value": "2.7%",
        "status": "live",
        "tooltip": "Retention metric tracked for Product Hunt launch. See section charts below for trend detail."
      },
      {
        "category": "Retention",
        "metric": "Latest WAU",
        "value": "2 (-88.2% WoW)",
        "status": "live",
        "tooltip": "Retention metric tracked for Product Hunt launch. See section charts below for trend detail."
      },
      {
        "category": "Retention",
        "metric": "Churn 7d (ever-active)",
        "value": "76.4%",
        "status": "live",
        "metric_key": "churn_7d_pct",
        "tooltip": "What it means: Among users who were ever active, the share with no return in the last 7 days. Lower is better \u2014 rising churn means more slipping away.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx. Lower churn protects DAU and path to 500 subscribers."
      },
      {
        "category": "Retention",
        "metric": "Churn 14d (ever-active)",
        "value": "70.8%",
        "status": "live",
        "metric_key": "churn_14d_pct",
        "tooltip": "What it means: Ever-active users with no activity in the last 14 days.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx. Lower churn protects DAU and path to 500 subscribers."
      },
      {
        "category": "Retention",
        "metric": "Churn 30d (ever-active)",
        "value": "63.9%",
        "status": "live",
        "metric_key": "churn_30d_pct",
        "tooltip": "What it means: Ever-active users with no activity in the last 30 days.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx. Lower churn protects DAU and path to 500 subscribers."
      },
      {
        "category": "Retention",
        "metric": "Sessions / active user (latest week)",
        "value": "4.0",
        "status": "live",
        "tooltip": "Retention metric tracked for Product Hunt launch. See section charts below for trend detail."
      },
      {
        "category": "Monetization",
        "metric": "Token limit hit rate",
        "value": "4.5%",
        "status": "live",
        "metric_key": "token_limit_hit_rate_pct",
        "tooltip": "What it means: Share of users who hit the daily AI token cap at least once. Often signals power users who may upgrade.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 80.0% gross margin. Current: 79.5% (below target). Gap: 0.5 pp to target. Goal: 500 paid subscribers by Dec 31, 2026; May 2026 target: 17 (behind pace). You have 1 (0.2% of year-end goal). Gap to year-end: 499 subscribers."
      },
      {
        "category": "Monetization",
        "metric": "Median days to first token limit",
        "value": "118 d",
        "status": "live",
        "metric_key": "median_days_to_first_limit",
        "tooltip": "What it means: Typical days from signup until a user first hits the token cap. Shorter often means heavy early usage.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Context: 176 on waitlist. Product Hunt launch may add 200\u20132000 signups in ~2 days \u2014 activation and conversion drive the 500 subscriber goal by Dec 31."
      },
      {
        "category": "Monetization",
        "metric": "Median hours to first token limit",
        "value": "2832.0 h",
        "status": "live",
        "tooltip": "Monetization metric tracked for Product Hunt launch. See section charts below for trend detail."
      },
      {
        "category": "Monetization",
        "metric": "Paid subscribers ($20/mo)",
        "value": "1",
        "status": "live",
        "tooltip": "Monetization metric tracked for Product Hunt launch. See section charts below for trend detail."
      },
      {
        "category": "Monetization",
        "metric": "Premium conversion (all users)",
        "value": "0.8%",
        "status": "live",
        "metric_key": "premium_conversion_pct",
        "tooltip": "What it means: Share of all users counted as paid subscribers ($20/mo Stripe plans). Count = baseline 1 plus distinct user_plans from May 24, 2026 onward.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 500 paid subscribers by Dec 31, 2026; May 2026 target: 17 (behind pace). You have 1 (0.2% of year-end goal). Gap to year-end: 499 subscribers."
      },
      {
        "category": "Monetization",
        "metric": "Premium conversion (limit hitters)",
        "value": "0.0%",
        "status": "live",
        "metric_key": "limit_hitter_conversion_pct",
        "tooltip": "What it means: Of users who hit token limits, how many are on a paid plan. Measures whether limits drive upgrades.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 500 paid subscribers by Dec 31, 2026; May 2026 target: 17 (behind pace). You have 1 (0.2% of year-end goal). Gap to year-end: 499 subscribers."
      },
      {
        "category": "Monetization",
        "metric": "Conversion velocity (median h to upgrade)",
        "value": "\u2014",
        "status": "live",
        "tooltip": "Median hours from signup to first premium upgrade among paying users."
      },
      {
        "category": "Monetization",
        "metric": "ARPU gross",
        "value": "$1.02",
        "status": "live",
        "tooltip": "Monetization metric tracked for Product Hunt launch. See section charts below for trend detail."
      },
      {
        "category": "Monetization",
        "metric": "ARPU net (est. API cost)",
        "value": "$1.01",
        "status": "live",
        "metric_key": "arpu_net_usd",
        "tooltip": "Average revenue per user after subtracting estimated API costs. Net unit economics per user."
      },
      {
        "category": "Monetization",
        "metric": "Est. API cost (all-time model)",
        "value": "$0.38",
        "status": "live",
        "tooltip": "Monetization metric tracked for Product Hunt launch. See section charts below for trend detail."
      },
      {
        "category": "Monetization",
        "metric": "Projected monthly API cost (7d run-rate)",
        "value": "$0.3",
        "status": "live",
        "tooltip": "Monetization metric tracked for Product Hunt launch. See section charts below for trend detail."
      },
      {
        "category": "Monetization",
        "metric": "LTV proxy (12 mo, net ARPU)",
        "value": "$12.12",
        "status": "live",
        "tooltip": "Monetization metric tracked for Product Hunt launch. See section charts below for trend detail."
      },
      {
        "category": "Monetization",
        "metric": "CAC / LTV ratio",
        "value": "Unavailable \u2014 no acquisition spend in DB",
        "status": "partial",
        "tooltip": "Monetization metric tracked for Product Hunt launch. See section charts below for trend detail."
      },
      {
        "category": "Monetization",
        "metric": "Actual Gemini spend (monthly)",
        "value": "Enter in dashboard \u2014 AI Studio actuals",
        "status": "manual",
        "tooltip": "Monetization metric tracked for Product Hunt launch. See section charts below for trend detail."
      },
      {
        "category": "Feedback",
        "metric": "Feedback submission rate",
        "value": "23.8%",
        "status": "live",
        "metric_key": "feedback_submission_rate_pct",
        "tooltip": "What it means: Share of users who submitted at least one feedback/training event. Signals product involvement beyond passive use.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Context: 176 on waitlist. Product Hunt launch may add 200\u20132000 signups in ~2 days \u2014 activation and conversion drive the 500 subscriber goal by Dec 31."
      },
      {
        "category": "Feedback",
        "metric": "Median hours to first feedback",
        "value": "672.29 h",
        "status": "live",
        "tooltip": "Feedback metric tracked for Product Hunt launch. See section charts below for trend detail."
      },
      {
        "category": "Feedback",
        "metric": "Anomalies (<15 min post-signup)",
        "value": "6",
        "status": "live",
        "tooltip": "Feedback metric tracked for Product Hunt launch. See section charts below for trend detail."
      },
      {
        "category": "Feedback",
        "metric": "Manual review samples",
        "value": "8",
        "status": "live",
        "tooltip": "Feedback metric tracked for Product Hunt launch. See section charts below for trend detail."
      },
      {
        "category": "DAU",
        "metric": "DAU (today)",
        "value": "2",
        "status": "live",
        "metric_key": "dau",
        "tooltip": "What it means: Users engaged today: new, current, reactivated, or resurrected.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx."
      },
      {
        "category": "DAU",
        "metric": "WAU (model)",
        "value": "14",
        "status": "live",
        "metric_key": "wau",
        "tooltip": "What it means: DAU plus users at-risk WAU (active recently but not today).\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx."
      },
      {
        "category": "DAU",
        "metric": "MAU (model)",
        "value": "26",
        "status": "live",
        "metric_key": "mau",
        "tooltip": "What it means: WAU plus users at-risk MAU (active 7\u201329 days ago, inactive lately).\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx."
      },
      {
        "category": "Lifecycle readiness",
        "metric": "New users \u2014 first AI prompt",
        "value": "\u2014",
        "status": "live",
        "tooltip": "Lifecycle readiness metric tracked for Product Hunt launch. See section charts below for trend detail."
      },
      {
        "category": "Lifecycle readiness",
        "metric": "New users \u2014 AI assistant trained",
        "value": "\u2014",
        "status": "live",
        "tooltip": "Lifecycle readiness metric tracked for Product Hunt launch. See section charts below for trend detail."
      },
      {
        "category": "Lifecycle readiness",
        "metric": "All users \u2014 \u22651 product milestone",
        "value": "58.2%",
        "status": "live",
        "tooltip": "Lifecycle readiness metric tracked for Product Hunt launch. See section charts below for trend detail."
      }
    ],
    "headlines": {
      "activation_24h_pct": 31.1,
      "retention_d7_pct": 11.9,
      "latest_wau": 2,
      "premium_conversion_pct": 0.8,
      "feedback_submission_rate_pct": 23.8,
      "arpu_net_usd": 1.01
    },
    "usage_cost_forecast": {
      "window_days": 7,
      "window_start": "2026-05-19",
      "window_end": "2026-05-25",
      "prompts_last_7d": 373,
      "estimated_cost_last_7d_usd": 0.07,
      "projected_monthly_prompts": 1599,
      "projected_monthly_cost_usd": 0.3
    },
    "premium_conversion_among_limit_hitters_pct": 0.0,
    "default_supabase_monthly_usd": 25
  },
  "deltas": {
    "daily": {
      "available": true,
      "as_of": "2026-05-24",
      "label": "vs 1d ago",
      "metrics": {
        "total_users": {
          "current": 122.0,
          "prior": 122.0,
          "abs_change": 0.0,
          "pct_change": 0.0,
          "direction": "flat",
          "significant": false
        },
        "active_users": {
          "current": 122.0,
          "prior": 122.0,
          "abs_change": 0.0,
          "pct_change": 0.0,
          "direction": "flat",
          "significant": false
        },
        "activation_24h_pct": {
          "current": 31.1,
          "prior": 32.0,
          "abs_change": -0.9,
          "pct_change": -2.8,
          "direction": "down",
          "significant": false
        },
        "retention_d7_pct": {
          "current": 11.9,
          "prior": 11.8,
          "abs_change": 0.1,
          "pct_change": 0.8,
          "direction": "up",
          "significant": false
        },
        "latest_wau": {
          "current": 2.0,
          "prior": 17.0,
          "abs_change": -15.0,
          "pct_change": -88.2,
          "direction": "down",
          "significant": true
        },
        "premium_conversion_pct": {
          "current": 0.8,
          "prior": 0.8,
          "abs_change": 0.0,
          "pct_change": 0.0,
          "direction": "flat",
          "significant": false
        },
        "feedback_submission_rate_pct": {
          "current": 23.8,
          "prior": 24.6,
          "abs_change": -0.8,
          "pct_change": -3.3,
          "direction": "down",
          "significant": false
        },
        "arpu_net_usd": {
          "current": 1.01,
          "prior": 1.34,
          "abs_change": -0.33,
          "pct_change": -24.6,
          "direction": "down",
          "significant": true
        },
        "churn_7d_pct": {
          "current": 76.4,
          "prior": 75.3,
          "abs_change": 1.1,
          "pct_change": 1.5,
          "direction": "up",
          "significant": false
        },
        "churn_14d_pct": {
          "current": 70.8,
          "prior": 71.2,
          "abs_change": -0.4,
          "pct_change": -0.6,
          "direction": "down",
          "significant": false
        },
        "churn_30d_pct": {
          "current": 63.9,
          "prior": 61.6,
          "abs_change": 2.3,
          "pct_change": 3.7,
          "direction": "up",
          "significant": false
        },
        "dau": {
          "current": 2.0,
          "prior": 2.0,
          "abs_change": 0.0,
          "pct_change": 0.0,
          "direction": "flat",
          "significant": false
        },
        "wau": {
          "current": 14.0,
          "prior": 17.0,
          "abs_change": -3.0,
          "pct_change": -17.6,
          "direction": "down",
          "significant": true
        },
        "mau": {
          "current": 26.0,
          "prior": 27.0,
          "abs_change": -1.0,
          "pct_change": -3.7,
          "direction": "down",
          "significant": false
        },
        "token_limit_hit_rate_pct": {
          "current": 4.5,
          "prior": 4.5,
          "abs_change": 0.0,
          "pct_change": 0.0,
          "direction": "flat",
          "significant": false
        },
        "limit_hitter_conversion_pct": {
          "current": 0.0,
          "prior": 0.0,
          "abs_change": 0.0,
          "pct_change": null,
          "direction": "flat",
          "significant": false
        },
        "median_days_to_first_limit": {
          "current": 118.0,
          "prior": 118.0,
          "abs_change": 0.0,
          "pct_change": 0.0,
          "direction": "flat",
          "significant": false
        },
        "bucket_new": {
          "current": 0.0,
          "prior": 0.0,
          "abs_change": 0.0,
          "pct_change": null,
          "direction": "flat",
          "significant": false
        },
        "bucket_current": {
          "current": 1.0,
          "prior": 1.0,
          "abs_change": 0.0,
          "pct_change": 0.0,
          "direction": "flat",
          "significant": false
        },
        "bucket_reactivated": {
          "current": 1.0,
          "prior": 0.0,
          "abs_change": 1.0,
          "pct_change": null,
          "direction": "up",
          "significant": false
        },
        "bucket_resurrected": {
          "current": 0.0,
          "prior": 1.0,
          "abs_change": -1.0,
          "pct_change": -100.0,
          "direction": "down",
          "significant": true
        },
        "bucket_at_risk_wau": {
          "current": 12.0,
          "prior": 15.0,
          "abs_change": -3.0,
          "pct_change": -20.0,
          "direction": "down",
          "significant": true
        },
        "bucket_at_risk_mau": {
          "current": 12.0,
          "prior": 10.0,
          "abs_change": 2.0,
          "pct_change": 20.0,
          "direction": "up",
          "significant": true
        },
        "bucket_dead": {
          "current": 96.0,
          "prior": 95.0,
          "abs_change": 1.0,
          "pct_change": 1.1,
          "direction": "up",
          "significant": false
        },
        "flow_NURR": {
          "current": 50.0,
          "prior": 50.0,
          "abs_change": 0.0,
          "pct_change": 0.0,
          "direction": "flat",
          "significant": false
        },
        "flow_1-NURR": {
          "current": 50.0,
          "prior": 50.0,
          "abs_change": 0.0,
          "pct_change": 0.0,
          "direction": "flat",
          "significant": false
        },
        "flow_CURR": {
          "current": 36.5,
          "prior": 32.9,
          "abs_change": 3.6,
          "pct_change": 10.9,
          "direction": "up",
          "significant": false
        },
        "flow_1-CURR": {
          "current": 63.5,
          "prior": 67.1,
          "abs_change": -3.6,
          "pct_change": -5.4,
          "direction": "down",
          "significant": false
        },
        "flow_RURR": {
          "current": 0.0,
          "prior": 16.7,
          "abs_change": -16.7,
          "pct_change": -100.0,
          "direction": "down",
          "significant": true
        },
        "flow_1-RURR": {
          "current": 100.0,
          "prior": 83.3,
          "abs_change": 16.7,
          "pct_change": 20.0,
          "direction": "up",
          "significant": true
        },
        "flow_SURR": {
          "current": 0.0,
          "prior": 50.0,
          "abs_change": -50.0,
          "pct_change": -100.0,
          "direction": "down",
          "significant": true
        },
        "flow_1-SURR": {
          "current": 100.0,
          "prior": 50.0,
          "abs_change": 50.0,
          "pct_change": 100.0,
          "direction": "up",
          "significant": true
        },
        "flow_iWAURR": {
          "current": 13.4,
          "prior": 18.8,
          "abs_change": -5.4,
          "pct_change": -28.7,
          "direction": "down",
          "significant": true
        },
        "flow_WAU_Loss_Rate": {
          "current": 8.8,
          "prior": 6.0,
          "abs_change": 2.8,
          "pct_change": 46.7,
          "direction": "up",
          "significant": false
        },
        "flow_iMAURR": {
          "current": 1.3,
          "prior": 2.3,
          "abs_change": -1.0,
          "pct_change": -43.5,
          "direction": "down",
          "significant": false
        },
        "flow_MAU_Loss_Rate": {
          "current": 7.0,
          "prior": 6.4,
          "abs_change": 0.6,
          "pct_change": 9.4,
          "direction": "up",
          "significant": false
        },
        "flow_Resurrection_Rate": {
          "current": 0.1,
          "prior": 0.3,
          "abs_change": -0.2,
          "pct_change": -66.7,
          "direction": "down",
          "significant": false
        }
      }
    },
    "weekly": {
      "available": false,
      "as_of": null,
      "label": "vs 7d ago",
      "metrics": {}
    },
    "monthly": {
      "available": false,
      "as_of": null,
      "label": "vs 30d ago",
      "metrics": {}
    }
  },
  "key_insights": {
    "summary": "Subscribers: 1/17 this month (500 by Dec 31). 78.7% of the base is dead. 24 users are at-risk (recoverable before 30d dead). Focus on at-risk WAU and resurrection levers.",
    "items": [
      {
        "severity": "high",
        "title": "Product Hunt in 2 days",
        "detail": "Launch May 27 ~3am ET may add 200\u20132000 users on top of 176 waitlist. Subscriber goal: 500 by Dec 31.",
        "lever": "Maximize 24h activation and limit-hitter \u2192 paid conversion before and during launch.",
        "metrics": [
          "activation_24h_pct",
          "premium_conversion_pct"
        ],
        "anchor": "activation"
      },
      {
        "severity": "high",
        "title": "Subscriber goal gap",
        "detail": "1 paid subscribers \u2014 May 2026 target 17 (16 behind). Year-end goal: 500 by Dec 31 (499 to go).",
        "lever": "Improve upgrade path at token limit; resurrect engaged free users.",
        "metrics": [
          "premium_conversion_pct",
          "limit_hitter_conversion_pct"
        ],
        "anchor": "monetization"
      },
      {
        "severity": "high",
        "title": "Gross margin below 80% target",
        "detail": "Current gross margin 79.5% vs 80.0% goal (gap 0.5 pp).",
        "lever": "Reduce API burn per user and grow paid conversion to improve margin.",
        "metrics": [
          "gross_margin_pct",
          "arpu_net_usd"
        ],
        "anchor": "monetization"
      },
      {
        "severity": "high",
        "title": "Lifecycle emails missed (overdue, not in cs_outreach_log)",
        "detail": "30 user(s) in the signup window should have received emails but have no log row: welcome_email: 10; activation_nudge_24h: 5; activation_cs_calendar: 4; nps_day3: 9; pmf_day10: 2.",
        "lever": "Check lifecycle-on-signup webhook, pg_cron job_run_details, and Brevo delivery.",
        "metrics": [],
        "anchor": "lifecycle-email-delivery"
      },
      {
        "severity": "high",
        "title": "Welcome email delivery below target",
        "detail": "Welcome delivery rate is 9.1% in the last 30-day signup window (target 95.0%).",
        "lever": "Verify users INSERT webhook \u2192 lifecycle-on-signup and Brevo template 54.",
        "metrics": [],
        "anchor": "lifecycle-email-delivery"
      },
      {
        "severity": "high",
        "title": "Majority of users are dead",
        "detail": "78.7% of users (96/122) have had no activity in 30+ days.",
        "lever": "Prioritize resurrection email flows and at-risk prevention (iWAURR).",
        "metrics": [
          "bucket_dead"
        ],
        "anchor": "dau-model"
      },
      {
        "severity": "medium",
        "title": "Low welcome email coverage for recent signups",
        "detail": "Only 9.1% of users who signed up in the last 30 days received welcome_email (1/11).",
        "lever": "Check lifecycle-on-signup webhook on users INSERT and Brevo template delivery.",
        "metrics": [],
        "anchor": "lifecycle-email-sends"
      },
      {
        "severity": "medium",
        "title": "Current users are slipping to at-risk",
        "detail": "1-CURR 63.5% \u2014 habitual users missing days.",
        "lever": "Habit loops, return triggers, and session reminders.",
        "metrics": [
          "flow_1-CURR",
          "flow_CURR"
        ],
        "anchor": "dau-model"
      }
    ],
    "focus_areas": [
      "resurrection",
      "at_risk_wau",
      "at_risk_mau"
    ],
    "delta_period_used": "weekly"
  },
  "metric_tooltips": {
    "feedback_submission_rate_pct": "What it means: Share of users who submitted at least one feedback/training event. Signals product involvement beyond passive use.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Context: 176 on waitlist. Product Hunt launch may add 200\u20132000 signups in ~2 days \u2014 activation and conversion drive the 500 subscriber goal by Dec 31.",
    "time_to_first_prompt_median": "What it means: Median hours from account creation to first AI prompt.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Context: 176 on waitlist. Product Hunt launch may add 200\u20132000 signups in ~2 days \u2014 activation and conversion drive the 500 subscriber goal by Dec 31.",
    "bucket_dead": "What it means: Dead users: No activity in the last 30 days\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx. Reducing dead/at-risk users supports DAU and subscriber goals.",
    "retention_d7": "What it means: Share of users who came back on day 7 after signup (session or AI usage). A leading indicator of whether new users stick.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Context: 176 on waitlist. Product Hunt launch may add 200\u20132000 signups in ~2 days \u2014 activation and conversion drive the 500 subscriber goal by Dec 31.",
    "flow_iMAURR": "What it means: At-risk MAU \u2192 Reactivated \u2014 average daily % of users making this transition over the last 7 days. Higher resurrection and iWAURR/iMAURR help win back at-risk and dead users.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx. Reducing dead/at-risk users supports DAU and subscriber goals.",
    "premium_users": "Trend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 500 paid subscribers by Dec 31, 2026; May 2026 target: 17 (behind pace). You have 1 (0.2% of year-end goal). Gap to year-end: 499 subscribers.",
    "bucket_at_risk_wau": "What it means: At-risk WAU: Inactive today, active on at least one of the prior 6 days\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx. Reducing dead/at-risk users supports DAU and subscriber goals.",
    "flow_Resurrection_Rate": "What it means: Dead \u2192 Resurrected \u2014 average daily % of users making this transition over the last 7 days. Higher resurrection and iWAURR/iMAURR help win back at-risk and dead users.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx. Reducing dead/at-risk users supports DAU and subscriber goals.",
    "churn_7d_pct": "What it means: Among users who were ever active, the share with no return in the last 7 days. Lower is better \u2014 rising churn means more slipping away.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx. Lower churn protects DAU and path to 500 subscribers.",
    "power_users_week0": "What it means: Users with 10+ AI prompts in their first 7 days.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Context: 176 on waitlist. Product Hunt launch may add 200\u20132000 signups in ~2 days \u2014 activation and conversion drive the 500 subscriber goal by Dec 31.",
    "arpu_net": "What it means: Average revenue per user after subtracting estimated API costs. Net unit economics per user.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Context: 176 on waitlist. Product Hunt launch may add 200\u20132000 signups in ~2 days \u2014 activation and conversion drive the 500 subscriber goal by Dec 31.",
    "feedback_rate": "What it means: Share of users who submitted at least one feedback/training event. Signals product involvement beyond passive use.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Context: 176 on waitlist. Product Hunt launch may add 200\u20132000 signups in ~2 days \u2014 activation and conversion drive the 500 subscriber goal by Dec 31.",
    "power_users_day0": "What it means: Users with 10+ AI prompts on their signup day.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Context: 176 on waitlist. Product Hunt launch may add 200\u20132000 signups in ~2 days \u2014 activation and conversion drive the 500 subscriber goal by Dec 31.",
    "activation_24h_pct": "What it means: Share of all users who sent their first AI prompt within 24 hours of signing up. Higher means onboarding is working quickly.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Context: 176 on waitlist. Product Hunt launch may add 200\u20132000 signups in ~2 days \u2014 activation and conversion drive the 500 subscriber goal by Dec 31. Goal: 500 paid subscribers by Dec 31, 2026; May 2026 target: 17 (behind pace). You have 1 (0.2% of year-end goal). Gap to year-end: 499 subscribers.",
    "flow_WAU_Loss_Rate": "What it means: At-risk WAU \u2192 At-risk MAU \u2014 average daily % of users making this transition over the last 7 days. Higher resurrection and iWAURR/iMAURR help win back at-risk and dead users.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx. Reducing dead/at-risk users supports DAU and subscriber goals.",
    "churn_30d_pct": "What it means: Ever-active users with no activity in the last 30 days.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx. Lower churn protects DAU and path to 500 subscribers.",
    "activation_24h": "What it means: Share of all users who sent their first AI prompt within 24 hours of signing up. Higher means onboarding is working quickly.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Context: 176 on waitlist. Product Hunt launch may add 200\u20132000 signups in ~2 days \u2014 activation and conversion drive the 500 subscriber goal by Dec 31.",
    "total_users": "Trend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Context: 176 on waitlist. Product Hunt launch may add 200\u20132000 signups in ~2 days \u2014 activation and conversion drive the 500 subscriber goal by Dec 31.",
    "flow_SURR": "What it means: Resurrected \u2192 Current \u2014 average daily % of users making this transition over the last 7 days. Higher resurrection and iWAURR/iMAURR help win back at-risk and dead users.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx. Reducing dead/at-risk users supports DAU and subscriber goals.",
    "bucket_new": "What it means: New users: First day of engagement ever\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx. Reducing dead/at-risk users supports DAU and subscriber goals.",
    "churn_7d": "What it means: Among users who were ever active, the share with no return in the last 7 days. Lower is better \u2014 rising churn means more slipping away.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx. Lower churn protects DAU and path to 500 subscribers.",
    "flow_CURR": "What it means: Current \u2192 Current \u2014 average daily % of users making this transition over the last 7 days. Higher resurrection and iWAURR/iMAURR help win back at-risk and dead users.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx. Reducing dead/at-risk users supports DAU and subscriber goals.",
    "median_days_to_first_limit": "What it means: Typical days from signup until a user first hits the token cap. Shorter often means heavy early usage.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Context: 176 on waitlist. Product Hunt launch may add 200\u20132000 signups in ~2 days \u2014 activation and conversion drive the 500 subscriber goal by Dec 31.",
    "gross_margin_pct": "Trend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 80.0% gross margin. Current: 79.5% (below target). Gap: 0.5 pp to target. Goal: 500 paid subscribers by Dec 31, 2026; May 2026 target: 17 (behind pace). You have 1 (0.2% of year-end goal). Gap to year-end: 499 subscribers.",
    "bucket_current": "What it means: Current users: Active today and at least one other day in the prior 7 days\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx. Reducing dead/at-risk users supports DAU and subscriber goals.",
    "bucket_reactivated": "What it means: Reactivated users: First day back after 7\u201329 days away\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx. Reducing dead/at-risk users supports DAU and subscriber goals.",
    "churn_14d": "What it means: Ever-active users with no activity in the last 14 days.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx. Lower churn protects DAU and path to 500 subscribers.",
    "token_limit_hit_rate": "What it means: Share of users who hit the daily AI token cap at least once. Often signals power users who may upgrade.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Context: 176 on waitlist. Product Hunt launch may add 200\u20132000 signups in ~2 days \u2014 activation and conversion drive the 500 subscriber goal by Dec 31.",
    "flow_1-RURR": "What it means: Reactivated \u2192 At-risk WAU \u2014 average daily % of users making this transition over the last 7 days. Higher resurrection and iWAURR/iMAURR help win back at-risk and dead users.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx. Reducing dead/at-risk users supports DAU and subscriber goals.",
    "conversion_velocity": "What it means: Median hours from signup to first premium upgrade among paying users.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Context: 176 on waitlist. Product Hunt launch may add 200\u20132000 signups in ~2 days \u2014 activation and conversion drive the 500 subscriber goal by Dec 31.",
    "churn_30d": "What it means: Ever-active users with no activity in the last 30 days.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx. Lower churn protects DAU and path to 500 subscribers.",
    "flow_1-CURR": "What it means: Current \u2192 At-risk WAU \u2014 average daily % of users making this transition over the last 7 days. Higher resurrection and iWAURR/iMAURR help win back at-risk and dead users.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx. Reducing dead/at-risk users supports DAU and subscriber goals.",
    "bucket_resurrected": "What it means: Resurrected users: First day back after 30+ days away\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx. Reducing dead/at-risk users supports DAU and subscriber goals.",
    "premium_conversion": "What it means: Share of all users counted as paid subscribers ($20/mo Stripe plans). Count = baseline 1 plus distinct user_plans from May 24, 2026 onward.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Context: 176 on waitlist. Product Hunt launch may add 200\u20132000 signups in ~2 days \u2014 activation and conversion drive the 500 subscriber goal by Dec 31.",
    "churn_14d_pct": "What it means: Ever-active users with no activity in the last 14 days.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx. Lower churn protects DAU and path to 500 subscribers.",
    "bucket_at_risk_mau": "What it means: At-risk MAU: Inactive today and prior 6 days, active 7\u201329 days ago\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx. Reducing dead/at-risk users supports DAU and subscriber goals.",
    "wau": "What it means: DAU plus users at-risk WAU (active recently but not today).\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx.",
    "premium_conversion_pct": "What it means: Share of all users counted as paid subscribers ($20/mo Stripe plans). Count = baseline 1 plus distinct user_plans from May 24, 2026 onward.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 500 paid subscribers by Dec 31, 2026; May 2026 target: 17 (behind pace). You have 1 (0.2% of year-end goal). Gap to year-end: 499 subscribers.",
    "retention_d7_pct": "What it means: Share of users who came back on day 7 after signup (session or AI usage). A leading indicator of whether new users stick.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Context: 176 on waitlist. Product Hunt launch may add 200\u20132000 signups in ~2 days \u2014 activation and conversion drive the 500 subscriber goal by Dec 31. Goal: 500 paid subscribers by Dec 31, 2026; May 2026 target: 17 (behind pace). You have 1 (0.2% of year-end goal). Gap to year-end: 499 subscribers.",
    "latest_wau": "What it means: Users active at least once in the last 7 days (sessions or AI prompts). Shows near-term engagement momentum.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx.",
    "multi_day_ai_7d": "What it means: Users who used AI on more than one day in their first week.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Context: 176 on waitlist. Product Hunt launch may add 200\u20132000 signups in ~2 days \u2014 activation and conversion drive the 500 subscriber goal by Dec 31.",
    "flow_NURR": "What it means: New \u2192 Current \u2014 average daily % of users making this transition over the last 7 days. Higher resurrection and iWAURR/iMAURR help win back at-risk and dead users.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx. Reducing dead/at-risk users supports DAU and subscriber goals.",
    "flow_1-SURR": "What it means: Resurrected \u2192 At-risk WAU \u2014 average daily % of users making this transition over the last 7 days. Higher resurrection and iWAURR/iMAURR help win back at-risk and dead users.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx. Reducing dead/at-risk users supports DAU and subscriber goals.",
    "mau": "What it means: WAU plus users at-risk MAU (active 7\u201329 days ago, inactive lately).\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx.",
    "flow_MAU_Loss_Rate": "What it means: At-risk MAU \u2192 Dead \u2014 average daily % of users making this transition over the last 7 days. Higher resurrection and iWAURR/iMAURR help win back at-risk and dead users.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx. Reducing dead/at-risk users supports DAU and subscriber goals.",
    "median_hours_to_first_limit": "What it means: Same as days to first limit, in hours.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Context: 176 on waitlist. Product Hunt launch may add 200\u20132000 signups in ~2 days \u2014 activation and conversion drive the 500 subscriber goal by Dec 31.",
    "dau": "What it means: Users engaged today: new, current, reactivated, or resurrected.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx.",
    "limit_hitter_conversion_pct": "What it means: Of users who hit token limits, how many are on a paid plan. Measures whether limits drive upgrades.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 500 paid subscribers by Dec 31, 2026; May 2026 target: 17 (behind pace). You have 1 (0.2% of year-end goal). Gap to year-end: 499 subscribers.",
    "limit_hitter_conversion": "What it means: Of users who hit token limits, how many are on a paid plan. Measures whether limits drive upgrades.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Context: 176 on waitlist. Product Hunt launch may add 200\u20132000 signups in ~2 days \u2014 activation and conversion drive the 500 subscriber goal by Dec 31.",
    "flow_iWAURR": "What it means: At-risk WAU \u2192 Current \u2014 average daily % of users making this transition over the last 7 days. Higher resurrection and iWAURR/iMAURR help win back at-risk and dead users.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx. Reducing dead/at-risk users supports DAU and subscriber goals.",
    "flow_RURR": "What it means: Reactivated \u2192 Current \u2014 average daily % of users making this transition over the last 7 days. Higher resurrection and iWAURR/iMAURR help win back at-risk and dead users.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx. Reducing dead/at-risk users supports DAU and subscriber goals.",
    "flow_1-NURR": "What it means: New \u2192 At-risk WAU \u2014 average daily % of users making this transition over the last 7 days. Higher resurrection and iWAURR/iMAURR help win back at-risk and dead users.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 4.5\u00d7 DAU vs launch-week baseline (set after PH launch). Focus on activation before May 27 influx. Reducing dead/at-risk users supports DAU and subscriber goals.",
    "token_limit_hit_rate_pct": "What it means: Share of users who hit the daily AI token cap at least once. Often signals power users who may upgrade.\n\nTrend: Not enough daily snapshot history yet to show a trend.\n\nGoals: Goal: 80.0% gross margin. Current: 79.5% (below target). Gap: 0.5 pp to target. Goal: 500 paid subscribers by Dec 31, 2026; May 2026 target: 17 (behind pace). You have 1 (0.2% of year-end goal). Gap to year-end: 499 subscribers."
  },
  "corporate_goals": {
    "subscribers": {
      "current": 1,
      "target_year_end": 500,
      "year_end_date": "2026-12-31",
      "pct_of_year_end_goal": 0.2,
      "gap_year_end": 499,
      "month": "2026-05",
      "month_label": "May 2026",
      "month_target": 17,
      "prorated_target": 5,
      "on_track_month": false,
      "on_track_year_end": false,
      "monthly_targets": [
        {
          "month": "2026-05",
          "label": "May 2026",
          "cumulative_target": 17
        },
        {
          "month": "2026-06",
          "label": "June 2026",
          "cumulative_target": 85
        },
        {
          "month": "2026-07",
          "label": "July 2026",
          "cumulative_target": 155
        },
        {
          "month": "2026-08",
          "label": "August 2026",
          "cumulative_target": 225
        },
        {
          "month": "2026-09",
          "label": "September 2026",
          "cumulative_target": 292
        },
        {
          "month": "2026-10",
          "label": "October 2026",
          "cumulative_target": 362
        },
        {
          "month": "2026-11",
          "label": "November 2026",
          "cumulative_target": 430
        },
        {
          "month": "2026-12",
          "label": "December 2026",
          "cumulative_target": 500
        }
      ],
      "target": 17,
      "pct_of_goal": 5.9,
      "gap": 16,
      "on_track": false
    },
    "gross_margin_pct": {
      "current": 79.5,
      "target": 80.0,
      "gap_pp": 0.5,
      "on_track": false
    },
    "dau_multiple": {
      "current_dau": 2,
      "baseline": null,
      "multiple": null,
      "target_multiple": 4.5,
      "on_track": false,
      "status": "pre_launch"
    },
    "launch": {
      "date": "2026-05-27",
      "days_until": 2,
      "days_since": 0,
      "post_launch": false,
      "waitlist": 176,
      "ph_signup_range": [
        200,
        2000
      ]
    }
  },
  "email_provider_capacity": {
    "as_of": "2026-05-25",
    "providers": [
      {
        "id": "hubspot",
        "name": "HubSpot",
        "funnel_role": "phase_3_terminal",
        "status": "ok",
        "contacts_used": 19,
        "contacts_limit": 1000000,
        "monthly_sends_projected": 0.0,
        "monthly_sends_limit": 2000,
        "daily_sends_projected": 0.0,
        "daily_sends_limit": null,
        "runway_months": null,
        "metrics": [
          {
            "key": "contacts",
            "used": 19,
            "limit": 1000000,
            "pct": 0.0,
            "near_limit": false,
            "at_limit": false
          },
          {
            "key": "sends_monthly",
            "used": 0.0,
            "limit": 2000,
            "pct": 0.0,
            "near_limit": false,
            "at_limit": false
          }
        ],
        "near_limit_errors": []
      },
      {
        "id": "brevo",
        "name": "Brevo",
        "funnel_role": "phase_1_primary",
        "status": "ok",
        "contacts_used": 122,
        "contacts_limit": 2000,
        "monthly_sends_projected": 354.0,
        "monthly_sends_limit": null,
        "daily_sends_projected": 11.8,
        "daily_sends_limit": 300,
        "runway_months": null,
        "metrics": [
          {
            "key": "contacts",
            "used": 122,
            "limit": 2000,
            "pct": 0.061,
            "near_limit": false,
            "at_limit": false
          },
          {
            "key": "sends_daily",
            "used": 11.8,
            "limit": 300,
            "pct": 0.039,
            "near_limit": false,
            "at_limit": false
          }
        ],
        "near_limit_errors": []
      },
      {
        "id": "omnisend",
        "name": "OmniSend",
        "funnel_role": "fallback",
        "status": "ok",
        "contacts_used": 0,
        "contacts_limit": 250,
        "monthly_sends_projected": 0.0,
        "monthly_sends_limit": 500,
        "daily_sends_projected": 0.0,
        "daily_sends_limit": null,
        "runway_months": null,
        "metrics": [
          {
            "key": "contacts",
            "used": 0,
            "limit": 250,
            "pct": 0.0,
            "near_limit": false,
            "at_limit": false
          },
          {
            "key": "sends_monthly",
            "used": 0.0,
            "limit": 500,
            "pct": 0.0,
            "near_limit": false,
            "at_limit": false
          }
        ],
        "near_limit_errors": []
      },
      {
        "id": "mailerlite",
        "name": "MailerLite",
        "funnel_role": "fallback",
        "status": "ok",
        "contacts_used": 0,
        "contacts_limit": 500,
        "monthly_sends_projected": 0.0,
        "monthly_sends_limit": 12000,
        "daily_sends_projected": 0.0,
        "daily_sends_limit": null,
        "runway_months": null,
        "metrics": [
          {
            "key": "contacts",
            "used": 0,
            "limit": 500,
            "pct": 0.0,
            "near_limit": false,
            "at_limit": false
          },
          {
            "key": "sends_monthly",
            "used": 0.0,
            "limit": 12000,
            "pct": 0.0,
            "near_limit": false,
            "at_limit": false
          }
        ],
        "near_limit_errors": []
      },
      {
        "id": "emailoctopus",
        "name": "EmailOctopus",
        "funnel_role": "phase_2_conversion",
        "status": "ok",
        "contacts_used": 121,
        "contacts_limit": 2500,
        "monthly_sends_projected": 289.0,
        "monthly_sends_limit": 10000,
        "daily_sends_projected": 9.6,
        "daily_sends_limit": null,
        "runway_months": 34.6,
        "metrics": [
          {
            "key": "contacts",
            "used": 121,
            "limit": 2500,
            "pct": 0.048,
            "near_limit": false,
            "at_limit": false
          },
          {
            "key": "sends_monthly",
            "used": 289.0,
            "limit": 10000,
            "pct": 0.029,
            "near_limit": false,
            "at_limit": false
          }
        ],
        "near_limit_errors": []
      },
      {
        "id": "resend",
        "name": "Resend",
        "funnel_role": "phase_2_paid",
        "status": "ok",
        "contacts_used": 1,
        "contacts_limit": null,
        "monthly_sends_projected": 1.0,
        "monthly_sends_limit": 3000,
        "daily_sends_projected": 0.0,
        "daily_sends_limit": 100,
        "runway_months": 3000.0,
        "metrics": [
          {
            "key": "sends_monthly",
            "used": 1.0,
            "limit": 3000,
            "pct": 0.0,
            "near_limit": false,
            "at_limit": false
          },
          {
            "key": "sends_daily",
            "used": 0.0,
            "limit": 100,
            "pct": 0.0,
            "near_limit": false,
            "at_limit": false
          }
        ],
        "near_limit_errors": []
      },
      {
        "id": "loops",
        "name": "Loops",
        "funnel_role": "fallback",
        "status": "ok",
        "contacts_used": 122,
        "contacts_limit": 1000,
        "monthly_sends_projected": 0.0,
        "monthly_sends_limit": 4000,
        "daily_sends_projected": 0.0,
        "daily_sends_limit": null,
        "runway_months": null,
        "metrics": [
          {
            "key": "contacts",
            "used": 122,
            "limit": 1000,
            "pct": 0.122,
            "near_limit": false,
            "at_limit": false
          },
          {
            "key": "sends_monthly",
            "used": 0.0,
            "limit": 4000,
            "pct": 0.0,
            "near_limit": false,
            "at_limit": false
          }
        ],
        "near_limit_errors": []
      },
      {
        "id": "ses",
        "name": "Amazon SES",
        "funnel_role": "operational",
        "status": "blocked_sandbox",
        "contacts_used": 122,
        "contacts_limit": null,
        "monthly_sends_projected": 0.0,
        "monthly_sends_limit": null,
        "daily_sends_projected": 0.0,
        "daily_sends_limit": 200,
        "runway_months": null,
        "metrics": [
          {
            "key": "sends_daily",
            "used": 0.0,
            "limit": 200,
            "pct": 0.0,
            "near_limit": false,
            "at_limit": false
          }
        ],
        "near_limit_errors": []
      }
    ],
    "pool_aggregate": {
      "send_used": 1.0,
      "send_cap": 19500.0,
      "contact_used": 122,
      "contact_cap": 1750,
      "provider_count": 4
    },
    "operational_pool_aggregate": {
      "send_used": 61.0,
      "send_cap": 50000.0,
      "daily_used": 2.0,
      "daily_cap": 0.0,
      "provider_count": 2,
      "primary_provider_id": "ses",
      "failover_provider_id": "resend",
      "ses_sandbox": true
    },
    "ses_sandbox": true,
    "any_near_limit": false,
    "estimation_note": "v1 estimates: Brevo Phase 1 (2k automation entrants \u00b7 300/day); EmailOctopus Phase 2 conversion; fallback pool = MailerLite + OmniSend + Loops + Resend; operational pool = SES primary, Resend Pro backup; HubSpot = paid + company email."
  },
  "lifecycle_readiness": {
    "as_of": "2026-05-25",
    "milestones": [
      {
        "id": "welcome_sent",
        "label": "Welcome email sent",
        "type": "email",
        "status": "live",
        "dedup_trigger_name": "welcome_email"
      },
      {
        "id": "activation_nudge_sent",
        "label": "Activation nudge sent",
        "type": "email",
        "status": "live",
        "dedup_trigger_name": "activation_nudge_24h"
      },
      {
        "id": "activation_cs_sent",
        "label": "CS calendar email sent",
        "type": "email",
        "status": "live",
        "dedup_trigger_name": "activation_cs_calendar"
      },
      {
        "id": "first_ai_prompt",
        "label": "First AI prompt sent",
        "type": "product",
        "status": "live",
        "source_table": "llm_usage"
      },
      {
        "id": "daily_limit_hit",
        "label": "Daily token limit hit \u22651",
        "type": "product",
        "status": "live",
        "source_table": "llm_daily_usage"
      },
      {
        "id": "training_done",
        "label": "AI assistant trained \u22651 (earns 1,000 tokens)",
        "type": "product",
        "status": "live",
        "source_table": "feedback_events"
      },
      {
        "id": "nps_sent",
        "label": "NPS email sent (D3)",
        "type": "email",
        "status": "live",
        "dedup_trigger_name": "nps_day3"
      },
      {
        "id": "pmf_sent",
        "label": "PMF email sent (D10)",
        "type": "email",
        "status": "live",
        "dedup_trigger_name": "pmf_day10"
      }
    ],
    "product_milestone_count": 3,
    "by_bucket": {
      "new": {
        "users": 0,
        "milestones": {
          "welcome_sent": {
            "count": 0,
            "pct": null
          },
          "activation_nudge_sent": {
            "count": 0,
            "pct": null
          },
          "activation_cs_sent": {
            "count": 0,
            "pct": null
          },
          "first_ai_prompt": {
            "count": 0,
            "pct": null
          },
          "daily_limit_hit": {
            "count": 0,
            "pct": null
          },
          "training_done": {
            "count": 0,
            "pct": null
          },
          "nps_sent": {
            "count": 0,
            "pct": null
          },
          "pmf_sent": {
            "count": 0,
            "pct": null
          }
        },
        "readiness": {
          "avg_score": 0.0,
          "max_score": 8
        }
      },
      "current": {
        "users": 1,
        "milestones": {
          "welcome_sent": {
            "count": 0,
            "pct": 0.0
          },
          "activation_nudge_sent": {
            "count": 0,
            "pct": 0.0
          },
          "activation_cs_sent": {
            "count": 0,
            "pct": 0.0
          },
          "first_ai_prompt": {
            "count": 1,
            "pct": 100.0
          },
          "daily_limit_hit": {
            "count": 1,
            "pct": 100.0
          },
          "training_done": {
            "count": 1,
            "pct": 100.0
          },
          "nps_sent": {
            "count": 0,
            "pct": 0.0
          },
          "pmf_sent": {
            "count": 0,
            "pct": 0.0
          }
        },
        "readiness": {
          "avg_score": 3.0,
          "max_score": 8
        }
      },
      "reactivated": {
        "users": 1,
        "milestones": {
          "welcome_sent": {
            "count": 0,
            "pct": 0.0
          },
          "activation_nudge_sent": {
            "count": 0,
            "pct": 0.0
          },
          "activation_cs_sent": {
            "count": 0,
            "pct": 0.0
          },
          "first_ai_prompt": {
            "count": 1,
            "pct": 100.0
          },
          "daily_limit_hit": {
            "count": 0,
            "pct": 0.0
          },
          "training_done": {
            "count": 1,
            "pct": 100.0
          },
          "nps_sent": {
            "count": 0,
            "pct": 0.0
          },
          "pmf_sent": {
            "count": 0,
            "pct": 0.0
          }
        },
        "readiness": {
          "avg_score": 2.0,
          "max_score": 8
        }
      },
      "resurrected": {
        "users": 0,
        "milestones": {
          "welcome_sent": {
            "count": 0,
            "pct": null
          },
          "activation_nudge_sent": {
            "count": 0,
            "pct": null
          },
          "activation_cs_sent": {
            "count": 0,
            "pct": null
          },
          "first_ai_prompt": {
            "count": 0,
            "pct": null
          },
          "daily_limit_hit": {
            "count": 0,
            "pct": null
          },
          "training_done": {
            "count": 0,
            "pct": null
          },
          "nps_sent": {
            "count": 0,
            "pct": null
          },
          "pmf_sent": {
            "count": 0,
            "pct": null
          }
        },
        "readiness": {
          "avg_score": 0.0,
          "max_score": 8
        }
      },
      "at_risk_wau": {
        "users": 12,
        "milestones": {
          "welcome_sent": {
            "count": 1,
            "pct": 8.3
          },
          "activation_nudge_sent": {
            "count": 0,
            "pct": 0.0
          },
          "activation_cs_sent": {
            "count": 0,
            "pct": 0.0
          },
          "first_ai_prompt": {
            "count": 12,
            "pct": 100.0
          },
          "daily_limit_hit": {
            "count": 0,
            "pct": 0.0
          },
          "training_done": {
            "count": 8,
            "pct": 66.7
          },
          "nps_sent": {
            "count": 0,
            "pct": 0.0
          },
          "pmf_sent": {
            "count": 0,
            "pct": 0.0
          }
        },
        "readiness": {
          "avg_score": 1.75,
          "max_score": 8
        }
      },
      "at_risk_mau": {
        "users": 12,
        "milestones": {
          "welcome_sent": {
            "count": 0,
            "pct": 0.0
          },
          "activation_nudge_sent": {
            "count": 0,
            "pct": 0.0
          },
          "activation_cs_sent": {
            "count": 0,
            "pct": 0.0
          },
          "first_ai_prompt": {
            "count": 12,
            "pct": 100.0
          },
          "daily_limit_hit": {
            "count": 0,
            "pct": 0.0
          },
          "training_done": {
            "count": 6,
            "pct": 50.0
          },
          "nps_sent": {
            "count": 0,
            "pct": 0.0
          },
          "pmf_sent": {
            "count": 0,
            "pct": 0.0
          }
        },
        "readiness": {
          "avg_score": 1.5,
          "max_score": 8
        }
      },
      "dead": {
        "users": 96,
        "milestones": {
          "welcome_sent": {
            "count": 1,
            "pct": 1.0
          },
          "activation_nudge_sent": {
            "count": 1,
            "pct": 1.0
          },
          "activation_cs_sent": {
            "count": 1,
            "pct": 1.0
          },
          "first_ai_prompt": {
            "count": 44,
            "pct": 45.8
          },
          "daily_limit_hit": {
            "count": 0,
            "pct": 0.0
          },
          "training_done": {
            "count": 13,
            "pct": 13.5
          },
          "nps_sent": {
            "count": 1,
            "pct": 1.0
          },
          "pmf_sent": {
            "count": 1,
            "pct": 1.0
          }
        },
        "readiness": {
          "avg_score": 0.65,
          "max_score": 8
        }
      }
    },
    "totals": {
      "users": 122,
      "milestones": {
        "welcome_sent": {
          "count": 2,
          "pct": 1.6
        },
        "activation_nudge_sent": {
          "count": 1,
          "pct": 0.8
        },
        "activation_cs_sent": {
          "count": 1,
          "pct": 0.8
        },
        "first_ai_prompt": {
          "count": 70,
          "pct": 57.4
        },
        "daily_limit_hit": {
          "count": 1,
          "pct": 0.8
        },
        "training_done": {
          "count": 29,
          "pct": 23.8
        },
        "nps_sent": {
          "count": 1,
          "pct": 0.8
        },
        "pmf_sent": {
          "count": 1,
          "pct": 0.8
        }
      },
      "users_with_any_product_milestone": 71,
      "pct_with_any_product_milestone": 58.2,
      "avg_readiness_score": 0.87,
      "max_score": 8
    }
  },
  "lifecycle_email_sends": {
    "as_of": "2026-05-25",
    "outreach_log_available": true,
    "outreach_log_row_count": 6,
    "new_user_window_days": 30,
    "cohort": {
      "label": "Active signups last 30 days",
      "users": 11,
      "triggers": [
        {
          "dedup_trigger_name": "welcome_email",
          "sequence_id": "welcome",
          "label": "Oasis Welcome",
          "brevo_template": "Oasis Welcome",
          "channel": "event",
          "when": "users INSERT (signup)",
          "sent_count": 1,
          "pct_of_cohort": 9.1
        },
        {
          "dedup_trigger_name": "activation_nudge_24h",
          "sequence_id": "activation_nudge",
          "label": "Oasis Activation Nudge",
          "brevo_template": "Oasis Activation Nudge",
          "channel": "cron",
          "when": "\u226524h after created_at",
          "sent_count": 1,
          "pct_of_cohort": 9.1
        },
        {
          "dedup_trigger_name": "activation_cs_calendar",
          "sequence_id": "activation_cs_calendar",
          "label": "Oasis Activation CS Calendar",
          "brevo_template": "Oasis Activation CS Calendar",
          "channel": "cron",
          "when": "day 3\u20135 after signup",
          "sent_count": 1,
          "pct_of_cohort": 9.1
        },
        {
          "dedup_trigger_name": "nps_day3",
          "sequence_id": "nps_day3",
          "label": "Oasis NPS",
          "brevo_template": "Oasis NPS",
          "channel": "cron",
          "when": "day 3\u20135 after signup",
          "sent_count": 1,
          "pct_of_cohort": 9.1
        },
        {
          "dedup_trigger_name": "pmf_day10",
          "sequence_id": "pmf_day10",
          "label": "Oasis PMF",
          "brevo_template": "Oasis PMF",
          "channel": "cron",
          "when": "day 10\u201312 after signup",
          "sent_count": 1,
          "pct_of_cohort": 9.1
        }
      ],
      "users_with_any_lifecycle_email": 1,
      "pct_with_any_lifecycle_email": 9.1,
      "users_with_all_five": 1,
      "pct_with_all_five": 9.1
    },
    "new_bucket": {
      "label": "DAU bucket: new (within cohort window)",
      "users": 0,
      "triggers": [
        {
          "dedup_trigger_name": "welcome_email",
          "sequence_id": "welcome",
          "label": "Oasis Welcome",
          "brevo_template": "Oasis Welcome",
          "channel": "event",
          "when": "users INSERT (signup)",
          "sent_count": 0,
          "pct_of_cohort": null
        },
        {
          "dedup_trigger_name": "activation_nudge_24h",
          "sequence_id": "activation_nudge",
          "label": "Oasis Activation Nudge",
          "brevo_template": "Oasis Activation Nudge",
          "channel": "cron",
          "when": "\u226524h after created_at",
          "sent_count": 0,
          "pct_of_cohort": null
        },
        {
          "dedup_trigger_name": "activation_cs_calendar",
          "sequence_id": "activation_cs_calendar",
          "label": "Oasis Activation CS Calendar",
          "brevo_template": "Oasis Activation CS Calendar",
          "channel": "cron",
          "when": "day 3\u20135 after signup",
          "sent_count": 0,
          "pct_of_cohort": null
        },
        {
          "dedup_trigger_name": "nps_day3",
          "sequence_id": "nps_day3",
          "label": "Oasis NPS",
          "brevo_template": "Oasis NPS",
          "channel": "cron",
          "when": "day 3\u20135 after signup",
          "sent_count": 0,
          "pct_of_cohort": null
        },
        {
          "dedup_trigger_name": "pmf_day10",
          "sequence_id": "pmf_day10",
          "label": "Oasis PMF",
          "brevo_template": "Oasis PMF",
          "channel": "cron",
          "when": "day 10\u201312 after signup",
          "sent_count": 0,
          "pct_of_cohort": null
        }
      ]
    },
    "recent_sends_7d": [
      {
        "trigger_name": "welcome_email",
        "count": 2
      },
      {
        "trigger_name": "activation_cs_calendar",
        "count": 1
      },
      {
        "trigger_name": "activation_nudge_24h",
        "count": 1
      },
      {
        "trigger_name": "nps_day3",
        "count": 1
      },
      {
        "trigger_name": "pmf_day10",
        "count": 1
      }
    ]
  },
  "lifecycle_email_delivery": {
    "as_of": "2026-05-25",
    "outreach_log_available": true,
    "rpc_available": true,
    "new_user_window_days": 30,
    "welcome_miss_hours": 2,
    "cohort_users": 11,
    "any_eligible_now_capped": false,
    "missed_total": 30,
    "missed_by_trigger": {
      "welcome_email": 10,
      "activation_nudge_24h": 5,
      "activation_cs_calendar": 4,
      "nps_day3": 9,
      "pmf_day10": 2
    },
    "cron_sent_last_24h": 4,
    "cron_eligible_now": 54,
    "triggers": [
      {
        "dedup_trigger_name": "welcome_email",
        "sequence_id": "welcome",
        "label": "Oasis Welcome",
        "channel": "event",
        "when": "users INSERT (signup)",
        "eligible_now": null,
        "eligible_now_capped": false,
        "rpc_error": null,
        "sent_all_time": 2,
        "sent_in_window": 1,
        "sent_last_24h": 2,
        "sent_last_7d": 2,
        "last_sent_at": "2026-05-25T19:14:15.231083",
        "missed_overdue": 10,
        "delivery_rate_pct": 9.1
      },
      {
        "dedup_trigger_name": "activation_nudge_24h",
        "sequence_id": "activation_nudge",
        "label": "Oasis Activation Nudge",
        "channel": "cron",
        "when": "\u226524h after created_at",
        "eligible_now": 51,
        "eligible_now_capped": false,
        "rpc_error": null,
        "sent_all_time": 1,
        "sent_in_window": 1,
        "sent_last_24h": 1,
        "sent_last_7d": 1,
        "last_sent_at": "2026-05-25T21:00:43.057156",
        "missed_overdue": 5,
        "delivery_rate_pct": 16.7
      },
      {
        "dedup_trigger_name": "activation_cs_calendar",
        "sequence_id": "activation_cs_calendar",
        "label": "Oasis Activation CS Calendar",
        "channel": "cron",
        "when": "day 3\u20135 after signup",
        "eligible_now": 1,
        "eligible_now_capped": false,
        "rpc_error": null,
        "sent_all_time": 1,
        "sent_in_window": 1,
        "sent_last_24h": 1,
        "sent_last_7d": 1,
        "last_sent_at": "2026-05-25T21:05:51.207073",
        "missed_overdue": 4,
        "delivery_rate_pct": 20.0
      },
      {
        "dedup_trigger_name": "nps_day3",
        "sequence_id": "nps_day3",
        "label": "Oasis NPS",
        "channel": "cron",
        "when": "day 3\u20135 after signup",
        "eligible_now": 1,
        "eligible_now_capped": false,
        "rpc_error": null,
        "sent_all_time": 1,
        "sent_in_window": 1,
        "sent_last_24h": 1,
        "sent_last_7d": 1,
        "last_sent_at": "2026-05-25T22:27:03.337616",
        "missed_overdue": 9,
        "delivery_rate_pct": 10.0
      },
      {
        "dedup_trigger_name": "pmf_day10",
        "sequence_id": "pmf_day10",
        "label": "Oasis PMF",
        "channel": "cron",
        "when": "day 10\u201312 after signup",
        "eligible_now": 1,
        "eligible_now_capped": false,
        "rpc_error": null,
        "sent_all_time": 1,
        "sent_in_window": 1,
        "sent_last_24h": 1,
        "sent_last_7d": 1,
        "last_sent_at": "2026-05-25T23:13:24.873150",
        "missed_overdue": 2,
        "delivery_rate_pct": 33.3
      }
    ]
  },
  "email_bucket_impact": {
    "as_of": "2026-05-25",
    "new_user_window_days": 30,
    "cohort_users": 11,
    "bucket_labels": {
      "new": "New users",
      "current": "Current users",
      "reactivated": "Reactivated users",
      "resurrected": "Resurrected users",
      "at_risk_wau": "At-risk WAU",
      "at_risk_mau": "At-risk MAU",
      "dead": "Dead users"
    },
    "methodology": "V1 compares bucket mix today for users who received an email vs those who did not (within the signup cohort). Not causal; flow rates are population-level.",
    "population_flow_rates_pct": {
      "NURR": 50.0,
      "CURR": 36.5,
      "iWAURR": 13.4,
      "Resurrection_Rate": 0.1
    },
    "any_lifecycle_email": {
      "exposed": {
        "users": 1,
        "counts": {
          "new": 0,
          "current": 0,
          "reactivated": 0,
          "resurrected": 0,
          "at_risk_wau": 0,
          "at_risk_mau": 0,
          "dead": 1
        },
        "pct": {
          "new": 0.0,
          "current": 0.0,
          "reactivated": 0.0,
          "resurrected": 0.0,
          "at_risk_wau": 0.0,
          "at_risk_mau": 0.0,
          "dead": 100.0
        }
      },
      "not_exposed": {
        "users": 10,
        "counts": {
          "new": 0,
          "current": 0,
          "reactivated": 0,
          "resurrected": 0,
          "at_risk_wau": 3,
          "at_risk_mau": 2,
          "dead": 5
        },
        "pct": {
          "new": 0.0,
          "current": 0.0,
          "reactivated": 0.0,
          "resurrected": 0.0,
          "at_risk_wau": 30.0,
          "at_risk_mau": 20.0,
          "dead": 50.0
        }
      }
    },
    "by_trigger": [
      {
        "dedup_trigger_name": "welcome_email",
        "label": "Oasis Welcome",
        "exposed": {
          "users": 1,
          "counts": {
            "new": 0,
            "current": 0,
            "reactivated": 0,
            "resurrected": 0,
            "at_risk_wau": 0,
            "at_risk_mau": 0,
            "dead": 1
          },
          "pct": {
            "new": 0.0,
            "current": 0.0,
            "reactivated": 0.0,
            "resurrected": 0.0,
            "at_risk_wau": 0.0,
            "at_risk_mau": 0.0,
            "dead": 100.0
          }
        },
        "not_exposed": {
          "users": 10,
          "counts": {
            "new": 0,
            "current": 0,
            "reactivated": 0,
            "resurrected": 0,
            "at_risk_wau": 3,
            "at_risk_mau": 2,
            "dead": 5
          },
          "pct": {
            "new": 0.0,
            "current": 0.0,
            "reactivated": 0.0,
            "resurrected": 0.0,
            "at_risk_wau": 30.0,
            "at_risk_mau": 20.0,
            "dead": 50.0
          }
        },
        "current_pct_exposed": 0.0,
        "current_pct_not_exposed": 0.0
      },
      {
        "dedup_trigger_name": "activation_nudge_24h",
        "label": "Oasis Activation Nudge",
        "exposed": {
          "users": 1,
          "counts": {
            "new": 0,
            "current": 0,
            "reactivated": 0,
            "resurrected": 0,
            "at_risk_wau": 0,
            "at_risk_mau": 0,
            "dead": 1
          },
          "pct": {
            "new": 0.0,
            "current": 0.0,
            "reactivated": 0.0,
            "resurrected": 0.0,
            "at_risk_wau": 0.0,
            "at_risk_mau": 0.0,
            "dead": 100.0
          }
        },
        "not_exposed": {
          "users": 10,
          "counts": {
            "new": 0,
            "current": 0,
            "reactivated": 0,
            "resurrected": 0,
            "at_risk_wau": 3,
            "at_risk_mau": 2,
            "dead": 5
          },
          "pct": {
            "new": 0.0,
            "current": 0.0,
            "reactivated": 0.0,
            "resurrected": 0.0,
            "at_risk_wau": 30.0,
            "at_risk_mau": 20.0,
            "dead": 50.0
          }
        },
        "current_pct_exposed": 0.0,
        "current_pct_not_exposed": 0.0
      },
      {
        "dedup_trigger_name": "activation_cs_calendar",
        "label": "Oasis Activation CS Calendar",
        "exposed": {
          "users": 1,
          "counts": {
            "new": 0,
            "current": 0,
            "reactivated": 0,
            "resurrected": 0,
            "at_risk_wau": 0,
            "at_risk_mau": 0,
            "dead": 1
          },
          "pct": {
            "new": 0.0,
            "current": 0.0,
            "reactivated": 0.0,
            "resurrected": 0.0,
            "at_risk_wau": 0.0,
            "at_risk_mau": 0.0,
            "dead": 100.0
          }
        },
        "not_exposed": {
          "users": 10,
          "counts": {
            "new": 0,
            "current": 0,
            "reactivated": 0,
            "resurrected": 0,
            "at_risk_wau": 3,
            "at_risk_mau": 2,
            "dead": 5
          },
          "pct": {
            "new": 0.0,
            "current": 0.0,
            "reactivated": 0.0,
            "resurrected": 0.0,
            "at_risk_wau": 30.0,
            "at_risk_mau": 20.0,
            "dead": 50.0
          }
        },
        "current_pct_exposed": 0.0,
        "current_pct_not_exposed": 0.0
      },
      {
        "dedup_trigger_name": "nps_day3",
        "label": "Oasis NPS",
        "exposed": {
          "users": 1,
          "counts": {
            "new": 0,
            "current": 0,
            "reactivated": 0,
            "resurrected": 0,
            "at_risk_wau": 0,
            "at_risk_mau": 0,
            "dead": 1
          },
          "pct": {
            "new": 0.0,
            "current": 0.0,
            "reactivated": 0.0,
            "resurrected": 0.0,
            "at_risk_wau": 0.0,
            "at_risk_mau": 0.0,
            "dead": 100.0
          }
        },
        "not_exposed": {
          "users": 10,
          "counts": {
            "new": 0,
            "current": 0,
            "reactivated": 0,
            "resurrected": 0,
            "at_risk_wau": 3,
            "at_risk_mau": 2,
            "dead": 5
          },
          "pct": {
            "new": 0.0,
            "current": 0.0,
            "reactivated": 0.0,
            "resurrected": 0.0,
            "at_risk_wau": 30.0,
            "at_risk_mau": 20.0,
            "dead": 50.0
          }
        },
        "current_pct_exposed": 0.0,
        "current_pct_not_exposed": 0.0
      },
      {
        "dedup_trigger_name": "pmf_day10",
        "label": "Oasis PMF",
        "exposed": {
          "users": 1,
          "counts": {
            "new": 0,
            "current": 0,
            "reactivated": 0,
            "resurrected": 0,
            "at_risk_wau": 0,
            "at_risk_mau": 0,
            "dead": 1
          },
          "pct": {
            "new": 0.0,
            "current": 0.0,
            "reactivated": 0.0,
            "resurrected": 0.0,
            "at_risk_wau": 0.0,
            "at_risk_mau": 0.0,
            "dead": 100.0
          }
        },
        "not_exposed": {
          "users": 10,
          "counts": {
            "new": 0,
            "current": 0,
            "reactivated": 0,
            "resurrected": 0,
            "at_risk_wau": 3,
            "at_risk_mau": 2,
            "dead": 5
          },
          "pct": {
            "new": 0.0,
            "current": 0.0,
            "reactivated": 0.0,
            "resurrected": 0.0,
            "at_risk_wau": 30.0,
            "at_risk_mau": 20.0,
            "dead": 50.0
          }
        },
        "current_pct_exposed": 0.0,
        "current_pct_not_exposed": 0.0
      }
    ]
  },
  "validation": {
    "payments_success_count": 12,
    "payments_revenue_usd": 124.0,
    "limit_hit_days": 2,
    "plus_users": 1
  }
} as BaselineData;

type BaselineData = {
  generated_at: string;
  snapshot_date: string;
  total_users: number;
  active_users: number;
  limitations: string[];
  activation: {
    activation_rate_pct: Record<string, number | null>;
    time_to_first_hours: { median: number | null; mean: number | null };
    users_with_first_prompt: number;
  };
  engagement: {
    prompts_per_active_day_by_cohort: Array<{ cohort: string; avg_prompts_per_active_day: number }>;
    power_users_day0_pct: number | null;
    power_users_week0_pct: number | null;
    multi_day_ai_first_7d_pct: number | null;
  };
  retention: {
    overall_retention_pct: Record<string, number | null>;
    cohort_retention: Array<Record<string, string | number | null>>;
    wau_by_week: Array<{ week: string; wau: number; wow_pct?: number | null }>;
    churn_pct: Record<string, number | null>;
    session_frequency_by_week: Array<{ week: string; sessions_per_active_user: number }>;
  };
  monetization: Record<string, unknown>;
  feedback: Record<string, unknown>;
  validation: Record<string, unknown>;
};

function pct(v: number | null | undefined): string {
  return v == null ? "—" : `${v}%`;
}

export default function OasisBaselineReport() {
  const { tokens } = useHostTheme();
  const a = BASELINE.activation;
  const e = BASELINE.engagement;
  const r = BASELINE.retention;
  const m = BASELINE.monetization as {
    token_limit_hit_rate_pct?: number;
    premium_conversion_pct?: number | null;
    arpu_gross_usd?: number;
    arpu_net_usd?: number;
    total_revenue_usd?: number;
    estimated_api_cost_usd?: number;
    ltv_proxy_usd?: number;
    cac_ltv?: { note?: string };
    median_days_to_first_limit?: number | null;
    conversion_velocity_hours?: { median: number | null };
  };
  const f = BASELINE.feedback as {
    submission_rate_pct?: number;
    median_hours_to_first?: number | null;
    distribution?: Array<{ bucket: string; users: number }>;
    anomalies?: Array<{ user_id: string; minutes_after_signup: number }>;
    review_samples?: Array<{
      feedback_id: string;
      category: string;
      negative_rating: boolean | null;
      reported_at: string;
      tag: string;
    }>;
  };

  const activationCategories = Object.keys(a.activation_rate_pct);
  const activationValues = activationCategories.map(
    (k) => a.activation_rate_pct[k] ?? 0
  );

  const retentionCategories = ["D1", "D3", "D7", "D14", "D30"];
  const retentionValues = retentionCategories.map(
    (k) => r.overall_retention_pct[k] ?? 0
  );

  const wauWeeks = r.wau_by_week ?? [];
  const wauCategories = wauWeeks.map((w) => w.week);
  const wauValues = wauWeeks.map((w) => w.wau);

  const cohortRows = (r.cohort_retention ?? []).slice(-8);
  const cohortColumns = [
    { key: "cohort", header: "Signup week" },
    ...retentionCategories.map((d) => ({ key: d, header: d, align: "right" as const })),
  ];

  const feedbackDist = f.distribution ?? [];
  const feedbackCategories = feedbackDist.map((x) => x.bucket);
  const feedbackValues = feedbackDist.map((x) => x.users);

  const engagementCohorts = e.prompts_per_active_day_by_cohort ?? [];
  const engCategories = engagementCohorts.map((c) => c.cohort);
  const engValues = engagementCohorts.map((c) => c.avg_prompts_per_active_day);

  const sessionFreq = r.session_frequency_by_week ?? [];
  const sessCategories = sessionFreq.map((s) => s.week);
  const sessValues = sessionFreq.map((s) => s.sessions_per_active_user);

  return (
    <Stack gap={24} style={{ padding: 24, maxWidth: 960, color: tokens.text.primary }}>
      <Stack gap={8}>
        <H1>Oasis Baseline Report</H1>
        <Text tone="secondary">
          Snapshot {BASELINE.snapshot_date} · generated {BASELINE.generated_at} ·{" "}
          {BASELINE.total_users} users ({BASELINE.active_users} active)
        </Text>
        <Callout tone="warning">
          Early-stage sample — treat percentages as directional, not statistically stable.
        </Callout>
      </Stack>

      <CollapsibleSection title="Activation">
        <Stack gap={16}>
          <Text tone="secondary">
            Source: users.created_at + llm_usage first prompt · activation windows from signup
          </Text>
          <Grid columns={2} gap={12}>
            <Stat label="Median time to first prompt" value={`${a.time_to_first_hours.median ?? "—"} h`} />
            <Stat label="Mean time to first prompt" value={`${a.time_to_first_hours.mean ?? "—"} h`} />
          </Grid>
          {activationCategories.length > 0 && (
            <Card>
              <CardHeader title="AI activation rate (% new users with first prompt)" />
              <CardBody>
                <BarChart
                  categories={activationCategories}
                  series={[{ name: "Activation %", data: activationValues }]}
                  valueSuffix="%"
                  height={220}
                />
                <Text tone="secondary" style={{ marginTop: 8, fontSize: 12 }}>
                  Denominator: all users · {a.users_with_first_prompt} users have ≥1 prompt
                </Text>
              </CardBody>
            </Card>
          )}
        </Stack>
      </CollapsibleSection>

      <CollapsibleSection title="Engagement">
        <Stack gap={16}>
          <Grid columns={3} gap={12}>
            <Stat label="10+ prompts day 0" value={pct(e.power_users_day0_pct)} />
            <Stat label="10+ prompts week 0" value={pct(e.power_users_week0_pct)} />
            <Stat label="Multi-day AI (first 7d)" value={pct(e.multi_day_ai_first_7d_pct)} />
          </Grid>
          {engCategories.length > 0 && (
            <Card>
              <CardHeader title="Avg prompts per active day by signup cohort" />
              <CardBody>
                <BarChart
                  categories={engCategories}
                  series={[{ name: "Prompts / active day", data: engValues }]}
                  height={220}
                />
              </CardBody>
            </Card>
          )}
        </Stack>
      </CollapsibleSection>

      <CollapsibleSection title="Retention & churn">
        <Stack gap={16}>
          <Text tone="secondary">
            Return = session or llm_usage on calendar day signup+N
          </Text>
          {retentionValues.some((v) => v > 0) && (
            <Card>
              <CardHeader title="Overall retention (%)" />
              <CardBody>
                <BarChart
                  categories={retentionCategories}
                  series={[{ name: "Retention %", data: retentionValues }]}
                  valueSuffix="%"
                  height={220}
                />
              </CardBody>
            </Card>
          )}
          {cohortRows.length > 0 && (
            <Card>
              <CardHeader title="Retention by signup cohort (last 8 weeks)" />
              <CardBody padding={0}>
                <Table columns={cohortColumns} rows={cohortRows} />
              </CardBody>
            </Card>
          )}
          {wauCategories.length > 0 && (
            <Card>
              <CardHeader title="Weekly active users (WAU)" />
              <CardBody>
                <LineChart
                  categories={wauCategories}
                  series={[{ name: "WAU", data: wauValues, tone: "info" }]}
                  height={220}
                />
                <Text tone="secondary" style={{ marginTop: 8, fontSize: 12 }}>
                  Source: sessions ∪ llm_usage · last {wauCategories.length} weeks
                </Text>
              </CardBody>
            </Card>
          )}
          <Grid columns={3} gap={12}>
            <Stat label="Churn 7d" value={pct(r.churn_pct?.churn_7d_pct)} tone="danger" />
            <Stat label="Churn 14d" value={pct(r.churn_pct?.churn_14d_pct)} tone="danger" />
            <Stat label="Churn 30d" value={pct(r.churn_pct?.churn_30d_pct)} tone="danger" />
          </Grid>
          {sessCategories.length > 0 && (
            <Card>
              <CardHeader title="Sessions per active user per week" />
              <CardBody>
                <BarChart
                  categories={sessCategories}
                  series={[{ name: "Sessions / active user", data: sessValues }]}
                  height={200}
                />
              </CardBody>
            </Card>
          )}
        </Stack>
      </CollapsibleSection>

      <CollapsibleSection title="Monetization">
        <Stack gap={16}>
          <Grid columns={2} gap={12}>
            <Stat label="Token limit hit rate" value={pct(m.token_limit_hit_rate_pct)} />
            <Stat label="Premium conversion" value={pct(m.premium_conversion_pct)} tone="success" />
            <Stat label="ARPU (gross)" value={`$${m.arpu_gross_usd ?? "—"}`} />
            <Stat label="ARPU (net of API est.)" value={`$${m.arpu_net_usd ?? "—"}`} />
            <Stat label="Revenue (successful payments)" value={`$${m.total_revenue_usd ?? "—"}`} />
            <Stat label="Est. API cost" value={`$${m.estimated_api_cost_usd ?? "—"}`} />
          </Grid>
          <Callout tone="info">
            CAC/LTV ratio unavailable in DB. LTV proxy (12 mo): ${m.ltv_proxy_usd ?? "—"}.{" "}
            {m.cac_ltv?.note ?? ""}
          </Callout>
        </Stack>
      </CollapsibleSection>

      <CollapsibleSection title="Feedback">
        <Stack gap={16}>
          <Grid columns={2} gap={12}>
            <Stat label="Submission rate" value={pct(f.submission_rate_pct)} />
            <Stat label="Median hours to first feedback" value={`${f.median_hours_to_first ?? "—"} h`} />
          </Grid>
          {feedbackCategories.length > 0 && (
            <Card>
              <CardHeader title="Users by feedback submission count" />
              <CardBody>
                <BarChart
                  categories={feedbackCategories}
                  series={[{ name: "Users", data: feedbackValues }]}
                  height={200}
                />
              </CardBody>
            </Card>
          )}
          {(f.anomalies?.length ?? 0) > 0 && (
            <Card>
              <CardHeader title="Anomaly: feedback within 15 min of signup" />
              <CardBody padding={0}>
                <Table
                  columns={[
                    { key: "user_id", header: "User" },
                    { key: "minutes_after_signup", header: "Minutes", align: "right" },
                  ]}
                  rows={f.anomalies ?? []}
                />
              </CardBody>
            </Card>
          )}
          {(f.review_samples?.length ?? 0) > 0 && (
            <Card>
              <CardHeader title="Manual review samples" />
              <CardBody padding={0}>
                <Table
                  columns={[
                    { key: "feedback_id", header: "ID" },
                    { key: "category", header: "Category" },
                    { key: "negative_rating", header: "Negative" },
                    { key: "tag", header: "Tag" },
                  ]}
                  rows={f.review_samples ?? []}
                />
              </CardBody>
            </Card>
          )}
        </Stack>
      </CollapsibleSection>

      <CollapsibleSection title="Data limitations">
        <Stack gap={8}>
          {BASELINE.limitations.map((note) => (
            <Text key={note}>· {note}</Text>
          ))}
        </Stack>
      </CollapsibleSection>
    </Stack>
  );
}
