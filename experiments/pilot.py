"""Stage 1 pilot runner.

Purpose is NOT to find results. It is to find bugs cheaply, and to measure how long
a trial actually takes -- the number that determines how large the full matrix in
Stage 2 can be.
"""
from __future__ import annotations

import argparse
import statistics
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from experiments.trial import run_trial
from experiments.trial_log import TrialLog
from games import ALL_GAMES


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="qwen7b")
    ap.add_argument("--n", type=int, default=2, help="trials per game per framing")
    ap.add_argument("--games", nargs="*", default=list(ALL_GAMES))
    ap.add_argument("--out", default="results/raw/pilot.csv")
    args = ap.parse_args()

    log = TrialLog(args.out)
    rows, latencies = [], []
    verdicts = Counter()

    total = len(args.games) * 2 * args.n
    i = 0
    for game in args.games:
        for framing in ("named", "disguised"):
            for k in range(args.n):
                i += 1
                row = run_trial(game, framing, args.model, seed=1000 + k)
                rows.append(row)
                latencies.append(row["total_latency_s"])
                verdicts[row["verdict"]] += 1
                print(f"[{i:3d}/{total}] {game:14s} {framing:10s} "
                      f"dev={row['deviation']!s:>8s} {row['verdict']:18s} "
                      f"{row['total_latency_s']:6.1f}s", flush=True)

    log.write(rows)

    print("\n=== verdicts ===")
    for verdict, n in verdicts.most_common():
        print(f"  {verdict:20s} {n:3d}  ({n/len(rows):.0%})")

    med = statistics.median(latencies)
    print("\n=== latency ===")
    print(f"  median {med:.1f}s   mean {statistics.mean(latencies):.1f}s   "
          f"min {min(latencies):.1f}s   max {max(latencies):.1f}s")

    print("\n=== full-matrix projection at this latency ===")
    for n_trials in (100, 150, 300):
        cells = 4 * 2 * 2 * 3          # games x framings x models x effort levels
        hours = cells * n_trials * med / 3600
        print(f"  n={n_trials:4d} per cell -> {cells * n_trials:6,d} trials "
              f"-> {hours:6.1f} h  ({hours/24:4.1f} days)")

    print(f"\nwrote {len(rows)} rows to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
