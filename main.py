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
    from triggers.evaluate import evaluate_triggers
    from collections import Counter

    all_metrics = []
    for u in users:
        m = compute_metrics(u, sessions, usage, daily, feedback, today)
        m.segment = classify_segment(m)
        all_metrics.append(m)
    log.info(f"metrics + segments computed: {len(all_metrics)}")

    # Segment distribution
    seg_counts = Counter(m.segment.value if m.segment else "none" for m in all_metrics)
    log.info("--- segment distribution ---")
    for seg, n in sorted(seg_counts.items()):
        log.info(f"  {seg}: {n}")

    # Trigger frequency across all users
    trigger_counts: Counter = Counter()
    total_fired = 0
    for m in all_metrics:
        results = evaluate_triggers(m)
        for r in results:
            trigger_counts[f"{r.trigger_name}/{r.channel}"] += 1
        total_fired += len(results)

    log.info(f"--- triggers fired: {total_fired} total across {len(all_metrics)} users ---")
    for key, n in sorted(trigger_counts.items(), key=lambda x: -x[1]):
        log.info(f"  {key}: {n}")


if __name__ == "__main__":
    main()
