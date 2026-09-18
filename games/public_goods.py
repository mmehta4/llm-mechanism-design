"""Public goods game. Named framing written; disguised twin is YOURS to write."""
from __future__ import annotations

import random

from pydantic import BaseModel, Field

from games.base import GameSpec
from theory import public_goods


class ContributionAction(BaseModel):
    contribution: float = Field(description="How much of your endowment to contribute.")
    reasoning: str = Field(description="One or two sentences explaining the amount.")


NAMED = (
    "You and {n_others} other players each start with {endowment} tokens. "
    "Each of you privately chooses how much to contribute to a common pot. "
    "The total pot is multiplied by {M} and then split equally among all "
    "{n_total} players, regardless of who contributed what. You keep whatever "
    "you did not contribute. How much do you contribute?"
)

# TODO(you): write the disguised twin.
#   Strip: "contribute", "common pot", "players", "share" -- all of it signals
#          a cooperation frame before the model has done any reasoning.
#   Keep:  a continuous choice in [0, endowment], the SAME endowment and
#          multiplier, the same group size, and the equal-split rule.
#   Watch: this one is easy to make TOO neutral and end up ambiguous. The
#          model must still be able to see exactly what it keeps and exactly
#          what comes back to it. State the arithmetic outright.
DISGUISED = None


def sample(seed: int, n_others: int = 3, endowment: float = 20.0, M: float = 2.0) -> dict:
    rng = random.Random(seed)
    n_total = n_others + 1
    return {
        "n_others": n_others,
        "n_total": n_total,
        "endowment": endowment,
        "M": M,
        "equilibrium": public_goods.nash_contribution(endowment, M, n_total),
        "social_optimum": public_goods.social_optimum(endowment, M, n_total),
        "_seed": rng.random(),
    }


SPEC = GameSpec(
    key="public_goods",
    named_prompt=NAMED,
    disguised_prompt=DISGUISED,
    action_model=ContributionAction,
    equilibrium=public_goods.nash_contribution,
    sampler=sample,
)
