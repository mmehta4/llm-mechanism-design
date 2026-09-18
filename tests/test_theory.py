"""Tests for the equilibrium calculators.

These are the ground truth for every number in the paper. If one of these is
wrong, every result downstream is wrong and nothing later will catch it.

Read them as a checklist you can verify by hand: each expected value is
something you can derive on paper in a couple of minutes.
"""
import math
import pytest

from theory import cournot, vickrey, repeated_pd, public_goods


# ---------------------------------------------------------------- COURNOT
# P = 100 - Q, both firms cost 10.
#   q* = (a - c)/3b = 90/3 = 30
#   P* = a - b(q1+q2) = 100 - 60 = 40
#   profit = (40 - 10) * 30 = 900

def test_cournot_symmetric_quantity():
    assert cournot.nash_quantity_symmetric(a=100, b=1, c=10) == pytest.approx(30.0)


def test_cournot_symmetric_via_general_formula():
    """The general two-cost formula must agree with the symmetric shortcut."""
    q1, q2 = cournot.nash_quantities(a=100, b=1, c1=10, c2=10)
    assert q1 == pytest.approx(30.0)
    assert q2 == pytest.approx(30.0)


def test_cournot_symmetric_price_and_profit():
    q1, q2 = cournot.nash_quantities(a=100, b=1, c1=10, c2=10)
    assert cournot.market_price(q1, q2, a=100, b=1) == pytest.approx(40.0)
    assert cournot.profit(q1, q2, a=100, b=1, c_i=10) == pytest.approx(900.0)


def test_cournot_asymmetric_costs():
    """c1=10, c2=25 -> q1=35, q2=20, P=45. The cheaper firm produces more."""
    q1, q2 = cournot.nash_quantities(a=100, b=1, c1=10, c2=25)
    assert q1 == pytest.approx(35.0)
    assert q2 == pytest.approx(20.0)
    assert cournot.market_price(q1, q2, a=100, b=1) == pytest.approx(45.0)


def test_cournot_equilibrium_is_mutual_best_response():
    """The real definition of Nash: neither firm wants to move.

    This is a stronger check than the formula test -- it verifies the
    equilibrium property itself rather than the algebra that produced it.
    """
    a, b, c = 100, 1, 10
    q1, q2 = cournot.nash_quantities(a, b, c, c)
    assert cournot.best_response(q2, a, b, c) == pytest.approx(q1)
    assert cournot.best_response(q1, a, b, c) == pytest.approx(q2)


# ---------------------------------------------------------------- VICKREY

def test_vickrey_equilibrium_bid_is_true_value():
    assert vickrey.equilibrium_bid(73.0) == 73.0


def test_vickrey_truthful_bidding_is_weakly_dominant():
    """The dominance PROOF, checked numerically rather than asserted.

    Sweep the highest rival bid across the whole range, and for each one
    confirm that bidding your true value does at least as well as bidding
    anything else. That is exactly what weak dominance means.
    """
    v = 73.0
    alternatives = [0.0, 20.0, 50.0, 65.0, 72.9, 73.1, 80.0, 95.0, 120.0]

    for m in [x * 2.5 for x in range(0, 60)]:          # rival bid 0 -> 147.5
        truthful = vickrey.payoff(v, v, m)
        for b in alternatives:
            assert truthful >= vickrey.payoff(b, v, m) - 1e-9, (
                f"bidding {b} beat truthful bidding when rival bid {m}"
            )


def test_vickrey_dominance_is_weak_not_strict():
    """There must EXIST a case where lying does exactly as well.

    If this fails, the dominance would be strict -- and it isn't. Most of the
    time the lie changes nothing, which is the whole reason the result is weak.
    """
    v = 73.0
    m = 10.0                       # rival bids far below value: you win either way
    assert vickrey.payoff(v, v, m) == pytest.approx(vickrey.payoff(80.0, v, m))


def test_vickrey_overbidding_can_lose_money():
    """Bid 90 with value 73, rival bids 80: you win and pay 80. Loss of 7."""
    assert vickrey.payoff(90.0, 73.0, 80.0) == pytest.approx(-7.0)


def test_vickrey_winner_pays_second_price():
    assert vickrey.winner_pays([73.0, 68.0, 40.0]) == 68.0


# ------------------------------------------------------------ REPEATED PD
# T=5, R=3, P=1, S=0  ->  delta_min = (T-R)/(T-P) = 2/4 = 0.5

def test_pd_stage_nash_is_mutual_defection():
    assert repeated_pd.stage_nash() == ("D", "D")


def test_pd_finite_horizon_unravels():
    """Known end -> backward induction -> defect in every single round."""
    assert repeated_pd.finite_horizon_prediction(5) == [("D", "D")] * 5


def test_pd_discount_threshold():
    assert repeated_pd.min_discount_factor(T=5, R=3, P=1, S=0) == pytest.approx(0.5)


def test_pd_cooperation_only_above_threshold():
    assert repeated_pd.cooperation_sustainable(0.6, T=5, R=3, P=1) is True
    assert repeated_pd.cooperation_sustainable(0.5, T=5, R=3, P=1) is True   # exactly at it
    assert repeated_pd.cooperation_sustainable(0.4, T=5, R=3, P=1) is False


def test_pd_higher_temptation_needs_more_patience():
    """Raising T makes cooperation harder to sustain -- a sanity check on sign."""
    low = repeated_pd.min_discount_factor(T=5, R=3, P=1)
    high = repeated_pd.min_discount_factor(T=9, R=3, P=1)
    assert high > low


# ----------------------------------------------------------- PUBLIC GOODS

def test_public_goods_free_riding_is_nash():
    """M=2, n=4: marginal return is -1 + 0.5 = -0.5. Contribute nothing."""
    assert public_goods.nash_contribution(endowment=20, M=2, n=4) == 0.0


def test_public_goods_full_contribution_is_optimal():
    assert public_goods.social_optimum(endowment=20, M=2, n=4) == 20.0


def test_public_goods_no_dilemma_when_M_exceeds_n():
    """M=5, n=4: marginal return is +0.25, so contributing is PRIVATELY optimal.

    This is the test that catches 'Nash is always zero'. It isn't -- the
    dilemma only exists when 1 < M < n.
    """
    assert public_goods.nash_contribution(endowment=20, M=5, n=4) == 20.0
    assert public_goods.has_dilemma(M=5, n=4) is False
    assert public_goods.has_dilemma(M=2, n=4) is True


def test_public_goods_payoff_arithmetic():
    """You contribute 0, three others contribute 20 each, M=2, n=4.
    payoff = 20 - 0 + (2/4)*60 = 20 + 30 = 50. Free-riding pays.
    """
    assert public_goods.payoff(0, 60, endowment=20, M=2, n=4) == pytest.approx(50.0)
