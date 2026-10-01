"""Fit λ to one cell (model × game × wording) and compare wordings: Δλ.

The fit is a posterior over the λ grid in analysis/qre.py, with a flat prior on
log λ between 0.001 and 1000. That choice is what handles the "too perfect" problem:
a cell where every answer is the equilibrium has evidence that keeps rising toward the
top of the grid, so instead of an infinite point estimate it gets an honest lower
bound -- "λ is at least X" -- and is flagged as CEILING.

Which answers count follows the pre-registrations: only answers whose maths check was
passed (AT_EQUILIBRIUM or STRATEGIC_GAP). The others are reported as rates, never fitted.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.special import logsumexp

from analysis.qre import LAMBDA, LOG_LAMBDA, answer_logprob

FITTED_VERDICTS = {"AT_EQUILIBRIUM", "STRATEGIC_GAP"}
CEILING_MASS = 0.05     # posterior mass in the top 5% of the log-λ range => CEILING


@dataclass
class CellFit:
    n: int
    n_clipped: int
    log_post: np.ndarray                  # normalised log posterior over LAMBDA
    median: float = field(init=False)
    lo95: float = field(init=False)
    hi95: float = field(init=False)
    ceiling: bool = field(init=False)
    floor: bool = field(init=False)

    def __post_init__(self):
        cdf = np.cumsum(np.exp(self.log_post))
        q = lambda x: float(LAMBDA[min(np.searchsorted(cdf, x), len(LAMBDA) - 1)])
        self.median, self.lo95, self.hi95 = q(0.5), q(0.025), q(0.975)
        top = LOG_LAMBDA >= LOG_LAMBDA[-1] - 0.05 * (LOG_LAMBDA[-1] - LOG_LAMBDA[0])
        bottom = LOG_LAMBDA <= LOG_LAMBDA[0] + 0.05 * (LOG_LAMBDA[-1] - LOG_LAMBDA[0])
        post = np.exp(self.log_post)
        self.ceiling = bool(post[top].sum() > CEILING_MASS)
        self.floor = bool(post[bottom].sum() > CEILING_MASS)

    def summary(self) -> str:
        if self.ceiling:
            return f"λ ≥ {self.lo95:.3g} (ceiling; n={self.n})"
        return f"λ = {self.median:.3g} [{self.lo95:.3g}, {self.hi95:.3g}] (n={self.n})"


def fit_cell(observations: list[dict]) -> CellFit:
    """observations: dicts with game, params, framing, answer -- kept answers only."""
    loglik = np.zeros_like(LAMBDA)
    clipped = 0
    for o in observations:
        lp, was_clipped = answer_logprob(o["game"], o["params"], o["framing"], o["answer"])
        loglik += lp
        clipped += was_clipped
    log_post = loglik - logsumexp(loglik)          # flat prior on the log-λ grid
    return CellFit(n=len(observations), n_clipped=clipped, log_post=log_post)


@dataclass
class DeltaLambda:
    median: float
    lo95: float
    hi95: float
    p_positive: float          # posterior probability that λ(normal) > λ(disguised)
    censored: bool             # either side at the ceiling: the difference is a bound

    note: str = ""             # set when a side is at the ceiling

    def summary(self) -> str:
        if self.note:
            return self.note
        return (f"Δλ = {self.median:+.3g} [{self.lo95:+.3g}, {self.hi95:+.3g}], "
                f"P(Δλ > 0) = {self.p_positive:.2f}")


def delta_lambda(named: CellFit, disguised: CellFit) -> DeltaLambda:
    """Δλ = λ(normal) − λ(disguised), from the two independent grid posteriors."""
    pn, pd = np.exp(named.log_post), np.exp(disguised.log_post)
    diff = LAMBDA[:, None] - LAMBDA[None, :]
    w = (pn[:, None] * pd[None, :]).ravel()
    order = np.argsort(diff.ravel())
    d, cw = diff.ravel()[order], np.cumsum(w[order])
    q = lambda x: float(d[min(np.searchsorted(cw, x), len(d) - 1)])
    # At the ceiling a side has only a lower bound, so a two-sided interval for the
    # difference would be an artefact of where the grid happens to stop.
    note = ""
    if named.ceiling and disguised.ceiling:
        note = "both wordings at the ceiling: no difference detectable in λ"
    elif named.ceiling:
        note = (f"Δλ ≥ {named.lo95 - disguised.hi95:+.3g} "
                f"(normal at the ceiling, so only a lower bound)")
    elif disguised.ceiling:
        note = (f"Δλ ≤ {named.hi95 - disguised.lo95:+.3g} "
                f"(disguised at the ceiling, so only an upper bound)")
    return DeltaLambda(
        median=q(0.5), lo95=q(0.025), hi95=q(0.975),
        p_positive=float(w[diff.ravel() > 0].sum()),
        censored=named.ceiling or disguised.ceiling, note=note,
    )
