"""Estimated API cost per model for net ARPU calculations."""

from models.db import LLMUsage

# USD per 1M tokens (input, output) — conservative estimates for baseline reporting
_MODEL_RATES: dict[str, tuple[float, float]] = {
    "gemini-2.5-flash": (0.15, 0.60),
    "text:gemini-1.5-flash": (0.075, 0.30),
    "voice:gemini-1.5-flash": (0.075, 0.30),
    "assist-router": (0.10, 0.40),
}
_DEFAULT_RATE = (0.10, 0.40)


def estimate_usage_cost_usd(row: LLMUsage) -> float:
    """Estimate marginal API cost for a single llm_usage row."""
    model = (row.model_used or "").strip()
    input_rate, output_rate = _MODEL_RATES.get(model, _DEFAULT_RATE)

    inp = row.input_tokens or 0
    out = row.output_tokens or 0
    if inp == 0 and out == 0 and row.total_tokens:
        inp = int(row.total_tokens * 0.7)
        out = int(row.total_tokens * 0.3)

    return (inp * input_rate + out * output_rate) / 1_000_000


def total_api_cost_usd(usage: list[LLMUsage]) -> float:
    return sum(estimate_usage_cost_usd(u) for u in usage)
