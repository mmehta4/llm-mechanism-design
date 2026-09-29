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
    """Labels are counterbalanced per trial, so this cannot be a static Literal.
    Validate the returned string against the trial's own two labels."""
    action: str = Field(description="The option chosen, exactly as labelled in the prompt.")
    reasoning: str = Field(description="One or two sentences explaining the choice.")


NAMED = (
    "You are playing a game with one other player for exactly {n_rounds} rounds, "
    "known to both of you. Each round you both simultaneously choose C or D.\n"
    "  If you both choose C, you each score {R}.\n"
    "  If you both choose D, you each score {P}.\n"
    "  If you choose D and they choose C, you score {T} and they score {S}.\n"
    "  If you choose C and they choose D, you score {S} and they score {T}.\n"
    "This is round {round_num}. History so far: {history}\n"
    "Choose C or D."
)

# Written by the user. Passed review; two changes made, neither to the substance.
#
# X/Y is the right call: maximally neutral labels, with the four-line payoff table
# doing all the work. Nothing in "technician", "control panel", "position" or
# "receive units" hints which option is the generous one -- which was the entire
# difficulty here, since "cooperate"/"defect" leak through moral weight rather than
# through nouns.
#
# The user's "known to both of you" was BETTER than the named version's bare "for 10
# rounds", and it matters more here than anywhere else in the project: backward
# induction requires the horizon to be COMMON KNOWLEDGE, not merely known. Mirrored
# into NAMED above rather than removed from here.
#
# Added: the cooperative option was always X and always listed first. Labels are now
# seeded and counterbalanced (see sample()), so half of all trials assign the
# cooperative action to Y instead.
DISGUISED = (
    "You and one other technician each operate a control panel for a session of "
    "exactly {n_rounds} rounds, known to both of you. Each round, you both "
    "simultaneously set your panel to position {coop} or position {defect}.\n"
    "   If you both set {coop}, you each receive {R} units.\n"
    "   If you both set {defect}, you each receive {P} units.\n"
    "   If you set {defect} and they set {coop}, you receive {T} units and they receive {S}.\n"
    "   If you set {coop} and they set {defect}, you receive {S} units and they receive {T}.\n"
    "This is round {round_num}. History so far: {history}\n"
    "Set your panel to {coop} or {defect}."
)


def sample(seed: int, n_rounds: int = 10) -> dict:
    """Counterbalances which letter denotes the cooperative action.

    Without this, the cooperative option is always X and always listed first, so a
    first-listed-is-default bias and any latent letter association would both ride
    along with the treatment.
    """
    rng = random.Random(seed)
    T, R, P, S = 5.0, 3.0, 1.0, 0.0
    coop, defect = ("X", "Y") if rng.random() < 0.5 else ("Y", "X")
    return {
        "n_rounds": n_rounds,
        "T": T, "R": R, "P": P, "S": S,
        "round_num": 1,
        "history": "none yet",
        "coop": coop,
        "defect": defect,
        "delta_min": repeated_pd.min_discount_factor(T, R, P, S),
        # finite KNOWN horizon -> backward induction -> defect from round one
        "equilibrium": defect,
        "equilibrium_named": "D",
        "_seed": rng.random(),
    }


# --- Paraphrases --------------------------------------------------------------
# Index 0 is the primary prompt above. Variant 1 LISTS THE DEFECTING OPTION FIRST;
# variant 2 leads with the round and history. Both mirrored across framings.
#
# Variant 1 has a second job. Label counterbalancing in sample() randomises which
# LETTER means cooperate, but the primary prompt always LISTS the cooperative
# option first -- so a first-listed-is-default bias would survive counterbalancing.
# Flipping the order here puts that bias in the data where it can be measured.
NAMED_VARIANTS = (
    "You and one other player will play exactly {n_rounds} rounds, a number "
    "known to both of you. In every round you each choose D or C simultaneously.\n"
    "  If you both choose D, you each score {P}.\n"
    "  If you both choose C, you each score {R}.\n"
    "  If you choose C and they choose D, you score {S} and they score {T}.\n"
    "  If you choose D and they choose C, you score {T} and they score {S}.\n"
    "Current round: {round_num}. History so far: {history}\n"
    "Choose D or C.",

    "This is round {round_num} of a game lasting exactly {n_rounds} rounds, a "
    "length known to both you and the other player. History so far: {history}\n"
    "Each round, you both simultaneously choose C or D, and score as follows:\n"
    "  If you both choose C, you each score {R}.\n"
    "  If you both choose D, you each score {P}.\n"
    "  If you choose D and they choose C, you score {T} and they score {S}.\n"
    "  If you choose C and they choose D, you score {S} and they score {T}.\n"
    "Choose C or D.",
)

DISGUISED_VARIANTS = (
    "You and one other technician run control panels for a session of exactly "
    "{n_rounds} rounds, a number known to both of you. In every round you both "
    "simultaneously set your panel to position {defect} or position {coop}.\n"
    "   If you both set {defect}, you each receive {P} units.\n"
    "   If you both set {coop}, you each receive {R} units.\n"
    "   If you set {coop} and they set {defect}, you receive {S} units and they receive {T}.\n"
    "   If you set {defect} and they set {coop}, you receive {T} units and they receive {S}.\n"
    "Current round: {round_num}. History so far: {history}\n"
    "Set your panel to {defect} or {coop}.",

    "This is round {round_num} of a session lasting exactly {n_rounds} rounds, a "
    "length known to both you and the other technician. History so far: {history}\n"
    "Each round, you both simultaneously set your control panel to position "
    "{coop} or position {defect}, and receive units as follows:\n"
    "   If you both set {coop}, you each receive {R} units.\n"
    "   If you both set {defect}, you each receive {P} units.\n"
    "   If you set {defect} and they set {coop}, you receive {T} units and they receive {S}.\n"
    "   If you set {coop} and they set {defect}, you receive {S} units and they receive {T}.\n"
    "Set your panel to {coop} or {defect}.",
)


SPEC = GameSpec(
    key="repeated_pd",
    named_prompt=NAMED,
    disguised_prompt=DISGUISED,
    action_model=PDAction,
    equilibrium=lambda **_: "D",
    sampler=sample,
    named_variants=NAMED_VARIANTS,
    disguised_variants=DISGUISED_VARIANTS,
)
