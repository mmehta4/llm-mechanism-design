"""Stage 3 fitting: the pieces checked by hand, pinned so they cannot drift."""
import numpy as np
import pytest

from analysis import qre
from analysis.fit import delta_lambda, fit_cell
from analysis.recovery import simulate
from games import GAMES


def test_pd_fixed_point_matches_the_workbook():
    """STAGE-3-TASKS.md Task 3.1 works these out by hand."""
    p = qre.pd_coop_prob(5, 3, 1, 0, np.array([0.5, 1.0, 2.0]))
    assert p == pytest.approx([0.3386, 0.2268, 0.0998], abs=1e-3)


def test_harmony_trap_makes_cooperation_likely():
    assert qre.pd_coop_prob(3, 5, 1, 2, np.array([2.0]))[0] > 0.9


@pytest.mark.parametrize("key,mult", [("vickrey", 1.0), ("vickrey_trap", 2.0)])
def test_vickrey_payoff_peaks_at_the_equilibrium(key, mult):
    p = GAMES[key].sampler(seed=5)
    grid = qre.vickrey_grid(p)
    assert grid[np.argmax(qre.vickrey_utilities(p, grid, mult))] == pytest.approx(p["equilibrium"])


@pytest.mark.parametrize("key", ["public_goods", "public_goods_trap"])
def test_public_goods_payoff_peaks_at_the_equilibrium(key):
    p = GAMES[key].sampler(seed=5)
    grid = qre.pg_grid(p)
    assert grid[np.argmax(qre.pg_utilities(p, grid))] == p["equilibrium"]


def test_equilibrium_answer_lands_exactly_on_the_grid():
    p = GAMES["cournot"].sampler(seed=5)
    grid = qre.cournot_grid(p)
    i, clipped = qre.nearest(grid, p["equilibrium"])
    assert grid[i] == pytest.approx(p["equilibrium"]) and not clipped


@pytest.mark.parametrize("game,lam", [("repeated_pd", 1.0), ("public_goods", 0.5)])
def test_recovers_a_known_lambda(game, lam):
    fit = fit_cell(simulate(game, "named", lam, 138, np.random.default_rng(1)))
    assert fit.lo95 <= lam <= fit.hi95
    assert not fit.ceiling


def test_perfect_model_is_a_ceiling_not_infinity():
    fit = fit_cell(simulate("public_goods", "named", 1e6, 60, np.random.default_rng(2)))
    assert fit.ceiling and "λ ≥" in fit.summary()


def test_both_ceilings_means_no_difference_detectable():
    rng = np.random.default_rng(3)
    a = fit_cell(simulate("public_goods", "named", 1e6, 40, rng))
    b = fit_cell(simulate("public_goods", "disguised", 1e6, 40, rng))
    assert "no difference detectable" in delta_lambda(a, b).summary()


def test_built_in_gap_recovered_with_right_sign():
    rng = np.random.default_rng(4)
    d = delta_lambda(fit_cell(simulate("repeated_pd", "named", 2.0, 138, rng)),
                     fit_cell(simulate("repeated_pd", "disguised", 0.3, 138, rng)))
    assert d.p_positive > 0.95 and d.median > 0


def test_equivalence_test_reads_the_p_value_not_the_statistic():
    """The practice run once printed TOST p = -0.886."""
    from statsmodels.stats.proportion import tost_proportions_2indep
    p = tost_proportions_2indep(19, 20, 18, 20, -0.13, 0.13).pvalue
    assert 0 <= p <= 1 and p == pytest.approx(0.188, abs=0.01)


def test_analysis_is_locked():
    """Editing the plan or the analysis code after the lock must fail loudly."""
    from analysis.lock import analysis_locked
    assert analysis_locked()
