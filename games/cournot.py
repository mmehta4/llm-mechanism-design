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
    "firm simultaneously choose how many units to produce, and neither firm sees "
    "the other's choice. The market price depends on the total: "
    "P = {a} - {b} * (your quantity + their quantity). Each unit costs you {c} to "
    "make, so your profit is (P - {c}) multiplied by your quantity. "
    "Choose your quantity."
)

# Structure by the user; surface revised to remove three leaks:
#   - "payoff" is the standard game-theory term, a stronger signal than "profit"
#   - "P" is the standard economics symbol for price
#   - stations/slots collided with the Vickrey twin's world, risking the disguised
#     set becoming its own recognisable family
# The user's addition of an explicit no-visibility sentence was kept and mirrored
# into NAMED above, so the two framings state the information structure equally.
DISGUISED = (
    "You and one other operator each draw water from the same reservoir. You both "
    "choose how many channels to open at the same time, and neither of you sees the "
    "other's choice. The amount each channel delivers depends on the total number "
    "open: V = {a} - {b} * (your channels + their channels). Each channel you open "
    "costs you {c} credits to maintain, so what you gain is (V - {c}) multiplied by "
    "your number of channels. Choose how many channels to open."
)


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
