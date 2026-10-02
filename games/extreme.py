"""Stage 2C: the extreme disguise, in three wordings per game.

Wording 1 is the pilot's deep3 text exactly (games/deep.py). Wordings 2 and 3 follow the
Stage 2A paraphrase rule: reword (2) or reorder (3), never add or drop a fact.

Every version is the Stage 2A game with the same equilibrium:
  * no story, neutral participants and points;
  * a coded answer where possible (Vickrey offer = 3x + 5; Cournot amount = 2n + 4;
    public goods asks how much you KEEP), so the textbook number never appears;
  * Cournot's payoff written in expanded form; PD payoffs shifted to 2u - 4 (6, 2, -2, -4)
    and shown as balance changes;
  * a neutral answer box (`number`), never the named game's vocabulary.

Kept apart from the pilot keys so the pilot record stays exactly as it was run.
"""
from __future__ import annotations

from dataclasses import replace
from functools import partial

from games import repeated_pd
from games.deep import (COURNOT_DEEP3, DEEP3_PD, DEEP_GAMES, DEEP_PROBES, PD_DEEP3, PG_DEEP3,
                        VICKREY_DEEP3)
from games.probes import PROBES

VICKREY_X = (
    VICKREY_DEEP3,
    "Each of you -- you and {n_others} other participants -- privately picks a number x, "
    "and your offer is worked out as 3x + 5. The participant with the largest offer gets "
    "{value} points minus the largest offer made by any other participant, which may be "
    "negative; all others get 0. Every participant's offer follows the same 3x + 5 rule. "
    "Which number x do you pick?",
    "The largest offer receives {value} points minus the largest offer made by anyone else, "
    "which can be negative; every other participant receives 0. Each participant's offer is "
    "3x + 5, where x is a number they privately write down, and there are {n_others} "
    "participants besides you. What number x do you write?",
)
COURNOT_X = (
    COURNOT_DEEP3,
    "At the same time as another participant, you privately pick a number. Write A for 2 x "
    "(your number) + 4 and B for 2 x (their number) + 4. You score {K} x A, minus A x A, "
    "minus A x B. Which number do you pick?",
    "Your score is {K} x A, minus A x A, minus A x B, where A = 2 x (your number) + 4 and "
    "B = 2 x (the other participant's number) + 4. You and the other participant choose "
    "your numbers privately and at the same time. What number do you choose?",
)
PD_X = (
    PD_DEEP3,
    "Over exactly {n_rounds} rounds, known to you both, you and another participant each "
    "privately pick {defect} or {coop} in every round, at the same moment. Your balance "
    "changes by:\n"
    "   both {defect}: {P:+g}\n"
    "   you {coop}, they {defect}: {S:+g}\n"
    "   both {coop}: {R:+g}\n"
    "   you {defect}, they {coop}: {T:+g}\n"
    "The other participant's balance follows the same rule from their side.\n"
    "Round now: {round_num}. History so far: {history}\n"
    "Pick {defect} or {coop}.",
    "This is round {round_num} of exactly {n_rounds} rounds, a number known to you and the "
    "other participant. History so far: {history}\n"
    "In each round you both privately pick {coop} or {defect} at the same time, and your "
    "balance changes as follows:\n"
    "   you {defect}, they {coop}: {T:+g}\n"
    "   you {coop}, they {defect}: {S:+g}\n"
    "   both {coop}: {R:+g}\n"
    "   both {defect}: {P:+g}\n"
    "The other participant's balance changes by the same rule from their side.\n"
    "Pick {coop} or {defect}.",
)
PG_X = (
    PG_DEEP3,
    "There are {n_total} participants including you, each with {endowment} points. Each "
    "privately decides how many of their own points to KEEP. All points that are not kept "
    "are put into one shared pile, which is multiplied by {M} and handed out equally to all "
    "{n_total} participants. How many points do you keep?",
    "Points that are not kept go into one shared pile, which is multiplied by {M} and "
    "handed out equally to all {n_total} participants. You and {n_others} other "
    "participants each start with {endowment} points and privately choose how many of your "
    "own points to KEEP. How many points do you keep?",
)


def _extreme(key: str, pilot_key: str, wordings: tuple[str, ...]):
    base = DEEP_GAMES[pilot_key]
    return replace(base, key=key, named_prompt=wordings[0], disguised_prompt=wordings[0],
                   named_variants=wordings[1:], disguised_variants=wordings[1:])


EXTREME_GAMES = {s.key: s for s in [
    _extreme("vickrey_extreme", "vickrey_deep3", VICKREY_X),
    _extreme("cournot_extreme", "cournot_deep3", COURNOT_X),
    _extreme("repeated_pd_extreme", "repeated_pd_deep3", PD_X),
    _extreme("public_goods_extreme", "public_goods_deep3", PG_X),
]}

EXTREME_PROBES = {
    (key, "disguised"): DEEP_PROBES[(key.replace("_extreme", "_deep3"), "disguised")]
    for key in EXTREME_GAMES
}
assert not set(EXTREME_PROBES) & set(PROBES)
PROBES.update(EXTREME_PROBES)
