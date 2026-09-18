"""Cournot duopoly. Named framing written; disguised twin is YOURS to write."""
from __future__ import annotations

import random

from pydantic import BaseModel, Field

from games.base import GameSpec
from theory import cournot


class QuantityAction(BaseModel):
    quantity: float = Field(description="The quantity to produce.")
    reasoning: str = Field(description="One or two sentences explaining the quantity.")


NAMED = (
    "You are one of two firms producing an identical product. You and the other "
    "firm simultaneously choose how many units to produce. The market price "
    "depends on the total: P = {a} - {b} * (your quantity + their quantity). "
    "Each unit costs you {c} to make, so your profit is (P - {c}) multiplied by "
    "your quantity. Choose your quantity."
)

# TODO(you): write the disguised twin.
#   Strip: "firm", "produce", "market price", "profit", "units".
#   Keep:  a continuous non-negative quantity choice, the SAME a/b/c numbers,
#          two simultaneous deciders, the same linear price-fall structure.
#   Watch: the hard part is expressing "price falls linearly in total output"
#          without economic vocabulary, and WITHOUT adding a step where the
#          model must first work out that this is a quantity-setting problem.
#          State the payoff formula outright, exactly as the named version does.
DISGUISED = None


def sample(seed: int, a: float = 100.0, b: float = 1.0, c: float = 10.0) -> dict:
    rng = random.Random(seed)
    a_draw = round(rng.uniform(a * 0.8, a * 1.2), 1)
    return {
        "a": a_draw,
        "b": b,
        "c": c,
        "equilibrium": cournot.nash_quantity_symmetric(a_draw, b, c),
    }


SPEC = GameSpec(
    key="cournot",
    named_prompt=NAMED,
    disguised_prompt=DISGUISED,
    action_model=QuantityAction,
    equilibrium=cournot.nash_quantity_symmetric,
    sampler=sample,
)
