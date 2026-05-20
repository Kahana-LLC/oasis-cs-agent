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

    all_metrics = [
        compute_metrics(u, sessions, usage, daily, feedback, today)
        for u in users
    ]
    log.info(f"metrics computed: {len(all_metrics)}")

    # Sample: log the first 3 users for a sanity check
    for m in all_metrics[:3]:
        log.info(
            f"  user={m.user_id} day={m.lifecycle_day} "
            f"sessions={m.session_count} gap={m.session_gap}d "
            f"active_7d={m.active_days_last_7} cmds={m.total_commands} "
            f"diversity={m.command_diversity} dominant={m.dominant_command_type} "
            f"tokens={m.total_tokens_used} plan={m.plan_id} "
            f"company={m.company_domain} neg_fb={m.has_recent_negative_feedback}"
        )


if __name__ == "__main__":
    main()
