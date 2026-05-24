"""Streamlit dashboard for Oasis baseline metrics (reads baseline_snapshot.json)."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

SNAPSHOT_PATH = Path(__file__).resolve().parent / "baseline_snapshot.json"
RETENTION_DAYS = ("D1", "D3", "D7", "D14", "D30")


@st.cache_data
def load_snapshot() -> dict:
    if not SNAPSHOT_PATH.exists():
        raise FileNotFoundError(
            f"Missing {SNAPSHOT_PATH}. Run: .venv/bin/python main.py --baseline"
        )
    return json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))


def _pct(v) -> str:
    return "—" if v is None else f"{v}%"


def main() -> None:
    st.set_page_config(page_title="Oasis Baseline Report", layout="wide")

    try:
        data = load_snapshot()
    except FileNotFoundError as e:
        st.error(str(e))
        st.stop()

    st.title("Oasis Baseline Report")
    st.caption(
        f"Snapshot {data.get('snapshot_date', '—')} · generated {data.get('generated_at', '—')} · "
        f"{data.get('total_users', 0)} users ({data.get('active_users', 0)} active)"
    )
    st.warning(
        "Early-stage sample — treat percentages as directional, not statistically stable."
    )

    with st.sidebar:
        st.header("Refresh data")
        st.code(".venv/bin/python main.py --baseline", language="bash")
        st.caption(
            "Run daily to populate `baseline_metric_history` in Supabase for KPI deltas."
        )
        if st.button("Rerun dashboard"):
            st.cache_data.clear()
            st.rerun()
        delta_period = st.radio(
            "Delta comparison",
            options=["daily", "weekly", "monthly"],
            format_func=lambda p: {"daily": "vs 1d ago", "weekly": "vs 7d ago", "monthly": "vs 30d ago"}[p],
            index=["daily", "weekly", "monthly"].index(
                st.session_state.get("delta_period", "weekly")
            ),
            key="delta_period",
        )

    tooltips = data.get("metric_tooltips") or {}

    def _help(key: str) -> str | None:
        t = tooltips.get(key)
        return t if t else None

    def _delta_str(metric_key: str) -> str | None:
        block = (data.get("deltas") or {}).get(delta_period) or {}
        if not block.get("available"):
            return None
        d = (block.get("metrics") or {}).get(metric_key)
        if not d or d.get("abs_change") is None:
            return None
        sign = "+" if d["abs_change"] > 0 else ""
        suffix = " pp" if "_pct" in metric_key or metric_key.startswith("flow_") else ""
        s = f"{sign}{d['abs_change']}{suffix}"
        if d.get("pct_change") is not None and not metric_key.startswith("flow_"):
            s += f" ({sign}{d['pct_change']}%)"
        return s

    insights = data.get("key_insights") or {}
    if insights.get("summary") or insights.get("items"):
        st.header("Key insights")
        st.caption("Churn & dead-user focus — levers for resurrection and at-risk recovery")
        st.info(insights.get("summary", ""))
        for item in insights.get("items", [])[:6]:
            sev = item.get("severity", "info")
            with st.expander(f"[{sev}] {item.get('title', 'Insight')}", expanded=(sev == "high")):
                st.write(item.get("detail", ""))
                st.markdown(f"**Lever:** {item.get('lever', '')}")

    deltas = data.get("deltas") or {}
    if not (deltas.get(delta_period) or {}).get("available"):
        st.caption(
            "KPI deltas appear after daily `main.py --baseline` runs populate history "
            "(7d for weekly, 30d for monthly)."
        )

    with st.expander("Data limitations"):
        for note in data.get("limitations", []):
            st.markdown(f"- {note}")

    # --- Launch KPIs ---
    launch = data.get("launch_kpis", {})
    if launch:
        st.header("Product Hunt Launch KPIs")
        st.caption(
            "At-a-glance scorecard mapped to Launch KPIs.txt · "
            "status: live (from DB), partial (proxy), manual (enter below)"
        )
        headlines = launch.get("headlines", {})
        h1, h2, h3, h4, h5, h6 = st.columns(6)
        h1.metric(
            "24h activation",
            _pct(headlines.get("activation_24h_pct")),
            delta=_delta_str("activation_24h_pct"),
            help=_help("activation_24h"),
        )
        h2.metric(
            "D7 retention",
            _pct(headlines.get("retention_d7_pct")),
            delta=_delta_str("retention_d7_pct"),
            help=_help("retention_d7"),
        )
        h3.metric(
            "Latest WAU",
            headlines.get("latest_wau", "—"),
            delta=_delta_str("latest_wau"),
            help=_help("latest_wau"),
        )
        h4.metric(
            "Premium conversion",
            _pct(headlines.get("premium_conversion_pct")),
            delta=_delta_str("premium_conversion_pct"),
            help=_help("premium_conversion"),
        )
        h5.metric(
            "Feedback rate",
            _pct(headlines.get("feedback_submission_rate_pct")),
            delta=_delta_str("feedback_submission_rate_pct"),
            help=_help("feedback_rate"),
        )
        arpu_net = headlines.get("arpu_net_usd")
        h6.metric(
            "Net ARPU",
            f"${arpu_net}" if arpu_net is not None else "—",
            delta=_delta_str("arpu_net_usd"),
            help=_help("arpu_net"),
        )

        kpi_rows = launch.get("kpi_rows", [])
        if kpi_rows:
            st.dataframe(pd.DataFrame(kpi_rows), use_container_width=True, hide_index=True)

    # --- DAU Model ---
    dau = data.get("dau_model", {})
    if dau:
        st.header("Daily Active Users Model")
        totals = dau.get("totals", {})
        st.caption(
            f"As of {dau.get('as_of', '—')} · flow rates = "
            f"{dau.get('flow_window_days', 7)}-day avg daily transitions"
        )
        c1, c2, c3 = st.columns(3)
        c1.metric("DAU", totals.get("dau", "—"), delta=_delta_str("dau"), help=_help("dau"))
        c2.metric("WAU", totals.get("wau", "—"), delta=_delta_str("wau"), help=_help("wau"))
        c3.metric("MAU", totals.get("mau", "—"), delta=_delta_str("mau"), help=_help("mau"))

        bucket_rows = dau.get("bucket_rows", [])
        if bucket_rows:
            cols = st.columns(4)
            defs = dau.get("definitions") or {}
            for i, row in enumerate(bucket_rows):
                key = row.get("key", "")
                cols[i % 4].metric(
                    row["bucket"],
                    f"{row['users']} ({row['pct_of_total']}%)",
                    delta=_delta_str(f"bucket_{key}") if key else None,
                    help=defs.get(key) or _help(f"bucket_{key}"),
                )
            df_buckets = pd.DataFrame(bucket_rows).set_index("bucket")[["users"]]
            st.subheader("User buckets")
            st.bar_chart(df_buckets)

        flow_rows = dau.get("flow_rate_rows", [])
        if flow_rows:
            st.subheader("Flow rates")
            st.dataframe(pd.DataFrame(flow_rows), use_container_width=True, hide_index=True)

    # --- Activation ---
    st.header("Activation")
    st.caption("Source: users.created_at + first llm_usage row · activation windows from signup")
    act = data.get("activation", {})
    ttf = act.get("time_to_first_hours", {})
    c1, c2, c3 = st.columns(3)
    c1.metric("Median time to first prompt", f"{ttf.get('median', '—')} h")
    c2.metric("Mean time to first prompt", f"{ttf.get('mean', '—')} h")
    c3.metric("Users with ≥1 prompt", act.get("users_with_first_prompt", "—"))

    rates = act.get("activation_rate_pct", {})
    if rates:
        df_act = pd.DataFrame(
            {"Activation %": [rates.get(k) for k in rates]},
            index=list(rates.keys()),
        )
        st.subheader("AI activation rate (% new users with first prompt)")
        st.bar_chart(df_act)
        st.caption(f"Denominator: all {act.get('total_users', data.get('total_users'))} users")

    # --- Engagement ---
    st.header("Engagement")
    eng = data.get("engagement", {})
    e1, e2, e3 = st.columns(3)
    e1.metric("10+ prompts (day 0)", _pct(eng.get("power_users_day0_pct")))
    e2.metric("10+ prompts (week 0)", _pct(eng.get("power_users_week0_pct")))
    e3.metric("Multi-day AI (first 7d)", _pct(eng.get("multi_day_ai_first_7d_pct")))

    cohorts = eng.get("prompts_per_active_day_by_cohort", [])
    if cohorts:
        recent = cohorts[-12:]
        df_eng = pd.DataFrame(recent).set_index("cohort")
        df_eng.columns = ["Avg prompts / active day"]
        st.subheader("Avg prompts per active day by signup cohort")
        st.bar_chart(df_eng)

    # --- Retention ---
    st.header("Retention & churn")
    st.caption("Return = session or llm_usage on calendar day signup+N")
    ret = data.get("retention", {})
    overall = ret.get("overall_retention_pct", {})
    if overall:
        df_ret = pd.DataFrame(
            {"Retention %": [overall.get(d) for d in RETENTION_DAYS]},
            index=list(RETENTION_DAYS),
        )
        st.subheader("Overall retention")
        st.bar_chart(df_ret)

    cohort_rows = ret.get("cohort_retention", [])
    if cohort_rows:
        st.subheader("Retention by signup cohort (last 8 weeks)")
        df_cohort = pd.DataFrame(cohort_rows[-8:]).set_index("cohort")
        st.dataframe(df_cohort, use_container_width=True)

    wau = ret.get("wau_by_week", [])
    if wau:
        df_wau = pd.DataFrame(wau).set_index("week")[["wau"]]
        st.subheader("Weekly active users (WAU)")
        st.line_chart(df_wau)
        st.caption("Source: sessions ∪ llm_usage")

    churn = ret.get("churn_pct", {})
    ch1, ch2, ch3 = st.columns(3)
    ch1.metric(
        "Churn 7d",
        _pct(churn.get("churn_7d_pct")),
        delta=_delta_str("churn_7d_pct"),
        help=_help("churn_7d"),
    )
    ch2.metric(
        "Churn 14d",
        _pct(churn.get("churn_14d_pct")),
        delta=_delta_str("churn_14d_pct"),
        help=_help("churn_14d"),
    )
    ch3.metric(
        "Churn 30d",
        _pct(churn.get("churn_30d_pct")),
        delta=_delta_str("churn_30d_pct"),
        help=_help("churn_30d"),
    )

    sess = ret.get("session_frequency_by_week", [])
    if sess:
        df_sess = pd.DataFrame(sess).set_index("week")
        st.subheader("Sessions per active user per week")
        st.bar_chart(df_sess)

    # --- Monetization ---
    st.header("Monetization")
    mon = data.get("monetization", {})
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric(
        "Token limit hit rate",
        _pct(mon.get("token_limit_hit_rate_pct")),
        delta=_delta_str("token_limit_hit_rate_pct"),
        help=_help("token_limit_hit_rate"),
    )
    m2.metric(
        "Premium conversion",
        _pct(mon.get("premium_conversion_pct")),
        delta=_delta_str("premium_conversion_pct"),
        help=_help("premium_conversion"),
    )
    m3.metric(
        "Limit-hitter conversion",
        _pct(mon.get("premium_conversion_among_limit_hitters_pct")),
        delta=_delta_str("limit_hitter_conversion_pct"),
        help=_help("limit_hitter_conversion"),
    )
    m4.metric("Median days to limit", mon.get("median_days_to_first_limit", "—"))
    m5.metric("Median hours to limit", mon.get("median_hours_to_first_limit", "—"))
    conv_vel = mon.get("conversion_velocity_hours") or {}
    m6.metric("Conversion velocity", f"{conv_vel.get('median', '—')} h")

    m7, m8, m9, m10, m11 = st.columns(5)
    m7.metric("ARPU (gross)", f"${mon.get('arpu_gross_usd', '—')}")
    m8.metric("ARPU (net of API est.)", f"${mon.get('arpu_net_usd', '—')}")
    m9.metric("Revenue (successful payments)", f"${mon.get('total_revenue_usd', '—')}")
    m10.metric("Est. API cost", f"${mon.get('estimated_api_cost_usd', '—')}")
    m11.metric("LTV proxy (12 mo)", f"${mon.get('ltv_proxy_usd', '—')}")

    launch = data.get("launch_kpis", {})
    forecast = launch.get("usage_cost_forecast", {})
    est_api = mon.get("estimated_api_cost_usd") or 0
    default_gemini = forecast.get("projected_monthly_cost_usd", est_api)
    default_supabase = launch.get("default_supabase_monthly_usd", 25)

    st.subheader("Costs & forecast")
    if "gemini_monthly_usd" not in st.session_state:
        st.session_state.gemini_monthly_usd = float(default_gemini)
    if "supabase_monthly_usd" not in st.session_state:
        st.session_state.supabase_monthly_usd = float(default_supabase)
    c1, c2 = st.columns(2)
    gemini_cost = c1.number_input(
        "Actual Gemini spend (USD/month)",
        min_value=0.0,
        step=0.01,
        key="gemini_monthly_usd",
    )
    supabase_cost = c2.number_input(
        "Supabase Pro (USD/month)",
        min_value=0.0,
        step=0.01,
        key="supabase_monthly_usd",
    )

    total_users = data.get("total_users") or 1
    revenue = mon.get("total_revenue_usd") or 0
    net_revenue = revenue - gemini_cost - supabase_cost
    net_arpu = net_revenue / total_users if total_users else 0
    ltv_adj = net_arpu * 12
    variance = ((gemini_cost - est_api) / est_api * 100) if est_api else None

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Net revenue (after costs)", f"${net_revenue:.2f}")
    r2.metric("Net ARPU (adjusted)", f"${net_arpu:.2f}")
    r3.metric("LTV proxy adjusted (12 mo)", f"${ltv_adj:.2f}")
    r4.metric("Gemini vs model variance", f"{variance:.1f}%" if variance is not None else "—")

    st.caption(
        f"7d prompts: {forecast.get('prompts_last_7d', '—')} · "
        f"est. cost ${forecast.get('estimated_cost_last_7d_usd', '—')} · "
        f"projected monthly ${forecast.get('projected_monthly_cost_usd', '—')} (model run-rate). "
        "Enter AI Studio actuals above."
    )

    cac = mon.get("cac_ltv", {})
    st.info(cac.get("note", "CAC/LTV ratio unavailable in DB."))

    hits = mon.get("limit_hits_by_lifecycle_day", [])
    if hits:
        st.subheader("Token limit hits by lifecycle day at hit")
        df_hits = pd.DataFrame(hits).set_index("lifecycle_day")
        hit_col = "hit_count" if "hit_count" in df_hits.columns else "users"
        st.bar_chart(df_hits[[hit_col]])

    # --- Feedback ---
    st.header("Feedback")
    fb = data.get("feedback", {})
    f1, f2 = st.columns(2)
    f1.metric("Submission rate", _pct(fb.get("submission_rate_pct")))
    f2.metric("Median hours to first feedback", f"{fb.get('median_hours_to_first', '—')} h")

    dist = fb.get("distribution", [])
    if dist:
        df_fb = pd.DataFrame(dist).set_index("bucket")[["users"]]
        st.subheader("Users by feedback submission count")
        st.bar_chart(df_fb)

    anomalies = fb.get("anomalies", [])
    if anomalies:
        st.subheader("Anomaly: feedback within 15 min of signup")
        st.dataframe(pd.DataFrame(anomalies), use_container_width=True, hide_index=True)

    samples = fb.get("review_samples", [])
    if samples:
        st.subheader("Manual review samples")
        st.dataframe(pd.DataFrame(samples), use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
