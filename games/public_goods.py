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

# Written by the user. Passed review unchanged.
#   numbers, bound, multiplier and group size all carry over; the multiply-then-split
#   rule and the "you keep what you held back" clause are both stated outright, which
#   is what lets the model compute the -0.5 marginal return; "route" is purely
#   mechanical and carries none of the generosity that "contribute" smuggles in; and
#   the operators/signal/amplifier world does not collide with the Vickrey or Cournot
#   twins.
#
# Noted but not corrected: neither framing states the [0, endowment] bound explicitly,
# both merely imply it. That is symmetric, so it does not bias delta-lambda -- but a
# model can return an out-of-range action, so `is_valid_action` below flags rather
# than clamps. The invalid rate is itself a finding.
DISGUISED = (
    "You and {n_others} other operators each hold {endowment} units of signal. "
    "Each of you privately chooses how many units to route into a central "
    "amplifier. The total routed in is multiplied by {M} and then divided evenly "
    "among all {n_total} operators, regardless of how much each one routed in. "
    "You keep whatever you did not route in. How many units do you route in?"
)


def is_valid_action(contribution: float, endowment: float) -> bool:
    """An action outside [0, endowment] is impossible, not merely unusual.

    Flagged rather than clamped: clamping would silently convert a comprehension
    failure into a data point at the boundary, which is exactly the kind of quiet
    corruption that survives every downstream check.
    """
    return 0.0 <= contribution <= endowment


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


# --- Paraphrases --------------------------------------------------------------
# Index 0 is the primary prompt above. Variant 1 rewords in the same order;
# variant 2 leads with the retention rule. Same facts, same numbers, nothing added.
NAMED_VARIANTS = (
    "There are {n_total} players, including you, and each begins with "
    "{endowment} tokens. Each of you privately decides how much to contribute to "
    "a common pot. Whatever is in the pot is multiplied by {M} and then split "
    "equally among all {n_total} players, regardless of who contributed what. You "
    "keep whatever you did not contribute. How much do you contribute?",

    "You keep whatever you do not contribute out of your {endowment} tokens. You "
    "and {n_others} other players each privately choose how much to contribute to "
    "a common pot; the total pot is multiplied by {M} and then split equally among "
    "all {n_total} players, regardless of who contributed what. How much do you "
    "contribute?",
)

DISGUISED_VARIANTS = (
    "There are {n_total} operators, including you, and each holds {endowment} "
    "units of signal. Each of you privately decides how many units to route into "
    "a central amplifier. Whatever is routed in is multiplied by {M} and then "
    "divided evenly among all {n_total} operators, regardless of how much each one "
    "routed in. You keep whatever you did not route in. How many units do you "
    "route in?",

    "You keep whatever you do not route in out of your {endowment} units of "
    "signal. You and {n_others} other operators each privately choose how many "
    "units to route into a central amplifier; the total routed in is multiplied by "
    "{M} and then divided evenly among all {n_total} operators, regardless of how "
    "much each one routed in. How many units do you route in?",
)


SPEC = GameSpec(
    key="public_goods",
    named_prompt=NAMED,
    disguised_prompt=DISGUISED,
    action_model=ContributionAction,
    equilibrium=public_goods.nash_contribution,
    sampler=sample,
    named_variants=NAMED_VARIANTS,
    disguised_variants=DISGUISED_VARIANTS,
)
