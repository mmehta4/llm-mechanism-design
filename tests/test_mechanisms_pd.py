"""Stage 4 toolkit: the prisoner's dilemma with a cooperation subsidy, noisy (QRE) players."""
import numpy as np
import pytest

from mechanisms.pd import coop_prob, delta_u, rational_threshold, required_subsidy


@pytest.mark.parametrize("lam", [0.05, 0.154, 0.5, 2.0, 10.0])
@pytest.mark.parametrize("target", [0.1, 0.3, 0.5, 0.75, 0.9, 0.99])
def test_theorem3_the_closed_form_subsidy_hits_the_target(lam, target):
    assert coop_prob(lam, float(required_subsidy(target, lam))) == pytest.approx(target, abs=1e-6)


@pytest.mark.parametrize("lam", [0.01, 0.154, 1.0, 50.0])
def test_corollary_the_halfway_point_does_not_depend_on_lambda(lam):
    """At τ = ΔU(1/2) = ((T − R) + (P − S)) / 2, every logit-QRE population cooperates half
    the time, whatever its precision."""
    tau_half = float(delta_u(0.5, 5.0, 3.0, 1.0, 0.0))
    assert tau_half == 1.5
    assert coop_prob(lam, tau_half) == pytest.approx(0.5, abs=1e-9)


def test_cooperation_rises_with_the_subsidy():
    ps = [coop_prob(0.154, t) for t in np.linspace(0, 30, 31)]
    assert all(a < b for a, b in zip(ps, ps[1:]))


def test_rational_limit_is_a_ramp_between_the_two_dominance_thresholds():
    """λ → ∞: defect below τ = P − S = 1, cooperate above τ = T − R = 2, and in between the
    subsidised game is chicken, whose symmetric equilibrium is mixed: p = τ − 1."""
    assert rational_threshold() == 2.0
    assert coop_prob(500.0, 0.8) < 0.01 and coop_prob(500.0, 2.2) > 0.99
    for tau in (1.2, 1.5, 1.8):
        assert coop_prob(500.0, tau) == pytest.approx(tau - 1, abs=0.01)


def test_noise_makes_high_targets_dearer_and_low_targets_cheaper():
    noisy, sharp = 0.154, 5.0
    assert required_subsidy(0.9, noisy) > required_subsidy(0.9, sharp)
    assert required_subsidy(0.2, noisy) < required_subsidy(0.2, sharp)
