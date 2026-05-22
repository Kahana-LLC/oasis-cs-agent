"""CLI: fetch Supabase data, compute baseline metrics, write JSON + canvas."""

from __future__ import annotations

import json
import logging
import sys
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_PATH = ROOT / "reporting" / "baseline_snapshot.json"
# In-repo path (shows in Explorer); also mirrored for Cursor canvas preview.
REPO_CANVAS_PATH = ROOT / "canvases" / "oasis-baseline-report.canvas.tsx"
CURSOR_CANVAS_PATH = (
    Path.home()
    / ".cursor/projects/Users-adamkershner-Documents-CS-Agent-oasis-cs-agent/canvases/oasis-baseline-report.canvas.tsx"
)
CANVAS_PATH = REPO_CANVAS_PATH

CANVAS_TEMPLATE = '''import {
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

const BASELINE = __SNAPSHOT_JSON__ as BaselineData;

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
'''


def _write_canvas(snapshot: dict) -> None:
    payload = json.dumps(snapshot, indent=2)
    content = CANVAS_TEMPLATE.replace("__SNAPSHOT_JSON__", payload)
    for path in (REPO_CANVAS_PATH, CURSOR_CANVAS_PATH):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        log.info("canvas written: %s", path)


def run(canvas_only: bool = False) -> dict:
    if canvas_only:
        if not SNAPSHOT_PATH.exists():
            raise FileNotFoundError(f"Snapshot not found: {SNAPSHOT_PATH}")
        data = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
        _write_canvas(data)
        log.info("canvas regenerated from existing snapshot")
        return data  # type: ignore[return-value]
    from reporting.snapshot_service import build_snapshot

    snapshot = build_snapshot(today=date.today())
    data = snapshot.to_dict()
    SNAPSHOT_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
    log.info("snapshot written: %s", SNAPSHOT_PATH)

    _write_canvas(data)

    v = snapshot.validation
    log.info("validation: revenue=$%s limit_hit_days=%s plus_users=%s",
             v.get("payments_revenue_usd"), v.get("limit_hit_days"), v.get("plus_users"))
    log.info("View dashboard: .venv/bin/python main.py --baseline-view")

    return snapshot


def main() -> None:
    import argparse

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="Generate Oasis baseline metrics report")
    parser.add_argument(
        "--canvas-only",
        action="store_true",
        help="Regenerate canvas from existing baseline_snapshot.json",
    )
    args = parser.parse_args()
    try:
        run(canvas_only=args.canvas_only)
    except Exception:
        log.exception("baseline report failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
