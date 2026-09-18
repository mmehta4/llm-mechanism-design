"""Second-price sealed-bid (Vickrey) auction — equilibrium calculator.

n bidders, each with a private value v_i, each submits one sealed bid b_i.
Highest bidder wins and pays the SECOND-highest bid. Winner's payoff is
v_i - (second highest bid); everyone else gets zero.

Bidding your true value is WEAKLY DOMINANT. The proof, which test_theory.py
checks numerically rather than just asserting:

    Fix m = the highest bid among everyone else. It is arbitrary -- that is
    what "dominant" means.

    Bid b > v:  the only case that differs from bidding v is  v < m < b.
                You now win and pay m > v, so payoff = v - m < 0.  Worse.
    Bid b < v:  the only case that differs is  b < m < v.
                You now lose (payoff 0) instead of winning at price m < v
                (payoff v - m > 0).  Worse.
    Every other case: identical outcome.

    WEAK, not strict, because in most cases the lie changes nothing at all.
"""
from __future__ import annotations


def equilibrium_bid(private_value: float) -> float:
    """The weakly dominant strategy: bid exactly what the item is worth to you."""
    return private_value


def payoff(own_bid: float, private_value: float, highest_other_bid: float) -> float:
    """Your payoff given your bid, your true value, and the best rival bid.

    Ties are resolved in the rival's favour here. That is a deliberate
    simplification: exact ties have probability zero with continuous values,
    and it keeps the dominance argument clean.
    """
    if own_bid > highest_other_bid:
        return private_value - highest_other_bid   # you win, pay SECOND price
    return 0.0                                     # you lose


def winner_pays(bids: list[float]) -> float:
    """The price actually charged: the second-highest bid submitted."""
    if len(bids) < 2:
        return 0.0
    return sorted(bids, reverse=True)[1]
