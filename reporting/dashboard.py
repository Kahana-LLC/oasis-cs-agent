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
        st.caption("Then use **Rerun** above or refresh the browser.")
        if st.button("Rerun dashboard"):
            st.cache_data.clear()
            st.rerun()

    with st.expander("Data limitations"):
        for note in data.get("limitations", []):
            st.markdown(f"- {note}")

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
    ch1.metric("Churn 7d", _pct(churn.get("churn_7d_pct")))
    ch2.metric("Churn 14d", _pct(churn.get("churn_14d_pct")))
    ch3.metric("Churn 30d", _pct(churn.get("churn_30d_pct")))

    sess = ret.get("session_frequency_by_week", [])
    if sess:
        df_sess = pd.DataFrame(sess).set_index("week")
        st.subheader("Sessions per active user per week")
        st.bar_chart(df_sess)

    # --- Monetization ---
    st.header("Monetization")
    mon = data.get("monetization", {})
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Token limit hit rate", _pct(mon.get("token_limit_hit_rate_pct")))
    m2.metric("Premium conversion", _pct(mon.get("premium_conversion_pct")))
    m3.metric("ARPU (gross)", f"${mon.get('arpu_gross_usd', '—')}")
    m4.metric("ARPU (net of API est.)", f"${mon.get('arpu_net_usd', '—')}")

    m5, m6, m7 = st.columns(3)
    m5.metric("Revenue (successful payments)", f"${mon.get('total_revenue_usd', '—')}")
    m6.metric("Est. API cost", f"${mon.get('estimated_api_cost_usd', '—')}")
    m7.metric("LTV proxy (12 mo)", f"${mon.get('ltv_proxy_usd', '—')}")

    cac = mon.get("cac_ltv", {})
    st.info(cac.get("note", "CAC/LTV ratio unavailable in DB."))

    hits = mon.get("limit_hits_by_lifecycle_day", [])
    if hits:
        st.subheader("Token limit hits by lifecycle day at hit")
        st.bar_chart(pd.DataFrame(hits).set_index("lifecycle_day"))

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
