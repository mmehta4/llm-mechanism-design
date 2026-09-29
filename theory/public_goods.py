"""Public goods game — equilibrium calculator.

n players, each with endowment e, each contributes g_i to a common pot.
The pot is multiplied by M and split equally regardless of who contributed:

    payoff_i = e - g_i + (M/n) * sum(g_j)

The whole game turns on ONE number -- the marginal return on a unit you
contribute yourself:

    you lose 1 and get back M/n, so marginal return = -1 + M/n

    M < n  ->  negative  ->  contributing is individually irrational
                            NASH EQUILIBRIUM = contribute nothing
    M > 1  ->  every unit contributed grows the total pie
                            SOCIAL OPTIMUM = contribute everything

So the dilemma exists exactly when  1 < M < n.  Outside that range there is
no conflict at all, which is why test_theory.py checks a no-dilemma case too:
if you have only memorised "Nash is zero" that test will fail.
"""
from __future__ import annotations


def marginal_private_return(M: float, n: int) -> float:
    """-1 + M/n. Negative means free-riding is individually optimal."""
    return -1.0 + M / n


def nash_contribution(endowment: float, M: float, n: int) -> float:
    """Individually rational contribution.

    Boundary: at M == n EXACTLY, the marginal private return is zero, so every
    contribution in [0, endowment] pays the same and all of them are equilibria --
    nothing is dominant. This returns the endowment there only as a representative
    choice, not because full contribution is uniquely optimal. Caught during the
    Stage 0A blank-page test. Irrelevant to the experiment, which uses M=2, n=4.
    """
    if marginal_private_return(M, n) < 0:
        return 0.0
    return endowment          # if M > n, contributing is privately profitable


def social_optimum(endowment: float, M: float, n: int) -> float:
    """Contribution maximising the group's total payoff."""
    return endowment if M > 1 else 0.0


def has_dilemma(M: float, n: int) -> bool:
    """True when private and social incentives genuinely conflict: 1 < M < n."""
    return 1 < M < n


def payoff(g_i: float, total_contributions: float, endowment: float, M: float, n: int) -> float:
    return endowment - g_i + (M / n) * total_contributions
