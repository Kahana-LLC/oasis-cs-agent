import logging
from datetime import date
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)


def main() -> None:
    from db.fetch import fetch_users, fetch_sessions, fetch_usage, fetch_daily_usage, fetch_feedback
    from pipeline.metrics import compute_metrics

    today = date.today()

    users = fetch_users()
    log.info(f"users: {len(users)}")

    sessions = fetch_sessions()
    log.info(f"sessions: {len(sessions)}")

    usage = fetch_usage()
    log.info(f"llm_usage rows: {len(usage)}")

    daily = fetch_daily_usage()
    log.info(f"llm_daily_usage rows: {len(daily)}")

    feedback = fetch_feedback()
    log.info(f"feedback_events rows: {len(feedback)}")

    from classifier.segment import classify_segment
    from collections import Counter

    all_metrics = []
    for u in users:
        m = compute_metrics(u, sessions, usage, daily, feedback, today)
        m.segment = classify_segment(m)
        all_metrics.append(m)
    log.info(f"metrics + segments computed: {len(all_metrics)}")

    # Segment distribution
    counts = Counter(str(m.segment.value) if m.segment else "none" for m in all_metrics)
    for seg, n in sorted(counts.items()):
        log.info(f"  {seg}: {n}")

    # One representative sample per segment (first match)
    seen = set()
    log.info("--- sample per segment ---")
    for m in all_metrics:
        key = m.segment.value if m.segment else "none"
        if key not in seen:
            seen.add(key)
            log.info(
                f"  [{key}] day={m.lifecycle_day} sessions={m.session_count} "
                f"gap={m.session_gap}d active_7d={m.active_days_last_7} "
                f"active_total={m.active_days_total} cmds={m.total_commands} "
                f"company={m.company_domain} neg_fb={m.has_recent_negative_feedback}"
            )


if __name__ == "__main__":
    main()
