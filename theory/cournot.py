"""Cournot duopoly — equilibrium calculator.

Two firms simultaneously choose quantities. Market price falls as total
quantity rises:  P = a - b*Q  where Q = q1 + q2.
Each firm's profit is  (P - c_i) * q_i.

The derivation this file encodes, so you can check it against your own:

    pi_1 = (a - b(q1+q2))q1 - c1*q1
    d(pi_1)/dq1 = a - 2b*q1 - b*q2 - c1 = 0        <- first order condition
    d2(pi_1)/dq1^2 = -2b < 0                       <- so it is a MAXIMUM

    best response:   q1 = (a - c1 - b*q2) / (2b)
    solving both simultaneously:
                     q1* = (a - 2c1 + c2) / (3b)
    and when c1 == c2 == c this collapses to the symmetric result
                     q*  = (a - c) / (3b)
"""
from __future__ import annotations


def best_response(q_other: float, a: float, b: float, c: float) -> float:
    """The quantity that maximises your profit, given what the other firm makes.

    Straight from the first order condition above. Clipped at zero because a
    firm cannot produce a negative quantity -- if the other firm floods the
    market, your best response is to produce nothing at all.
    """
    q = (a - c - b * q_other) / (2 * b)
    return max(0.0, q)


def nash_quantities(a: float, b: float, c1: float, c2: float) -> tuple[float, float]:
    """Both firms' equilibrium quantities, solving the two best responses together."""
    q1 = (a - 2 * c1 + c2) / (3 * b)
    q2 = (a - 2 * c2 + c1) / (3 * b)
    return max(0.0, q1), max(0.0, q2)


def nash_quantity_symmetric(a: float, b: float, c: float) -> float:
    """The symmetric case, both firms with the same cost:  q* = (a - c) / 3b."""
    return (a - c) / (3 * b)


def market_price(q1: float, q2: float, a: float, b: float) -> float:
    """P = a - b*Q. Clipped at zero -- price cannot go negative."""
    return max(0.0, a - b * (q1 + q2))


def profit(q_i: float, q_other: float, a: float, b: float, c_i: float) -> float:
    """(price - your marginal cost) * your quantity."""
    return (market_price(q_i, q_other, a, b) - c_i) * q_i
