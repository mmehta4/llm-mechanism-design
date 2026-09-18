"""Second-price sealed-bid auction. Named and disguised framings.

This module carries the WORKED EXAMPLE of a disguised twin. Use it as the
pattern for the other three.
"""
from __future__ import annotations

import random

from pydantic import BaseModel, Field

from games.base import GameSpec
from theory import vickrey


class BidAction(BaseModel):
    bid: float = Field(description="The sealed bid to submit.")
    reasoning: str = Field(description="One or two sentences explaining the bid.")


NAMED = (
    "You are bidding in a sealed-bid auction for a single item against "
    "{n_others} other bidders. The highest bidder wins and pays the "
    "SECOND-highest bid submitted. Your private value for the item is "
    "{value} tokens -- winning at a price below that value profits you the "
    "difference, and winning above it loses you the difference. Submit your bid."
)

# --- the worked example ------------------------------------------------------
# Check it against the criteria in games/base.py:
#   same action (a single number)      same magnitude (the value carries over)
#   same number of other agents        same rule (second-highest is charged)
#   no auction vocabulary anywhere     comparable length
#   equilibrium identical: request exactly your value
# Crucially it STATES the rule outright rather than expecting the model to
# recognise the format -- so no inference step has been added.
DISGUISED = (
    "{n_total} research stations are requesting a processing slot. Each station "
    "submits one request number. The station with the highest request receives "
    "the slot, and is charged the amount of the SECOND-highest request. The slot "
    "is worth {value} credits to your station -- you gain the difference between "
    "{value} and what you are charged, and lose the difference if you are charged "
    "more. Submit your request number."
)


def sample(seed: int, n_others: int = 2, value_range: tuple[float, float] = (10.0, 100.0)) -> dict:
    rng = random.Random(seed)
    value = round(rng.uniform(*value_range), 1)
    return {
        "value": value,
        "n_others": n_others,
        "n_total": n_others + 1,
        "equilibrium": vickrey.equilibrium_bid(value),
    }


SPEC = GameSpec(
    key="vickrey",
    named_prompt=NAMED,
    disguised_prompt=DISGUISED,
    action_model=BidAction,
    equilibrium=vickrey.equilibrium_bid,
    sampler=sample,
)
