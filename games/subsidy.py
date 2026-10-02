"""Stage 5 materials (DRAFT, not registered): the repeated PD with a cooperation subsidy.

The Stage 2A named PD, word for word, with ONE added rule (design decision 1, option A):
the subsidy is shown as a separate rule, never folded into the payoff table. A folded table
is, for 1 < τ < 2, the game of chicken, and a model could recognise and recall that game.

Kept out of games.GAMES on purpose: nothing can run these questions until pre-registration 4
is locked and they are registered there.

Rational benchmark (stage game, every round, since the subsidy is paid every round):
  τ < P − S = 1  defect is dominant; backward induction: defect throughout
  τ > T − R = 2  cooperate is dominant
  1 < τ < 2      the stage game is chicken; the symmetric equilibrium mixes, p = τ − 1
                 (so there is no single "equilibrium action" to score against: the outcome
                 measure for Stage 5 is the cooperation RATE, not equilibrium play)
"""
from __future__ import annotations

import random
from dataclasses import replace
from functools import partial

from games import repeated_pd
from games.probes import NumericProbe

# docs/stage5-design.md. Fixed levels: baseline, the parameter-free halfway point
# (τ = ((T − R) + (P − S)) / 2 = 1.5), and the classical "guess" just above the dominance
# threshold T − R = 2. The fourth, DERIVED level is per model: Theorem 3's subsidy for 90%
# cooperation at that model's fitted λ (derived_level), fixed at the decision gate.
SUBSIDY_LEVELS = (0.0, 1.5, 2.5)
TARGET = 0.9


def derived_level(lam: float, target: float = TARGET) -> float:
    """The derived mechanism: τ(p*, λ) of Theorem 3, rounded to one decimal for the question."""
    from mechanisms.pd import required_subsidy
    return round(float(required_subsidy(target, lam)), 1)


RULE = ("On top of these scores, each player is paid an extra {tau:g} points in every round "
        "in which they choose C.")


def _with_rule(template: str, before: str) -> str:
    """Insert the subsidy rule as its own line, immediately before `before`."""
    assert template.count(before) == 1, before
    return template.replace(before, RULE + "\n" + before)


NAMED = _with_rule(repeated_pd.NAMED, "This is round {round_num}.")
NAMED_VARIANTS = (
    _with_rule(repeated_pd.NAMED_VARIANTS[0], "Current round: {round_num}."),
    _with_rule(repeated_pd.NAMED_VARIANTS[1], "Choose C or D."),
)


def rational_play(tau: float, T=5.0, R=3.0, P=1.0, S=0.0) -> str:
    if tau < P - S:
        return "D"
    if tau > T - R:
        return "C"
    return "mixed"


def sample(seed: int, tau: float) -> dict:
    p = repeated_pd.sample(seed)            # Stage 2A payoffs, round 1, same draws
    p["tau"] = tau
    p["equilibrium_named"] = rational_play(tau, p["T"], p["R"], p["P"], p["S"])
    p["equilibrium"] = p["equilibrium_named"]
    return p


def key_for(tau: float) -> str:
    return "repeated_pd_subsidy_" + f"{tau:g}".replace(".", "p")


def spec_for(tau: float):
    return replace(
        repeated_pd.SPEC, key=key_for(tau), named_prompt=NAMED, named_variants=NAMED_VARIANTS,
        disguised_prompt=None, disguised_variants=(),
        equilibrium=lambda **p: p["equilibrium_named"], sampler=partial(sample, tau=tau))


SUBSIDY_GAMES = {key_for(tau): spec_for(tau) for tau in SUBSIDY_LEVELS}

# Maths check in the question's own terms: the subsidy must be read and applied.
PROBE = (
    "Two players simultaneously choose C or D. Your own score:\n"
    "  you choose C, they choose C  ->  you score {R:g}\n"
    "  you choose D, they choose C  ->  you score {T:g}\n"
    "  you choose C, they choose D  ->  you score {S:g}\n"
    "  you choose D, they choose D  ->  you score {P:g}\n"
    + RULE + "\n"
    "In one round you choose C and the other player chooses D. Including any extra payment, "
    "how many points do you get for that round?"
)
SUBSIDY_PROBES = {
    (key, "named"): (PROBE, NumericProbe, lambda S=0.0, tau=0.0, **_: S + tau)
    for key in SUBSIDY_GAMES
}


def render(tau: float, wording: int = 0, seed: int = 1) -> str:
    """The exact question text, for the author's prompt check."""
    spec = spec_for(tau)
    return spec.prompt("named", wording, **spec.sampler(seed=seed))
