"""Repeated Prisoner's Dilemma — equilibrium calculator.

Stage game payoffs satisfy  T > R > P > S  and  2R > T + S:
    T = temptation (you defect, they cooperate)
    R = reward     (both cooperate)
    P = punishment (both defect)
    S = sucker     (you cooperate, they defect)

Defection strictly dominates in the one-shot game, so (D, D) is the unique
stage Nash equilibrium.

FINITE horizon, known to both players -> backward induction.
    In the last round there is no future to protect, so both defect. That
    makes the second-to-last round effectively the last, so both defect there
    too... and the whole thing unravels. Prediction: defect in EVERY round.

INDEFINITE horizon with discount factor delta -> grim trigger can hold.
    cooperate forever:        R / (1 - delta)
    defect once, then punished forever:  T + delta*P / (1 - delta)

    Cooperation is sustainable when the first is at least the second:
        R/(1-delta)  >=  T + delta*P/(1-delta)
        R            >=  T(1-delta) + delta*P
        delta(T - P) >=  T - R
        delta        >=  (T - R) / (T - P)
"""
from __future__ import annotations

COOPERATE = "C"
DEFECT = "D"


def stage_nash() -> tuple[str, str]:
    """The one-shot equilibrium: both defect."""
    return (DEFECT, DEFECT)


def finite_horizon_prediction(n_rounds: int) -> list[tuple[str, str]]:
    """Backward induction says defect every round when the end is known."""
    return [(DEFECT, DEFECT) for _ in range(n_rounds)]


def min_discount_factor(T: float, R: float, P: float, S: float = 0.0) -> float:
    """Smallest delta for which grim trigger sustains cooperation.

    delta >= (T - R) / (T - P).  S is unused in the threshold but kept in the
    signature so callers pass the full payoff structure in one place.
    """
    return (T - R) / (T - P)


def cooperation_sustainable(delta: float, T: float, R: float, P: float, S: float = 0.0) -> bool:
    """Is cooperation an equilibrium at this discount factor?"""
    return delta >= min_discount_factor(T, R, P, S)
