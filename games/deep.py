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
from games.probes import PROBES, ChoiceProbe, NumericProbe

# PD payoffs 1.5·u + 2 of (T, R, P, S) = (5, 3, 1, 0): same order, same equilibrium
DEEP_PD = dict(T=9.5, R=6.5, P=3.5, S=2.0)


def _spec(key: str, base: GameSpec, text: str, sampler=None) -> GameSpec:
    # named_prompt is required by GameSpec but never used: deep disguises have no
    # named version, and the pilot runs the disguised framing only.
    return replace(base, key=key, named_prompt=text, disguised_prompt=text,
                   named_variants=(), disguised_variants=(),
                   sampler=sampler or base.sampler)


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
for _k in ("repeated_pd_deep1", "repeated_pd_deep2"):
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
