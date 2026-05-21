from models.actions import TriggerResult
from models.metrics import UserMetrics, UserSegment


# ---------------------------------------------------------------------------
# Day 0 — Onboarding
# ---------------------------------------------------------------------------

def _day_0_welcome(m: UserMetrics) -> bool:
    # Wide window: day 0 or 1 so a missed first-run doesn't lose the welcome
    return m.lifecycle_day <= 1


def _day_0_guided_modal(m: UserMetrics) -> bool:
    # Stub — requires product layer to detect no-command-success in session
    return False


# ---------------------------------------------------------------------------
# Day 1–7 — Early Exploration
# ---------------------------------------------------------------------------

def _day_3_checkin(m: UserMetrics) -> bool:
    return 3 <= m.lifecycle_day <= 4 and m.session_count < 2


def _day_5_nudge(m: UserMetrics) -> bool:
    return 5 <= m.lifecycle_day <= 6 and m.session_count == 1


def _day_7_no_commands(m: UserMetrics) -> bool:
    # Logged in (sessions exist) but never ran a command — silent drop-off
    return 5 <= m.lifecycle_day <= 8 and m.session_count >= 1 and m.total_commands == 0


def _day_7_highvalue_flag(m: UserMetrics) -> bool:
    return (
        7 <= m.lifecycle_day <= 8
        and (m.session_count >= 4 or m.command_diversity >= 3)
    )


def _day_7_no_session(m: UserMetrics) -> bool:
    return 7 <= m.lifecycle_day <= 8 and m.session_count == 0


# ---------------------------------------------------------------------------
# Day 8–14 — Value Confirmation
# ---------------------------------------------------------------------------

def _day_10_email(m: UserMetrics) -> bool:
    return 10 <= m.lifecycle_day <= 11 and m.session_count in {2, 3}


def _day_12_survey(m: UserMetrics) -> bool:
    # Floor of 3 on prev week prevents firing on noise (e.g. 1 → 0 requests)
    return (
        12 <= m.lifecycle_day <= 13
        and m.weekly_requests_prev >= 3
        and m.weekly_requests < m.weekly_requests_prev
    )


def _day_14_at_risk(m: UserMetrics) -> bool:
    return 14 <= m.lifecycle_day <= 15 and m.segment == UserSegment.at_risk


# ---------------------------------------------------------------------------
# Day 15–30 — Habit Formation
# ---------------------------------------------------------------------------

def _day_21_diversity(m: UserMetrics) -> bool:
    if m.total_commands == 0 or m.dominant_command_type is None:
        return False
    dominant_count = m.command_type_breakdown.get(m.dominant_command_type, 0)
    return (
        21 <= m.lifecycle_day <= 22
        and dominant_count / m.total_commands > 0.70
    )


def _day_28_community(m: UserMetrics) -> bool:
    return 28 <= m.lifecycle_day <= 29 and m.session_count >= 5


def _day_30_milestone(m: UserMetrics) -> bool:
    return 30 <= m.lifecycle_day <= 31 and m.segment == UserSegment.healthy


def _day_30_inactive(m: UserMetrics) -> bool:
    return 30 <= m.lifecycle_day <= 31 and m.segment == UserSegment.inactive


# ---------------------------------------------------------------------------
# Day 31–60 — Engagement Deepening
# ---------------------------------------------------------------------------

def _day_45_winback(m: UserMetrics) -> bool:
    return 45 <= m.lifecycle_day <= 46 and 10 <= m.session_gap <= 14


def _day_55_founder(m: UserMetrics) -> bool:
    return (
        55 <= m.lifecycle_day <= 56
        and m.company_domain
        and m.session_count >= 8
    )


def _day_60_winback(m: UserMetrics) -> bool:
    return 60 <= m.lifecycle_day <= 61 and m.segment == UserSegment.inactive


# ---------------------------------------------------------------------------
# Day 61–90 — Retention & Expansion
# ---------------------------------------------------------------------------

def _day_75_referral(m: UserMetrics) -> bool:
    # Stub — referral system not built yet
    return False


def _day_85_enterprise(m: UserMetrics) -> bool:
    return (
        85 <= m.lifecycle_day <= 86
        and m.company_domain
        and m.session_count >= 10
    )


def _day_90_churn(m: UserMetrics) -> bool:
    return 90 <= m.lifecycle_day <= 91 and m.segment == UserSegment.inactive


# ---------------------------------------------------------------------------
# Ongoing — Fire Any Time
# ---------------------------------------------------------------------------

def _ongoing_dropoff(m: UserMetrics) -> bool:
    # Guard weekly_requests_prev > 0: if there was no prior activity there
    # is no baseline to call a dropoff against
    return (
        m.lifecycle_day > 7
        and m.session_count >= 2
        and m.weekly_requests_prev > 0
        and m.weekly_requests < m.weekly_requests_prev * 0.5
    )


def _ongoing_gap_14d(m: UserMetrics) -> bool:
    # Mutually exclusive with gap_21d by lifecycle_day range
    return 14 <= m.lifecycle_day <= 60 and m.session_gap > 14


def _ongoing_gap_21d(m: UserMetrics) -> bool:
    return m.lifecycle_day > 60 and m.session_gap > 21


def _ongoing_healthy_nudge(m: UserMetrics) -> bool:
    # NOTE: Phase 4 outreach log must check was_triggered within 14 days,
    # not all-time — otherwise this fires every single day for healthy users.
    return m.segment == UserSegment.healthy


def _ongoing_upgrade_nudge(m: UserMetrics) -> bool:
    # Free users showing strong engagement are primed for a Plus upgrade pitch
    return (
        m.plan_id == "Free"
        and m.weekly_requests >= 5
        and m.total_tokens_used >= 50_000
    )


# ---------------------------------------------------------------------------
# Registry
# Each entry: (check_fn, trigger_name, channels)
# Order matters only for readability — all triggers are evaluated independently.
# ---------------------------------------------------------------------------

_TRIGGERS: list[tuple] = [
    (_day_0_welcome,         "day_0_welcome",         ["in_app"]),
    (_day_0_guided_modal,    "day_0_guided_modal",    ["in_app"]),
    (_day_3_checkin,         "day_3_checkin",         ["email"]),
    (_day_5_nudge,           "day_5_nudge",           ["in_app"]),
    (_day_7_no_commands,     "day_7_no_commands",     ["email"]),
    (_day_7_highvalue_flag,  "day_7_highvalue_flag",  ["in_app", "email"]),
    (_day_7_no_session,      "day_7_no_session",      ["alert"]),
    (_day_10_email,          "day_10_email",          ["email"]),
    (_day_12_survey,         "day_12_survey",         ["in_app"]),
    (_day_14_at_risk,        "day_14_at_risk",        ["email"]),
    (_day_21_diversity,      "day_21_diversity",      ["email", "in_app"]),
    (_day_28_community,      "day_28_community",      ["email"]),
    (_day_30_milestone,      "day_30_milestone",      ["email"]),
    (_day_30_inactive,       "day_30_inactive",       ["email"]),
    (_day_45_winback,        "day_45_winback",        ["email"]),
    (_day_55_founder,        "day_55_founder",        ["alert"]),
    (_day_60_winback,        "day_60_winback",        ["email"]),
    (_day_75_referral,       "day_75_referral",       ["email"]),
    (_day_85_enterprise,     "day_85_enterprise",     ["alert"]),
    (_day_90_churn,          "day_90_churn",          ["email", "alert"]),
    (_ongoing_dropoff,       "ongoing_dropoff",       ["in_app", "email"]),
    (_ongoing_gap_14d,       "ongoing_gap_14d",       ["email"]),
    (_ongoing_gap_21d,       "ongoing_gap_21d",       ["email"]),
    (_ongoing_healthy_nudge, "ongoing_healthy_nudge", ["in_app", "alert"]),
    (_ongoing_upgrade_nudge, "ongoing_upgrade_nudge", ["email"]),
]


def evaluate_triggers(m: UserMetrics) -> list[TriggerResult]:
    """Return one TriggerResult per (fired trigger, channel) pair."""
    fired: list[TriggerResult] = []
    for fn, name, channels in _TRIGGERS:
        if fn(m):
            for ch in channels:
                fired.append(TriggerResult(trigger_name=name, channel=ch))
    return fired
