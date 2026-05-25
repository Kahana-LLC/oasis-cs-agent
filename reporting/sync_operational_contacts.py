#!/usr/bin/env python3
"""Sync active Oasis users to operational email audience (CSV + optional Resend)."""

from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "data" / "operational_contacts.csv"


def load_active_users() -> list[dict[str, str]]:
    try:
        from db.fetch import fetch_all_users
    except ImportError as exc:
        raise SystemExit(f"db.fetch unavailable: {exc}") from exc

    rows: list[dict[str, str]] = []
    for user in fetch_all_users():
        status = getattr(user, "status", None) or ""
        email = (getattr(user, "email", None) or "").strip()
        if status != "active" or not email or "@" not in email:
            continue
        name = (getattr(user, "name", None) or getattr(user, "full_name", None) or "").strip()
        first = name.split()[0] if name else "there"
        rows.append(
            {
                "email": email,
                "first_name": first,
                "user_id": str(getattr(user, "user_id", "") or ""),
            }
        )
    return rows


def write_csv(users: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["email", "first_name", "user_id"])
        writer.writeheader()
        writer.writerows(users)
    print(f"Wrote {len(users)} contacts -> {path}")


def sync_resend_audience(users: list[dict[str, str]], *, audience_id: str) -> int:
    """Optional Resend audience sync when RESEND_API_KEY is configured."""
    api_key = os.environ.get("RESEND_API_KEY", "").strip()
    if not api_key:
        print("RESEND_API_KEY not set — skipped Resend sync")
        return 0
    try:
        import resend  # type: ignore
    except ImportError:
        print("Install resend package to sync: uv add resend")
        return 0

    resend.api_key = api_key
    synced = 0
    for u in users:
        try:
            resend.Contacts.create(
                {
                    "email": u["email"],
                    "first_name": u["first_name"],
                    "audience_id": audience_id,
                    "unsubscribed": False,
                }
            )
            synced += 1
        except Exception as err:
            print(f"Resend skip {u['email']}: {err}")
    print(f"Resend audience {audience_id}: synced {synced}/{len(users)}")
    return synced


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync operational email contacts")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="CSV output path")
    parser.add_argument(
        "--resend-audience-id",
        default=os.environ.get("RESEND_OPERATIONAL_AUDIENCE_ID", ""),
        help="Resend audience ID for oasis-operational-all",
    )
    args = parser.parse_args()

    users = load_active_users()
    if not users:
        print("No active users found")
        return
    write_csv(users, args.out)
    if args.resend_audience_id:
        sync_resend_audience(users, audience_id=args.resend_audience_id)


if __name__ == "__main__":
    main()
