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
#
# CORRECTED after the n=20 pilot: the original omitted "privately", so the named
# framing ("sealed-bid") conveyed that bids are secret and this one did not -- an
# information-structure difference, which the isomorphism rule forbids. It does
# not move the equilibrium (truthful bidding is dominant whether or not rival bids
# are visible) but a model could reason differently if it imagined them visible.
# Caught by tests/test_paraphrases.py. Pilot rows store the full prompt text, so
# trials run under the old wording remain identifiable.
DISGUISED = (
    "{n_total} research stations are requesting a processing slot. Each station "
    "privately submits one request number. The station with the highest request receives "
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


# --- Paraphrases --------------------------------------------------------------
# Index 0 is the primary prompt above. Variant 1 rewords in the same order;
# variant 2 leads with the private value. Same facts, same numbers, nothing added.
NAMED_VARIANTS = (
    "A single item is up for sealed-bid auction, with you and {n_others} other "
    "bidders taking part. The bidder with the highest bid wins, and pays the "
    "SECOND-highest bid submitted. The item is privately worth {value} tokens to "
    "you: winning at a price under {value} earns you the difference, and winning "
    "at a price over {value} costs you the difference. Enter your bid.",

    "Your private value for the single item on offer is {value} tokens. It is "
    "being sold by sealed-bid auction to you and {n_others} other bidders: the "
    "highest bid wins, and the winner pays the SECOND-highest bid submitted. If "
    "you win at a price below {value} you profit by the difference; if you win at "
    "a price above {value} you lose the difference. What is your bid?",
)

DISGUISED_VARIANTS = (
    "A processing slot is being allocated among {n_total} research stations, "
    "yours included. Every station privately submits a single request number. The slot goes "
    "to the station with the highest request, which is then charged the amount of "
    "the SECOND-highest request. To your station the slot is worth {value} "
    "credits: you gain the difference between {value} and the charge, and lose "
    "the difference if the charge is higher. Enter your request number.",

    "The processing slot is worth {value} credits to your station. It will go to "
    "whichever of the {n_total} research stations submits the highest request "
    "number, and that station is charged the amount of the SECOND-highest "
    "request. Each station privately submits exactly one request number. You gain the "
    "difference between {value} and what you are charged, and lose the "
    "difference if you are charged more. What request number do you submit?",
)


SPEC = GameSpec(
    key="vickrey",
    named_prompt=NAMED,
    disguised_prompt=DISGUISED,
    action_model=BidAction,
    equilibrium=vickrey.equilibrium_bid,
    sampler=sample,
    named_variants=NAMED_VARIANTS,
    disguised_variants=DISGUISED_VARIANTS,
)
