"""Second-price auctions with noisy (logit QRE) bidders: the Stage 4 toolkit.

The rule M(r, α): the highest bid wins if it is at least the reserve r, and the winner pays
α × max(second-highest bid, r). α = 1, r = 0 is the ordinary Vickrey auction.

Bidders are symmetric logit QRE players: a bidder with value v bids b with probability
proportional to exp(λ · U(b | v)), where U is the expected payoff of b against the OTHER
bidders' noisy bids -- and those bids are themselves the QRE. solve() finds that fixed point.
(analysis/qre.py, used to FIT λ, makes the simpler assumption that rivals bid their
equilibrium bid; here, where we design, the rivals are noisy too.)

Payoffs are in value units, so λ is on the same scale as the Stage 2A Vickrey fits.

Two results this file is built to check (docs/stage4-theory.md):

  Theorem 1  α does nothing for QRE bidders. Bids under M(r, α) are the bids under
             M(α·r, 1) divided by α: same winner, same revenue, same payoffs.
             The bid grid is laid out in value units (b = β / α) so the check is exact.
  Theorem 2  For efficiency, the best reserve is r = 0: a reserve never changes who wins
             when there is a sale; it can only cancel sales.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.special import logsumexp

VALUE_RANGE = (10.0, 100.0)        # Stage 2A's Vickrey values: uniform on this range
BETA_MAX = 150.0                   # top of the bid grid, in value units (= qre.BID_MAX)


@dataclass
class Outcome:
    lam: float
    n: int
    alpha: float
    reserve: float
    revenue: float               # expected payment to the seller
    efficiency: float            # expected value of the winner (0 if no sale)
    efficiency_share: float      # efficiency / E[highest value]
    sale_prob: float
    iterations: int
    bids: np.ndarray             # bid grid
    bid_pmf: np.ndarray          # p(bid | value), shape (values, bids)
    values: np.ndarray


def value_grid(n_values: int, value_range=VALUE_RANGE) -> np.ndarray:
    lo, hi = value_range
    step = (hi - lo) / n_values
    return lo + step * (np.arange(n_values) + 0.5)          # midpoints: uniform values


def win_and_pay(pmf: np.ndarray, bids: np.ndarray, rivals: int, reserve: float):
    """For one bidder against `rivals` independent rivals bidding with pmf (over the grid):
    W[b] = P(win with bid b), P[b] = E[max(second bid, r) · 1{win}] (to be scaled by α).
    Ties are split evenly between the tied bidders (approximated as two-way)."""
    cdf = np.cumsum(pmf)
    m_cdf = cdf ** rivals                                      # CDF of the highest rival bid
    m_pmf = np.diff(np.concatenate([[0.0], m_cdf]))
    below = np.concatenate([[0.0], m_cdf[:-1]])                # P(highest rival < b)
    price = np.maximum(bids, reserve)
    pay_below = np.concatenate([[0.0], np.cumsum(m_pmf * price)[:-1]])
    W = below + 0.5 * m_pmf
    P = pay_below + 0.5 * m_pmf * price
    eligible = bids >= reserve - 1e-12
    return np.where(eligible, W, 0.0), np.where(eligible, P, 0.0)


def solve(lam: float, n: int = 3, alpha: float = 1.0, reserve: float = 0.0,
          n_values: int = 181, n_bids: int = 601, value_range=VALUE_RANGE,
          damping: float = 0.5, max_iter: int = 5000, tol: float = 1e-11) -> Outcome:
    """The symmetric logit QRE of M(reserve, alpha) with n bidders, and its outcomes."""
    values = value_grid(n_values, value_range)
    bids = np.linspace(0.0, BETA_MAX, n_bids) / alpha          # value units / α
    # start from everyone bidding (close to) their equilibrium bid, value / α
    start = np.exp(-0.5 * ((bids[None, :] * alpha - values[:, None]) / 2.0) ** 2)
    pmf_v = start / start.sum(axis=1, keepdims=True)
    agg = pmf_v.mean(axis=0)
    it = 0
    for it in range(1, max_iter + 1):
        W, P = win_and_pay(agg, bids, n - 1, reserve)
        U = values[:, None] * W[None, :] - alpha * P[None, :]
        z = lam * U
        pmf_v = np.exp(z - logsumexp(z, axis=1, keepdims=True))
        new = (1 - damping) * agg + damping * pmf_v.mean(axis=0)
        if np.abs(new - agg).max() < tol:
            agg = new
            break
        agg = new
    W, P = win_and_pay(agg, bids, n - 1, reserve)
    pmf_v = np.exp(lam * (values[:, None] * W - alpha * P)
                   - logsumexp(lam * (values[:, None] * W - alpha * P), axis=1, keepdims=True))
    # exact outcomes: each of the n bidders wins with prob W(b) at bid b
    revenue = n * float((pmf_v * (alpha * P)[None, :]).sum(axis=1).mean())
    efficiency = n * float((pmf_v * W[None, :] * values[:, None]).sum(axis=1).mean())
    sale = n * float((pmf_v * W[None, :]).sum(axis=1).mean())
    lo, hi = value_range
    best = lo + (hi - lo) * n / (n + 1)                        # E[highest of n uniforms]
    return Outcome(lam, n, alpha, reserve, revenue, efficiency, efficiency / best, sale,
                   it, bids, pmf_v, values)


def optimal_reserve(lam: float, n: int = 3, objective: str = "revenue",
                    grid: np.ndarray | None = None, **kw) -> tuple[float, Outcome]:
    """The reserve on `grid` maximising `objective` ("revenue" or "efficiency"), α = 1."""
    grid = np.arange(0.0, 100.0 + 1e-9, 1.0) if grid is None else grid
    best = None
    for r in grid:
        o = solve(lam, n=n, reserve=float(r), **kw)
        if best is None or getattr(o, objective) > getattr(best, objective) + 1e-12:
            best = o
    return best.reserve, best


def myerson_reserve(value_range=VALUE_RANGE) -> float:
    """Rational bidders, uniform values on [lo, hi]: φ(v) = 2v − hi = 0  ⇒  r* = hi / 2
    (when that is above lo)."""
    lo, hi = value_range
    return max(lo, hi / 2)
