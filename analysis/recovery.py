"""Parameter recovery: can the fit get back a λ we chose ourselves?

    python analysis/recovery.py            # full run, every game, several λ, 20 reps
    python analysis/recovery.py --quick    # what the test suite runs

For each game (Stage 2A and the Stage 2B traps), simulate a "model" with a known λ on
the exact questions the plan asks (same seeds, same numbers), fit it, and check:

  coverage   the true λ falls inside the 95% interval in roughly 95% of repetitions
  ceiling    a perfect model is flagged CEILING, never given a finite point estimate
  direction  a gap built in on purpose (named sharper than disguised) is recovered
             with the right sign

If the code cannot recover a λ we set ourselves, it cannot be trusted on real models.
Real Stage 2 answers are not touched by this file.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from analysis.fit import delta_lambda, fit_cell
from analysis.qre import sample_answer
from games import GAMES

# λ values chosen per game so equilibrium play is noticeably imperfect but not random:
# payoff scales differ by game (Cournot profits run to the hundreds, the PD is single
# digits), so a sensible λ differs too.
TRUE_LAMBDA = {
    "repeated_pd": [0.5, 1.5], "repeated_pd_trap": [0.5, 1.5],
    "public_goods": [0.3, 1.0], "public_goods_trap": [0.3, 1.0],
    "cournot": [0.02, 0.1], "cournot_trap": [0.02, 0.1],
    "vickrey": [0.05, 0.3], "vickrey_trap": [0.05, 0.3],
}
SEED_BASE = 700_000          # never used by any real Stage 2 question


def simulate(game: str, framing: str, lam: float, n: int, rng) -> list[dict]:
    obs = []
    for k in range(n):
        params = GAMES[game].sampler(seed=SEED_BASE + k)
        obs.append({"game": game, "params": params, "framing": framing,
                    "answer": sample_answer(game, params, framing, lam, rng)})
    return obs


def run(reps: int, n: int, games: list[str], quick: bool = False) -> bool:
    rng = np.random.default_rng(20261001)
    ok = True
    totals: list[tuple[int, int]] = []
    print(f"{'game':18s} {'true λ':>7s} {'covered':>8s} {'median of medians':>18s}")
    for game in games:
        for lam in TRUE_LAMBDA[game]:
            hits, meds = 0, []
            for _ in range(reps):
                f = fit_cell(simulate(game, "named", lam, n, rng))
                hits += f.lo95 <= lam <= f.hi95
                meds.append(f.median)
            cov = hits / reps
            print(f"{game:18s} {lam:7.3g} {cov:8.0%} {np.median(meds):18.3g}")
            # 95% target. With few repetitions one miss is already 75%, so the quick
            # run checks the estimate lands near the truth and leaves coverage to
            # the full run.
            if quick:
                ok &= 0.5 * lam <= float(np.median(meds)) <= 2 * lam
            else:
                # judged overall (below): with 16 settings, one at 80% of 20 is chance
                totals.append((hits, reps))
                ok &= cov >= 0.75
        # a perfect model: every answer is the equilibrium
        perfect = fit_cell(simulate(game, "named", 1e6, n, rng))
        ceiling_ok = perfect.ceiling
        # a built-in gap: named sharper than disguised
        lo, hi = TRUE_LAMBDA[game]
        d = delta_lambda(fit_cell(simulate(game, "named", hi, n, rng)),
                         fit_cell(simulate(game, "disguised", lo, n, rng)))
        print(f"{'':18s} perfect model -> {perfect.summary()}   "
              f"built-in gap -> {d.summary()}")
        ok &= ceiling_ok and d.p_positive > 0.95
    if totals:
        h, n_ = sum(t[0] for t in totals), sum(t[1] for t in totals)
        print(f"\noverall coverage {h}/{n_} = {h / n_:.1%} (target 95%; pass if >= 90%)")
        ok &= h / n_ >= 0.90
    return ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()
    games = list(TRUE_LAMBDA)
    ok = run(reps=4 if args.quick else 20, n=60 if args.quick else 138, games=games,
             quick=args.quick)
    print("\nRECOVERY PASSED" if ok else "\nRECOVERY FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
