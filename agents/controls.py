"""Control agents — the scale against which LLM deviation is read.

"Deviation of -8" means nothing on its own. These two make it interpretable:

    RandomAgent     what pure chance looks like on this game
    HeuristicAgent  what a crude rule of thumb looks like

If an LLM sits between them, that is a very different paper from one where it sits
beyond random. Distinct from the scripted *theoretical* agent used as an OPPONENT --
these exist purely as comparison baselines.
"""
from __future__ import annotations

import random

from agents.base import AgentResponse


class RandomAgent:
    """Uniform over the action space."""

    model_api_id = "control:random"

    def __init__(self, seed: int = 0):
        self.rng = random.Random(seed)

    def act_numeric(self, low: float, high: float) -> AgentResponse:
        value = self.rng.uniform(low, high)
        return AgentResponse(
            action=value, reasoning="uniform random", raw="", parse_ok=True,
            latency_s=0.0, model_api_id=self.model_api_id,
        )

    def act_discrete(self, options: list[str]) -> AgentResponse:
        choice = self.rng.choice(options)
        return AgentResponse(
            action=choice, reasoning="uniform random", raw="", parse_ok=True,
            latency_s=0.0, model_api_id=self.model_api_id,
        )


class HeuristicAgent:
    """A fixed fractional rule -- e.g. always shade to 90% of the equilibrium.

    Crude on purpose. The question it answers is whether an LLM is doing anything
    more sophisticated than a constant multiplicative bias.
    """

    def __init__(self, fraction: float = 0.9):
        self.fraction = fraction
        self.model_api_id = f"control:heuristic_{fraction}"

    def act_numeric(self, anchor: float) -> AgentResponse:
        return AgentResponse(
            action=anchor * self.fraction,
            reasoning=f"fixed rule: {self.fraction} x anchor",
            raw="", parse_ok=True, latency_s=0.0, model_api_id=self.model_api_id,
        )
