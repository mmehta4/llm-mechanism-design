"""Logit quantal response: how likely each move is, for any precision λ.

    P(move a) = exp(λ·u(a)) / Σ_b exp(λ·u(b))

λ = 0 is uniform noise; λ → ∞ is the game-theory answer. Everything here is computed
for a whole GRID of λ values at once, because the fit (analysis/fit.py) needs the
likelihood of each observed answer at every λ on the grid.

How each game's expected payoff u(a) is built -- the modelling choices, fixed here
before any real Stage 2 data is fitted:

  Repeated PD     Symmetric logit QRE of the stage game: the opponent cooperates with
                  probability p, and p is the fixed point of the model's own logit
                  response. Continuation play is ignored: with a dominant stage action
                  and a known horizon it does not change the equilibrium action.
                  Rounds 5/9/10 (Block E) use the same stage-game model.
  Public goods    Each token returns M/n to its owner whatever the others do, so
                  u(g) = (M/n - 1)·g up to a constant. No fixed point is needed.
  Cournot         Symmetric logit QRE: profit is linear in the rivals' TOTAL, so only
                  the rivals' mean quantity matters, and that mean is the fixed point
                  of the model's own logit response. n = 2, or 3 for the trap.
  Vickrey         The question does not state the rivals' values, so they are assumed
                  to bid their equilibrium bid (value / m, where the winner pays m times
                  the second-highest bid) with values uniform on [10, 100] -- the range
                  the questions are drawn from. Logit response to that.

Numeric answers are placed on a grid with step 0.5 that also contains the exact
equilibrium answer, so a model that plays the equilibrium exactly is scored as doing so.
"""
from __future__ import annotations

import numpy as np
from scipy.special import expit, logsumexp

# λ grid: log-uniform from 0.001 to 1000. The top is the "too perfect" ceiling: a
# cell whose evidence keeps rising toward it is reported as "λ at least ...".
LOG_LAMBDA = np.linspace(np.log(1e-3), np.log(1e3), 481)
LAMBDA = np.exp(LOG_LAMBDA)

STEP = 0.5
VALUE_RANGE = (10.0, 100.0)          # games/vickrey.py draws values uniformly here
BID_MAX = 150.0


def numeric_grid(lo: float, hi: float, equilibrium: float) -> np.ndarray:
    grid = np.arange(lo, hi + STEP / 2, STEP)
    return np.unique(np.append(grid, float(np.clip(equilibrium, lo, hi))))


def nearest(grid: np.ndarray, x: float) -> tuple[int, bool]:
    """Index of the grid point closest to an answer, and whether it had to be clipped
    into range (an impossible answer, e.g. a negative bid)."""
    clipped = not (grid[0] - STEP / 2 <= x <= grid[-1] + STEP / 2)
    return int(np.argmin(np.abs(grid - x))), clipped


def logit_logprobs(utilities: np.ndarray, lam: np.ndarray = LAMBDA) -> np.ndarray:
    """log P(each action) for each λ: shape (len(lam), len(utilities))."""
    z = lam[:, None] * utilities[None, :]
    return z - logsumexp(z, axis=1, keepdims=True)


# --- Repeated PD ------------------------------------------------------------

def pd_coop_prob(T: float, R: float, P: float, S: float,
                 lam: np.ndarray = LAMBDA) -> np.ndarray:
    """Symmetric QRE probability of cooperating, for each λ.

    D pays more than C by  dU(p) = p(T-R) + (1-p)(P-S)  against an opponent who
    cooperates with probability p, so  p = 1 / (1 + exp(λ·dU(p))).  The right side
    minus p is positive at p=0 and negative at p=1, so bisection finds the root.
    """
    lo, hi = np.zeros_like(lam), np.ones_like(lam)
    for _ in range(60):
        mid = (lo + hi) / 2
        du = mid * (T - R) + (1 - mid) * (P - S)
        above = expit(-lam * du) > mid
        lo, hi = np.where(above, mid, lo), np.where(above, hi, mid)
    return (lo + hi) / 2


def pd_logprob(params: dict, chose_coop: bool, lam: np.ndarray = LAMBDA) -> np.ndarray:
    p = pd_coop_prob(params["T"], params["R"], params["P"], params["S"], lam)
    p = np.clip(p, 1e-300, 1 - 1e-16)
    return np.log(p) if chose_coop else np.log1p(-p)


# --- Public goods -------------------------------------------------------------

def pg_grid(params: dict) -> np.ndarray:
    return numeric_grid(0.0, params["endowment"], params["equilibrium"])


def pg_utilities(params: dict, grid: np.ndarray) -> np.ndarray:
    return (params["M"] / params["n_total"] - 1.0) * grid


# --- Cournot ------------------------------------------------------------------

def cournot_grid(params: dict) -> np.ndarray:
    top = (params["a"] - params["c"]) / params["b"]
    return numeric_grid(0.0, top, params["equilibrium"])


def cournot_logprobs(params: dict, grid: np.ndarray, lam: np.ndarray = LAMBDA) -> np.ndarray:
    """Symmetric QRE: expected profit (a - c - b·q - b·(n-1)·m)·q, where m is the
    rivals' mean quantity. m is the fixed point of m = E_λ[q | m]; the right side
    falls as m rises, so bisection on m finds it for every λ at once."""
    a, b, c = params["a"], params["b"], params["c"]
    n = params.get("n_firms", 2)
    lo, hi = np.zeros_like(lam), np.full_like(lam, grid[-1])
    for _ in range(50):
        m = (lo + hi) / 2
        u = (a - c - b * grid[None, :] - b * (n - 1) * m[:, None]) * grid[None, :]
        z = lam[:, None] * u
        prob = np.exp(z - logsumexp(z, axis=1, keepdims=True))
        mean = prob @ grid
        above = mean > m
        lo, hi = np.where(above, m, lo), np.where(above, hi, m)
    m = (lo + hi) / 2
    u = (a - c - b * grid[None, :] - b * (n - 1) * m[:, None]) * grid[None, :]
    z = lam[:, None] * u
    return z - logsumexp(z, axis=1, keepdims=True)


# --- Vickrey ------------------------------------------------------------------

def vickrey_grid(params: dict) -> np.ndarray:
    return numeric_grid(0.0, BID_MAX, params["equilibrium"])


def vickrey_utilities(params: dict, grid: np.ndarray, multiplier: float = 1.0) -> np.ndarray:
    """Expected payoff of each bid against n_others rivals who bid value/multiplier,
    values uniform on VALUE_RANGE. Win when your bid beats the highest rival bid H;
    then pay multiplier·H."""
    v, k = params["value"], params["n_others"]
    lo, hi = VALUE_RANGE[0] / multiplier, VALUE_RANGE[1] / multiplier
    h = np.linspace(lo, hi, 4001)
    dens = k * ((h - lo) / (hi - lo)) ** (k - 1) / (hi - lo)       # density of H
    gain = (v - multiplier * h) * dens
    # cumulative integral of gain up to each h, then read it off at each bid
    cum = np.concatenate([[0.0], np.cumsum((gain[1:] + gain[:-1]) / 2 * np.diff(h))])
    return np.interp(np.clip(grid, lo, hi), h, cum)


# --- One entry point ----------------------------------------------------------

def family(game_key: str) -> str:
    for fam in ("vickrey", "cournot", "public_goods", "repeated_pd"):
        if game_key.startswith(fam):
            return fam
    raise KeyError(game_key)


def answer_logprob(game_key: str, params: dict, framing: str, answer,
                   lam: np.ndarray = LAMBDA) -> tuple[np.ndarray, bool]:
    """log P(this answer | λ) at every λ, and whether the answer was out of range."""
    fam = family(game_key)
    if fam == "repeated_pd":
        coop = "C" if framing == "named" else params["coop"]
        return pd_logprob(params, str(answer).strip().upper() == coop.upper(), lam), False
    x = float(answer)
    if fam == "public_goods":
        grid = pg_grid(params)
        i, clipped = nearest(grid, x)
        return logit_logprobs(pg_utilities(params, grid), lam)[:, i], clipped
    if fam == "cournot":
        grid = cournot_grid(params)
        i, clipped = nearest(grid, x)
        return cournot_logprobs(params, grid, lam)[:, i], clipped
    mult = 2.0 if game_key == "vickrey_trap" else 1.0
    grid = vickrey_grid(params)
    i, clipped = nearest(grid, x)
    return logit_logprobs(vickrey_utilities(params, grid, mult), lam)[:, i], clipped


def sample_answer(game_key: str, params: dict, framing: str, lam: float,
                  rng: np.random.Generator):
    """Draw one answer from the QRE model at a single λ -- for parameter recovery."""
    fam = family(game_key)
    lam_arr = np.array([lam])
    if fam == "repeated_pd":
        p = pd_coop_prob(params["T"], params["R"], params["P"], params["S"], lam_arr)[0]
        coop = rng.random() < p
        if framing == "named":
            return "C" if coop else "D"
        return params["coop"] if coop else params["defect"]
    if fam == "public_goods":
        grid = pg_grid(params)
        lp = logit_logprobs(pg_utilities(params, grid), lam_arr)[0]
    elif fam == "cournot":
        grid = cournot_grid(params)
        lp = cournot_logprobs(params, grid, lam_arr)[0]
    else:
        mult = 2.0 if game_key == "vickrey_trap" else 1.0
        grid = vickrey_grid(params)
        lp = logit_logprobs(vickrey_utilities(params, grid, mult), lam_arr)[0]
    return float(rng.choice(grid, p=np.exp(lp - logsumexp(lp))))
