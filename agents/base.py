"""What an agent returns from one decision.

Every field here exists because something downstream needs it:

    latency_s     -> Stage 1 multiplies this out to size the whole experiment
    parse_ok      -> reported as a RATE, never silently dropped. A condition that
                     produces many unparseable responses is itself a finding.
    raw           -> the audit trail, and in practice the most interesting
                     qualitative material in the project (Stage 3.5)
    model_api_id  -> providers deprecate and silently update models; a result that
                     cannot name its subject cannot be rechecked
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentResponse:
    action: Any | None
    reasoning: str
    raw: str
    latency_s: float
    parse_ok: bool
    model_api_id: str
    error: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    extra: dict = field(default_factory=dict)
