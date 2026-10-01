"""Stage 2B games: traps, number sweeps and the PD endgame.

Kept apart from ALL_GAMES on purpose. ALL_GAMES is the registered Stage 2A set and
tests/test_stage2a_frozen.py pins every one of its questions; nothing here may touch
them.

Every Stage 2B game is an existing, already-approved game with one thing changed:

    TRAPS (Block B)   the numbers or one rule make the textbook answer wrong
    SWEEP (Block C)   the ordinary game at three sizes
    ENDGAME (Block E) the repeated PD asked at a late round after mutual cooperation

Where a trap needs new wording (Cournot's third firm, Vickrey's doubled payment), the
text is written out in full below rather than generated, so it can be read and
checked against the approved Stage 0 twin line by line.
"""
from __future__ import annotations

from dataclasses import replace
from functools import partial

from games import cournot, public_goods, repeated_pd, vickrey
from games.base import GameSpec
from games.probes import PROBES, ChoiceProbe, NumericProbe
from theory import cournot as cournot_theory
from theory import vickrey as vickrey_theory

# =============================================================================
# Block B -- traps
# =============================================================================

# --- Public goods: multiplier above the group size ---------------------------
# M = 5 with 4 players: each token put in returns 5/4 = 1.25 to its owner, so
# contributing everything is dominant. Same wording as Stage 2A; only M changes.
PG_TRAP = replace(
    public_goods.SPEC, key="public_goods_trap",
    sampler=partial(public_goods.sample, M=5.0),
)

# --- Prisoner's dilemma payoffs turned into a harmony game -------------------
# R > T and S > P, so cooperating is best against BOTH opponent choices. Same
# wording as Stage 2A; only the four payoffs change.
HARMONY = dict(T=3.0, R=5.0, P=1.0, S=2.0)
PD_TRAP = replace(
    repeated_pd.SPEC, key="repeated_pd_trap",
    sampler=partial(repeated_pd.sample, **HARMONY),
)

# --- Cournot with three firms -----------------------------------------------
# Correct: (a - c) / 4b. The duopoly formula (a - c) / 3b is the trap.
COURNOT3_NAMED = (
    "You are one of three firms producing an identical product. You and the other "
    "two firms simultaneously choose how many units to produce, and no firm sees "
    "the others' choices. The market price depends on the total: "
    "P = {a} - {b} * (your quantity + the other two firms' quantities). Each unit "
    "costs you {c} to make, so your profit is (P - {c}) multiplied by your "
    "quantity. Choose your quantity."
)
COURNOT3_DISGUISED = (
    "You and two other operators each draw water from the same reservoir. You all "
    "choose how many channels to open at the same time, and none of you sees the "
    "others' choices. The amount each channel delivers depends on the total number "
    "open: V = {a} - {b} * (your channels + the other two operators' channels). "
    "Each channel you open costs you {c} credits to maintain, so what you gain is "
    "(V - {c}) multiplied by your number of channels. Choose how many channels to "
    "open."
)
COURNOT3_NAMED_VARIANTS = (
    "Three firms, you and two rivals, make an identical product. Each of you "
    "decides how many units to produce at the same time, and no firm sees the "
    "others' choices. The market price is set by total output: "
    "P = {a} - {b} * (your quantity + the other two firms' quantities). Every unit "
    "costs you {c} to make, so your profit equals (P - {c}) times your quantity. "
    "How many units do you produce?",

    "Your profit is (P - {c}) multiplied by your quantity, where {c} is what each "
    "unit costs you to make and P is the market price. You and two other firms "
    "sell an identical product, and the market price depends on the total: "
    "P = {a} - {b} * (your quantity + the other two firms' quantities). All three "
    "firms choose quantities simultaneously, and no firm sees the others' choices. "
    "Choose your quantity.",
)
COURNOT3_DISGUISED_VARIANTS = (
    "Three operators, you and two others, draw water from the same reservoir. Each "
    "of you decides how many channels to open at the same moment, and none of you "
    "sees the others' choices. How much each channel delivers depends on the total "
    "number open: V = {a} - {b} * (your channels + the other two operators' "
    "channels). Each channel you open costs you {c} credits to maintain, so what "
    "you gain is (V - {c}) times your number of channels. How many channels do you "
    "open?",

    "What you gain is (V - {c}) multiplied by your number of channels, where {c} "
    "credits is what each channel you open costs to maintain and V is the amount "
    "each channel delivers. You and two other operators draw water from the same "
    "reservoir, so V = {a} - {b} * (your channels + the other two operators' "
    "channels). All three of you choose at the same time, and none of you sees the "
    "others' choices. Choose how many channels to open.",
)


def _cournot3_sample(seed: int) -> dict:
    params = cournot.sample(seed)
    params["n_firms"] = 3
    params["equilibrium"] = cournot_theory.nash_quantity_symmetric_n(
        params["a"], params["b"], params["c"], 3)
    return params


COURNOT_TRAP = GameSpec(
    key="cournot_trap",
    named_prompt=COURNOT3_NAMED,
    disguised_prompt=COURNOT3_DISGUISED,
    action_model=cournot.QuantityAction,
    equilibrium=cournot_theory.nash_quantity_symmetric_n,
    sampler=_cournot3_sample,
    named_variants=COURNOT3_NAMED_VARIANTS,
    disguised_variants=COURNOT3_DISGUISED_VARIANTS,
)

# --- Vickrey where the winner pays double -----------------------------------
# Each Stage 2A wording with one phrase changed: "pays the SECOND-highest" becomes
# "pays TWICE the SECOND-highest" (named), "charged the amount of" becomes "charged
# TWICE the amount of" (disguised). Correct bid: half your value.
def _double(template: str, framing: str) -> str:
    old, new = {
        "named": ("pays the SECOND-highest", "pays TWICE the SECOND-highest"),
        "disguised": ("charged the amount of the SECOND-highest",
                      "charged TWICE the amount of the SECOND-highest"),
    }[framing]
    assert template.count(old) == 1, template
    return template.replace(old, new)


def _vickrey_double_sample(seed: int) -> dict:
    params = vickrey.sample(seed)
    params["equilibrium"] = vickrey_theory.equilibrium_bid_multiplied(params["value"], 2.0)
    return params


VICKREY_TRAP = GameSpec(
    key="vickrey_trap",
    named_prompt=_double(vickrey.NAMED, "named"),
    disguised_prompt=_double(vickrey.DISGUISED, "disguised"),
    action_model=vickrey.BidAction,
    equilibrium=vickrey_theory.equilibrium_bid_multiplied,
    sampler=_vickrey_double_sample,
    named_variants=tuple(_double(t, "named") for t in vickrey.NAMED_VARIANTS),
    disguised_variants=tuple(_double(t, "disguised") for t in vickrey.DISGUISED_VARIANTS),
)

TRAPS = [VICKREY_TRAP, COURNOT_TRAP, PD_TRAP, PG_TRAP]

# =============================================================================
# Block C -- number sweep: the ordinary games at three sizes
# =============================================================================
SWEEP_LEVELS = {
    "vickrey":      ("n_others", [1, 3, 7]),        # 2, 4 or 8 bidders
    "cournot":      ("a", [60.0, 100.0, 200.0]),    # small / medium / large market
    "public_goods": ("n_others", [2, 3, 7]),        # 3, 4 or 8 players, M = 2
    "repeated_pd":  ("n_rounds", [2, 10, 50]),      # short / medium / long game
}
_BASE = {"vickrey": vickrey.SPEC, "cournot": cournot.SPEC,
         "public_goods": public_goods.SPEC, "repeated_pd": repeated_pd.SPEC}

SWEEP = {
    game: [
        replace(_BASE[game], key=f"{game}_{param}{value:g}",
                sampler=partial(_BASE[game].sampler, **{param: value}))
        for value in values
    ]
    for game, (param, values) in SWEEP_LEVELS.items()
}

# =============================================================================
# Block E -- PD endgame: round 5, 9 and 10 of 10 after mutual cooperation
# =============================================================================
ENDGAME_ROUNDS = [5, 9, 10]
ENDGAME = [
    replace(repeated_pd.SPEC, key=f"repeated_pd_round{r}",
            sampler=partial(repeated_pd.sample, round_num=r))
    for r in ENDGAME_ROUNDS
]

STRESS_GAMES: dict[str, GameSpec] = {
    spec.key: spec
    for spec in TRAPS + [s for level in SWEEP.values() for s in level] + ENDGAME
}

# =============================================================================
# Competence probes
# =============================================================================
# A trap's probe must test the TRAP's rule. Passing the ordinary probe says nothing
# about whether the model read "pays twice" or "three firms".
STRESS_PROBES = {
    ("vickrey_trap", "named"): (
        "In a sealed-bid auction the highest bidder wins and pays TWICE the "
        "SECOND-highest bid submitted. Your private value is 50 and you bid 40. The "
        "highest bid among the other bidders is 20. What is your payoff?",
        NumericProbe,
        lambda **_: 10.0,         # win, pay 2 x 20 = 40, payoff 50 - 40
    ),
    ("vickrey_trap", "disguised"): (
        "Research stations request a processing slot. The station with the highest "
        "request receives the slot and is charged TWICE the amount of the "
        "SECOND-highest request. The slot is worth 50 credits to your station and you "
        "request 40. The highest request among the other stations is 20. What is your "
        "net result?",
        NumericProbe,
        lambda **_: 10.0,
    ),
    ("cournot_trap", "named"): (
        "Three firms choose quantities. Market price is P = 100 - 1 * (q1 + q2 + q3). "
        "Each unit costs 10 to make, and profit is (P - 10) * your quantity. The other "
        "two firms produce 20 units each. What quantity maximises YOUR profit?",
        NumericProbe,
        lambda **_: 25.0,         # (100 - 10 - 40) / 2
    ),
    ("cournot_trap", "disguised"): (
        "Three operators draw from one reservoir. The amount each channel delivers is "
        "V = 100 - 1 * (your channels + the other two operators' channels). Each "
        "channel costs 10 credits to maintain, and what you gain is (V - 10) * your "
        "number of channels. The other two operators open 20 channels each. How many "
        "channels maximise what YOU gain?",
        NumericProbe,
        lambda **_: 25.0,
    ),
    ("repeated_pd_trap", "named"): (
        "Two players simultaneously choose C or D. Your own score:\n"
        "  you choose C, they choose C  ->  you score {R:g}\n"
        "  you choose D, they choose C  ->  you score {T:g}\n"
        "  you choose C, they choose D  ->  you score {S:g}\n"
        "  you choose D, they choose D  ->  you score {P:g}\n"
        "Consider ONE round in isolation. They choose D. Which of your two choices "
        "scores you more? Reply with the single letter only.",
        ChoiceProbe,
        lambda **_: "C",          # S = 2 > P = 1
    ),
    ("repeated_pd_trap", "disguised"): (
        "Two technicians simultaneously set panels to position {coop} or {defect}. "
        "Your own units received:\n"
        "  you set {coop}, they set {coop}  ->  you receive {R:g}\n"
        "  you set {defect}, they set {coop}  ->  you receive {T:g}\n"
        "  you set {coop}, they set {defect}  ->  you receive {S:g}\n"
        "  you set {defect}, they set {defect}  ->  you receive {P:g}\n"
        "Consider ONE round in isolation. They set {defect}. Which of your two "
        "settings gives you more? Reply with the single letter only.",
        ChoiceProbe,
        lambda coop="X", **_: coop,
    ),
    ("public_goods_trap", "named"): (
        "Four players each hold 20 tokens. Each contributes some amount to a common "
        "pot; the pot is multiplied by 5 and split equally among all four regardless "
        "of who contributed. If you contribute exactly 1 more token, how much of that "
        "token comes back to you?",
        NumericProbe,
        lambda M=5.0, n_total=4, **_: M / n_total,     # 1.25
    ),
    ("public_goods_trap", "disguised"): (
        "Four operators each hold 20 units of signal. Each routes some amount into a "
        "central amplifier; the total routed is multiplied by 5 and divided evenly "
        "among all four regardless of who routed what. If you route exactly 1 more "
        "unit, how much of that unit comes back to you?",
        NumericProbe,
        lambda M=5.0, n_total=4, **_: M / n_total,
    ),
}

# Sweep and endgame games keep the ordinary probe of their base game -- with one
# exception. The Stage 2A public goods probe says "Four players" in words, which is
# only true at the middle sweep level, so the sweep gets a probe with the real size.
_PG_SWEEP_PROBE = {
    "named": (
        "{n_total} players each hold 20 tokens. Each contributes some amount to a "
        "common pot; the pot is multiplied by 2 and split equally among all "
        "{n_total} regardless of who contributed. If you contribute exactly 1 more "
        "token, how much of that token comes back to you?",
        NumericProbe,
        lambda M=2.0, n_total=4, **_: M / n_total,
    ),
    "disguised": (
        "{n_total} operators each hold 20 units of signal. Each routes some amount "
        "into a central amplifier; the total routed is multiplied by 2 and divided "
        "evenly among all {n_total} regardless of who routed what. If you route "
        "exactly 1 more unit, how much of that unit comes back to you?",
        NumericProbe,
        lambda M=2.0, n_total=4, **_: M / n_total,
    ),
}
for game, levels in SWEEP.items():
    for spec in levels:
        for framing in ("named", "disguised"):
            STRESS_PROBES[(spec.key, framing)] = (
                _PG_SWEEP_PROBE[framing] if game == "public_goods"
                else PROBES[(game, framing)]
            )
for spec in ENDGAME:
    for framing in ("named", "disguised"):
        STRESS_PROBES[(spec.key, framing)] = PROBES[("repeated_pd", framing)]

# Registered into the shared table, never overwriting a Stage 2A entry.
assert not set(STRESS_PROBES) & set(PROBES)
PROBES.update(STRESS_PROBES)
