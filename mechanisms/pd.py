"""Prisoner's dilemma with a cooperation subsidy, for noisy (logit QRE) players: Stage 4.

The rule S(τ): every player who cooperates is paid τ on top of the stage-game payoff. (A tax
of τ on defecting is the same rule for the players, as only the payoff DIFFERENCE between
the two actions matters.)

Symmetric logit QRE, as in analysis/qre.py: against an opponent who cooperates with
probability p, defecting pays more by

    ΔU(p) = p·(T − R) + (1 − p)·(P − S),

so under S(τ) the advantage of defecting is ΔU(p) − τ, and

    p = 1 / (1 + exp(λ·(ΔU(p) − τ))).

Theorem 3 (docs/stage4-theory.md) inverts this: the subsidy that makes noisy players
cooperate with probability p* is

    τ(p*, λ) = ΔU(p*) + ln(p* / (1 − p*)) / λ,

in closed form, with no fixed point to solve. Rational players (λ → ∞) need only τ just above
max(T − R, P − S) for p* → 1. Noisy players need an extra ln(p*/(1−p*))/λ: cheaper than
rational theory for low targets, and ever dearer as p* → 1.
"""
from __future__ import annotations

import numpy as np

from analysis.qre import pd_coop_prob

STAGE_2A = dict(T=5.0, R=3.0, P=1.0, S=0.0)


def delta_u(p, T: float, R: float, P: float, S: float):
    """How much more defecting pays than cooperating, against cooperation probability p."""
    return np.asarray(p) * (T - R) + (1 - np.asarray(p)) * (P - S)


def coop_prob(lam: float, tau: float, T=5.0, R=3.0, P=1.0, S=0.0) -> float:
    """QRE cooperation probability under subsidy τ (the subsidy shifts both C payoffs)."""
    return float(pd_coop_prob(T, R + tau, P, S + tau, np.array([lam]))[0])


def required_subsidy(p_target, lam: float, T=5.0, R=3.0, P=1.0, S=0.0):
    """Theorem 3: the τ at which the symmetric QRE cooperation probability is p_target."""
    p = np.asarray(p_target, dtype=float)
    return delta_u(p, T, R, P, S) + np.log(p / (1 - p)) / lam


def rational_threshold(T=5.0, R=3.0, P=1.0, S=0.0) -> float:
    """Above this τ, cooperating is dominant for a rational player."""
    return max(T - R, P - S)


def expected_cost(p_target, lam: float, **payoffs) -> float:
    """Subsidy paid per player at the target: τ · p*."""
    return float(required_subsidy(p_target, lam, **payoffs) * p_target)
