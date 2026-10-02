"""Stage 4 toolkit: QRE bidders in second-price auctions with reserve r and multiplier α."""
import numpy as np
import pytest

from mechanisms.auction import myerson_reserve, solve

FAST = dict(n_values=61, n_bids=301)


@pytest.mark.parametrize("lam", [0.05, 0.5, 5.0])
def test_theorem1_alpha_changes_nothing_for_qre_bidders(lam):
    """M(r, α) is M(α·r, 1) with every bid divided by α: same revenue, same efficiency."""
    base = solve(lam, alpha=1.0, reserve=20.0, **FAST)
    for alpha in (2.0, 0.5):
        o = solve(lam, alpha=alpha, reserve=20.0 / alpha, **FAST)
        assert o.revenue == pytest.approx(base.revenue, rel=1e-9)
        assert o.efficiency == pytest.approx(base.efficiency, rel=1e-9)
        assert np.allclose(o.bids * alpha, base.bids)


@pytest.mark.parametrize("lam", [0.05, 0.2, 2.0])
def test_theorem2_a_reserve_never_raises_efficiency(lam):
    eff = [solve(lam, reserve=r, **FAST).efficiency for r in (0, 10, 30, 50, 70)]
    assert all(a >= b - 1e-9 for a, b in zip(eff, eff[1:]))


def test_rational_limit():
    """λ large: bids at values, revenue = E[second highest of 3 uniforms on 10–100] = 55,
    efficiency share → 1."""
    o = solve(200.0, **FAST)
    assert o.revenue == pytest.approx(55.0, abs=0.5)
    assert o.efficiency_share > 0.995


def test_no_precision_means_uniform_bids():
    o = solve(0.0, **FAST)
    assert np.allclose(o.bid_pmf, 1 / len(o.bids))


def test_myerson_reserve_for_uniform_10_100():
    assert myerson_reserve() == 50.0


def test_the_fixed_point_is_reached():
    o = solve(0.2, **FAST)
    assert o.iterations < 5000
