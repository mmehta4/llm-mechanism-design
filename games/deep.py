"""Stage 2C pilot: deeper disguises.

The Stage 2A disguises were seen through: Nemotron named the disguised game in 96-100%
of its Cournot and Vickrey answers. These are candidate DEEPER disguises, piloted on
practice questions only, to find a wording that hides the game without changing it.

Every version is the same game with the same equilibrium. Only how it is described
changes:

  deep1  REPHRASED RULE  the Stage 2A story, with every textbook signature replaced by an
                         equivalent statement:
                           Vickrey  "charged the second-highest request" ->
                                    "charged the largest request made by any OTHER station"
                                    (the same number whenever you win)
                           Cournot  the price formula written out in words
                           PD       the famous 5/3/1/0 payoffs replaced by 9.5/6.5/3.5/2
                                    (1.5 x + 2: an affine transform, the same game)
                           PG       "multiplied by M and divided evenly" ->
                                    "every unit turns into M units, spread evenly"
  deep2  ABSTRACT        no story at all: "you and another participant each choose...",
                         with the same rephrased rules

Only the disguised framing exists here; there is no "named" version of a deep disguise.
"""
from __future__ import annotations

from dataclasses import replace
from functools import partial

from games import cournot, public_goods, repeated_pd, vickrey
from games.base import GameSpec
from pydantic import BaseModel, Field

from games.probes import PROBES, ChoiceProbe, NumericProbe

# PD payoffs 1.5·u + 2 of (T, R, P, S) = (5, 3, 1, 0): same order, same equilibrium
DEEP_PD = dict(T=9.5, R=6.5, P=3.5, S=2.0)


class NumberAction(BaseModel):
    """A NEUTRAL answer box. The Stage 2A boxes carried the named game's vocabulary into
    the disguised questions ("bid: The sealed bid to submit", "quantity: The quantity to
    produce", "contribution: How much of your endowment to contribute"), and a model
    writes the field name as it answers. Every deep version uses this instead."""
    number: float = Field(description="The number you choose.")
    reasoning: str = Field(description="One or two sentences explaining the number.")


def _spec(key: str, base: GameSpec, text: str, sampler=None, neutral: bool = True) -> GameSpec:
    # named_prompt is required by GameSpec but never used: deep disguises have no
    # named version, and the pilot runs the disguised framing only.
    model = base.action_model
    if neutral and base.key != "repeated_pd":       # the PD box is already neutral
        model = NumberAction
    return replace(base, key=key, named_prompt=text, disguised_prompt=text,
                   named_variants=(), disguised_variants=(),
                   sampler=sampler or base.sampler, action_model=model)


VICKREY_DEEP1 = (
    "{n_total} research stations are requesting a processing slot. Each station privately "
    "submits one request number. The station with the highest request receives the slot, "
    "and is charged the largest request number submitted by any of the other stations. "
    "The slot is worth {value} credits to your station -- you gain the difference between "
    "{value} and what you are charged, and lose the difference if you are charged more. "
    "Submit your request number."
)
VICKREY_DEEP2 = (
    "You and {n_others} other participants each privately write down one number. Whoever "
    "writes the largest number receives {value} points minus the largest number written by "
    "anyone else -- which can be negative. Everyone else receives nothing. What number do "
    "you write?"
)
COURNOT_DEEP1 = (
    "You and one other operator each draw water from the same reservoir. You both choose "
    "how many channels to open at the same time, and neither of you sees the other's "
    "choice. Each channel you open delivers {a} credits, minus {b} credit for every channel "
    "open in total, yours and theirs together, and costs you {c} credits to keep running. "
    "Choose how many channels to open."
)
COURNOT_DEEP2 = (
    "You and another participant each privately choose an amount at the same time. Your "
    "score is your amount multiplied by: {a}, minus {b} times the two amounts added "
    "together, minus {c}. What amount do you choose?"
)
PD_DEEP2 = (
    "You and another participant take part in exactly {n_rounds} rounds, a number known to "
    "you both. In each round you both privately choose {coop} or {defect} at the same time. "
    "Your points for a round:\n"
    "   {R} if you both choose {coop}\n"
    "   {P} if you both choose {defect}\n"
    "   {T} if you choose {defect} and they choose {coop}\n"
    "   {S} if you choose {coop} and they choose {defect}\n"
    "The other participant's points follow the same rule from their side.\n"
    "This is round {round_num}. History so far: {history}\n"
    "Choose {coop} or {defect}."
)
PG_DEEP1 = (
    "You and {n_others} other operators each hold {endowment} units of signal. Each of you "
    "privately decides how many units to route into a central amplifier. Every unit routed "
    "in, by anyone, turns into {M} units, which are spread evenly across all {n_total} "
    "operators. You keep whatever you did not route in. How many units do you route in?"
)
PG_DEEP2 = (
    "You and {n_others} other participants each start with {endowment} points. Each of you "
    "privately chooses how many of your points to place in a shared box. Every point placed "
    "in the box, by anyone, becomes {M} points, divided equally among all {n_total} "
    "participants. You keep the points you did not place. How many points do you place?"
)

# --- deep3: EXTREME. No story; the answer is a coded number so the textbook value never
# appears; payoffs written out in expanded form; PD payoffs shifted to include negatives;
# public goods asks how much you KEEP. Same games, same equilibria.
VICKREY_DEEP3 = (
    "You and {n_others} other participants each privately write down a number x. Your "
    "offer is 3x + 5. Whoever has the largest offer receives {value} points minus the "
    "largest offer made by anyone else, which can be negative; everyone else receives 0. "
    "Every participant's offer is worked out the same way from their own number. What "
    "number x do you write?"
)
COURNOT_DEEP3 = (
    "You and another participant each privately choose a number at the same time. Let A = "
    "2 x (your number) + 4 and B = 2 x (their number) + 4. Your score is {K} x A, minus A "
    "x A, minus A x B. What number do you choose?"
)
PD_DEEP3 = (
    "You and another participant take part in exactly {n_rounds} rounds, a number known to "
    "you both. In each round you both privately pick {coop} or {defect} at the same time, "
    "and your balance changes as follows:\n"
    "   you {defect}, they {coop}: {T:+g}\n"
    "   you {coop}, they {defect}: {S:+g}\n"
    "   both {coop}: {R:+g}\n"
    "   both {defect}: {P:+g}\n"
    "The other participant's balance changes by the same rule from their side.\n"
    "This is round {round_num}. History so far: {history}\n"
    "Pick {coop} or {defect}."
)
PG_DEEP3 = (
    "You and {n_others} other participants each start with {endowment} points. Each of you "
    "privately chooses how many of your points to KEEP. Every point not kept goes into one "
    "shared pile; the pile is then multiplied by {M} and handed out equally to all "
    "{n_total} participants. How many points do you keep?"
)
DEEP3_PD = dict(T=6.0, R=2.0, P=-2.0, S=-4.0)        # 2u - 4 of (5, 3, 1, 0)


def _vickrey3_sample(seed: int) -> dict:
    p = vickrey.sample(seed)
    p["equilibrium"] = (p["value"] - 5) / 3          # offer = value  =>  x = (v - 5) / 3
    return p


def _cournot3_sample(seed: int) -> dict:
    p = cournot.sample(seed)
    p["K"] = round(p["a"] - p["c"], 1)                # b = 1: score = A (K - A - B)
    p["equilibrium"] = (p["K"] / 3 - 4) / 2          # A* = K/3  =>  number = (A* - 4) / 2
    return p


def _pg3_sample(seed: int) -> dict:
    p = public_goods.sample(seed)
    p["equilibrium"] = p["endowment"] - p["equilibrium"]   # keep = endowment - contribution
    return p


_pd_sampler = partial(repeated_pd.sample, **DEEP_PD)

DEEP_GAMES = {s.key: s for s in [
    _spec("vickrey_deep1", vickrey.SPEC, VICKREY_DEEP1),
    _spec("vickrey_deep2", vickrey.SPEC, VICKREY_DEEP2),
    _spec("cournot_deep1", cournot.SPEC, COURNOT_DEEP1),
    _spec("cournot_deep2", cournot.SPEC, COURNOT_DEEP2),
    _spec("repeated_pd_deep1", repeated_pd.SPEC, repeated_pd.DISGUISED, _pd_sampler),
    _spec("repeated_pd_deep2", repeated_pd.SPEC, PD_DEEP2, _pd_sampler),
    _spec("public_goods_deep1", public_goods.SPEC, PG_DEEP1),
    _spec("public_goods_deep2", public_goods.SPEC, PG_DEEP2),
    # the Stage 2A disguised wording, word for word, with only the neutral answer box:
    # measures how much the leaky box alone drove recognition
    _spec("vickrey_neutralbox", vickrey.SPEC, vickrey.DISGUISED),
    _spec("cournot_neutralbox", cournot.SPEC, cournot.DISGUISED),
    _spec("public_goods_neutralbox", public_goods.SPEC, public_goods.DISGUISED),
    _spec("vickrey_deep3", vickrey.SPEC, VICKREY_DEEP3, _vickrey3_sample),
    _spec("cournot_deep3", cournot.SPEC, COURNOT_DEEP3, _cournot3_sample),
    _spec("repeated_pd_deep3", repeated_pd.SPEC, PD_DEEP3, partial(repeated_pd.sample, **DEEP3_PD)),
    _spec("public_goods_deep3", public_goods.SPEC, PG_DEEP3, _pg3_sample),
]}

# maths checks in each version's own words
DEEP_PROBES = {
    ("vickrey_deep1", "disguised"): (
        "Research stations request a processing slot. The station with the highest request "
        "receives the slot and is charged the largest request made by any of the other "
        "stations. The slot is worth 50 credits to your station and you request 50. The "
        "largest request among the other stations is 60. What is your net result?",
        NumericProbe, lambda **_: 0.0),
    ("vickrey_deep2", "disguised"): (
        "Participants each write down one number. Whoever writes the largest number receives "
        "50 points minus the largest number written by anyone else; everyone else receives "
        "nothing. You write 50, and the largest number written by anyone else is 60. How many "
        "points do you receive?",
        NumericProbe, lambda **_: 0.0),
    ("cournot_deep1", "disguised"): (
        "Two operators draw from one reservoir. Each channel delivers 100 credits minus 1 "
        "credit for every channel open in total, and costs 10 credits to keep running. The "
        "other operator opens 30 channels. How many channels maximise what YOU gain?",
        NumericProbe, lambda **_: 30.0),
    ("cournot_deep2", "disguised"): (
        "Your score is your amount multiplied by: 100, minus 1 times the two amounts added "
        "together, minus 10. The other participant chooses 30. Which amount maximises YOUR "
        "score?",
        NumericProbe, lambda **_: 30.0),
    ("public_goods_deep1", "disguised"): (
        "Four operators each hold 20 units. Every unit routed into the amplifier, by anyone, "
        "turns into 2 units spread evenly across all four. If you route exactly 1 more unit, "
        "how much of that comes back to you?",
        NumericProbe, lambda **_: 0.5),
    ("public_goods_deep2", "disguised"): (
        "Four participants each start with 20 points. Every point placed in the shared box, "
        "by anyone, becomes 2 points divided equally among all four. If you place exactly 1 "
        "more point, how much of it comes back to you?",
        NumericProbe, lambda **_: 0.5),
}
DEEP_PROBES.update({
    ("vickrey_neutralbox", "disguised"): PROBES[("vickrey", "disguised")],
    ("cournot_neutralbox", "disguised"): PROBES[("cournot", "disguised")],
    ("public_goods_neutralbox", "disguised"): PROBES[("public_goods", "disguised")],
    ("vickrey_deep3", "disguised"): (
        "Each participant writes a number x and their offer is 3x + 5. Whoever has the "
        "largest offer receives 70 points minus the largest offer made by anyone else. You "
        "write 20, so your offer is 65, and the largest offer by anyone else is 50. How many "
        "points do you receive?",
        NumericProbe, lambda **_: 20.0),
    ("cournot_deep3", "disguised"): (
        "Let A = 2 x (your number) + 4 and B = 2 x (their number) + 4. Your score is 90 x A, "
        "minus A x A, minus A x B. The other participant chooses 13, so B = 30. Which number "
        "maximises YOUR score?",
        NumericProbe, lambda **_: 13.0),        # best A = (90 - 30) / 2 = 30  =>  (30 - 4) / 2
    ("public_goods_deep3", "disguised"): (
        "Four participants each start with 20 points and choose how many to keep. Points not "
        "kept go into a shared pile, which is multiplied by 2 and handed out equally to all "
        "four. If you keep exactly 1 point fewer, by how much does your own final total "
        "change? (Give a negative number for a loss.)",
        NumericProbe, lambda **_: -0.5),
})
for _k in ("repeated_pd_deep1", "repeated_pd_deep2", "repeated_pd_deep3"):
    DEEP_PROBES[(_k, "disguised")] = (
        "Two participants simultaneously choose {coop} or {defect}. Your own points:\n"
        "  you choose {coop}, they choose {coop}  ->  you get {R:g}\n"
        "  you choose {defect}, they choose {coop}  ->  you get {T:g}\n"
        "  you choose {coop}, they choose {defect}  ->  you get {S:g}\n"
        "  you choose {defect}, they choose {defect}  ->  you get {P:g}\n"
        "Consider ONE round in isolation. They choose {coop}. Which of your two choices gives "
        "you more? Reply with the single letter only.",
        ChoiceProbe, lambda defect="Y", **_: defect)

assert not set(DEEP_PROBES) & set(PROBES)
PROBES.update(DEEP_PROBES)
