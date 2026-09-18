"""Repeated Prisoner's Dilemma. Named framing written; disguised twin is YOURS.

This is the HARDEST twin of the four, by a distance. "Cooperate" and "defect"
carry such strong moral valence that most substitutes smuggle it straight back
in -- "share" versus "hoard" still tells the model which option is the nice one.
You want two labels with no moral colour at all.
"""
from __future__ import annotations

import random
from typing import Literal

from pydantic import BaseModel, Field

from games.base import GameSpec
from theory import repeated_pd


class PDAction(BaseModel):
    action: Literal["C", "D"] = Field(description="C to cooperate, D to defect.")
    reasoning: str = Field(description="One or two sentences explaining the choice.")


NAMED = (
    "You are playing a game with one other player for {n_rounds} rounds. "
    "Each round you both simultaneously choose C or D.\n"
    "  If you both choose C, you each score {R}.\n"
    "  If you both choose D, you each score {P}.\n"
    "  If you choose D and they choose C, you score {T} and they score {S}.\n"
    "  If you choose C and they choose D, you score {S} and they score {T}.\n"
    "This is round {round_num}. History so far: {history}\n"
    "Choose C or D."
)

# TODO(you): write the disguised twin.
#   Strip: any word implying one option is generous, fair, honest or nice.
#   Keep:  two discrete options, the SAME four payoff numbers, the same round
#          count and the same history format.
#   Watch: neutral labels are the whole difficulty. Consider options that are
#          purely mechanical -- two settings on a device, two routes, two
#          allocations -- where neither carries social meaning. Test your
#          wording on yourself: if you can tell which one is "nice", so can
#          the model, and the disguise has failed.
DISGUISED = None


def sample(seed: int, n_rounds: int = 10) -> dict:
    rng = random.Random(seed)
    T, R, P, S = 5.0, 3.0, 1.0, 0.0
    return {
        "n_rounds": n_rounds,
        "T": T, "R": R, "P": P, "S": S,
        "round_num": 1,
        "history": "none yet",
        "delta_min": repeated_pd.min_discount_factor(T, R, P, S),
        "equilibrium": "D",          # finite known horizon -> defect throughout
        "_seed": rng.random(),
    }


SPEC = GameSpec(
    key="repeated_pd",
    named_prompt=NAMED,
    disguised_prompt=DISGUISED,
    action_model=PDAction,
    equilibrium=lambda **_: "D",
    sampler=sample,
)
