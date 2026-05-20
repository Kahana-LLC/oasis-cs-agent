import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)


def main() -> None:
    from db.fetch import fetch_users, fetch_sessions, fetch_usage, fetch_daily_usage

    users = fetch_users()
    log.info(f"users: {len(users)}")

    sessions = fetch_sessions()
    log.info(f"sessions: {len(sessions)}")

    usage = fetch_usage()
    log.info(f"llm_usage rows: {len(usage)}")

    daily = fetch_daily_usage()
    log.info(f"llm_daily_usage rows: {len(daily)}")


if __name__ == "__main__":
    main()
