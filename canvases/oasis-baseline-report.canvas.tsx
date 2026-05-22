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
  "generated_at": "2026-05-21T22:03:12.784184Z",
  "snapshot_date": "2026-05-21",
  "total_users": 122,
  "active_users": 122,
  "limitations": [
    "Small sample size (122 users) \u2014 percentages are directional.",
    "First AI command inferred from llm_usage.timestamp (no first_command_at column).",
    "Token limits inferred from llm_daily_usage vs plan limits, not UX events.",
    "NULL plan_id treated as Free (121/122 users historically).",
    "CAC unavailable \u2014 user_acquisition and events tables empty.",
    "Feedback quality requires manual review of sampled rows."
  ],
  "activation": {
    "total_users": 122,
    "users_with_first_prompt": 71,
    "activation_rate_pct": {
      "1h": 27.9,
      "24h": 32.0,
      "3d": 33.6,
      "7d": 38.5
    },
    "time_to_first_hours": {
      "median": 5.07,
      "mean": 415.88
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
        "avg_prompts_per_active_day": 33.56
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
        "avg_prompts_per_active_day": 3.41
      },
      {
        "cohort": "2025-12-29/2026-01-04",
        "avg_prompts_per_active_day": 8.17
      },
      {
        "cohort": "2026-01-05/2026-01-11",
        "avg_prompts_per_active_day": 9.64
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
        "avg_prompts_per_active_day": 9.7
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
        "cohort": "2026-05-04/2026-05-10",
        "avg_prompts_per_active_day": 37.0
      },
      {
        "cohort": "2026-05-11/2026-05-17",
        "avg_prompts_per_active_day": 2.5
      },
      {
        "cohort": "2026-05-18/2026-05-24",
        "avg_prompts_per_active_day": 3.0
      }
    ],
    "power_users_day0_pct": 7.4,
    "power_users_week0_pct": 13.9,
    "multi_day_ai_first_7d_pct": 12.3
  },
  "retention": {
    "overall_retention_pct": {
      "D1": 10.7,
      "D3": 4.2,
      "D7": 11.9,
      "D14": 4.4,
      "D30": 2.8
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
        "D30": null
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
        "cohort": "2026-05-04/2026-05-10",
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
        "D7": 25.0,
        "D14": null,
        "D30": null
      },
      {
        "cohort": "2026-05-18/2026-05-24",
        "D1": 50.0,
        "D3": null,
        "D7": null,
        "D14": null,
        "D30": null
      }
    ],
    "wau_by_week": [
      {
        "week": "2026-03-02/2026-03-08",
        "week_start": "2026-03-02",
        "wau": 16,
        "wow_pct": null
      },
      {
        "week": "2026-03-09/2026-03-15",
        "week_start": "2026-03-09",
        "wau": 7,
        "wow_pct": -56.2
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
        "wau": 10,
        "wow_pct": 42.9
      },
      {
        "week": "2026-05-11/2026-05-17",
        "week_start": "2026-05-11",
        "wau": 15,
        "wow_pct": 50.0
      },
      {
        "week": "2026-05-18/2026-05-24",
        "week_start": "2026-05-18",
        "wau": 16,
        "wow_pct": 6.7
      }
    ],
    "churn_pct": {
      "churn_7d_pct": 75.3,
      "churn_14d_pct": 71.2,
      "churn_30d_pct": 60.3
    },
    "session_frequency_by_week": [
      {
        "week": "2025-10-20/2025-10-26",
        "sessions_per_active_user": 55.5
      },
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
        "sessions_per_active_user": 31.6
      },
      {
        "week": "2026-05-11/2026-05-17",
        "sessions_per_active_user": 16.2
      },
      {
        "week": "2026-05-18/2026-05-24",
        "sessions_per_active_user": 8.94
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
    "premium_conversion_pct": 8.2,
    "premium_users": 10,
    "conversion_velocity_hours": {
      "median": 486.7,
      "mean": 1127.8
    },
    "arpu_gross_usd": 1.34,
    "arpu_net_usd": 1.34,
    "total_revenue_usd": 164.0,
    "estimated_api_cost_usd": 0.37,
    "ltv_proxy_usd": 16.08,
    "cac_ltv": {
      "cac_available": false,
      "ltv_proxy_usd": 16.08,
      "note": "user_acquisition and events tables empty \u2014 provide marketing spend externally"
    }
  },
  "feedback": {
    "submission_rate_pct": 24.6,
    "median_hours_to_first": 622.45,
    "distribution": [
      {
        "bucket": "0",
        "users": 92
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
        "users": 6
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
  "validation": {
    "payments_success_count": 14,
    "payments_revenue_usd": 164.0,
    "limit_hit_days": 2,
    "plus_users": 10
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
