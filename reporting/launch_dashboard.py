"""Launch the Streamlit baseline dashboard in the default browser."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_SCRIPT = ROOT / "reporting" / "dashboard.py"
SNAPSHOT_PATH = ROOT / "reporting" / "baseline_snapshot.json"


def launch() -> int:
    if not SNAPSHOT_PATH.exists():
        print(
            f"Missing {SNAPSHOT_PATH}\n"
            "Run first: .venv/bin/python main.py --baseline",
            file=sys.stderr,
        )
        return 1

    print("Opening dashboard at http://localhost:8501")
    print("Press Ctrl+C to stop the server.")
    env = os.environ.copy()
    env["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    return subprocess.call(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(DASHBOARD_SCRIPT),
            "--server.headless",
            "false",
            "--server.showEmailPrompt",
            "false",
        ],
        cwd=str(ROOT),
        env=env,
    )


if __name__ == "__main__":
    raise SystemExit(launch())
