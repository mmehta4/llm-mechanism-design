"""Practice check of Stage 2C's wordings 2 and 3 (the pilot tested wording 1 only).

    python experiments/practice_extreme.py --model nemotron

Two practice questions per game per wording, practice seeds 960,000+, never analysed.
Checks each wording parses, gets a readable answer, and its maths check is answerable.
"""
from __future__ import annotations

import argparse
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from experiments.trial import run_trial
from experiments.trial_log import TrialLog
from games.extreme import EXTREME_GAMES

ap = argparse.ArgumentParser()
ap.add_argument("--model", default="nemotron")
ap.add_argument("--games", nargs="*", default=list(EXTREME_GAMES))
ap.add_argument("--wordings", nargs="*", type=int, default=[1, 2], help="0-based wording indices")
args = ap.parse_args()
jobs = [(g, 960_000 + k, w) for g in args.games for w in args.wordings for k in range(2)]
log, lock = TrialLog(ROOT / "results" / "raw" / f"practice2c_wordings_{args.model}.csv"), threading.Lock()


def one(job):
    g, seed, w = job
    row = run_trial(g, "disguised", args.model, seed=seed, paraphrase_idx=w)
    with lock:
        log.write([row])
        print(f"{g:22s} wording {w + 1} {row['verdict']:17s} played {row.get('observed_action')} "
              f"eq {row['equilibrium']} probe_ok {row.get('probe_passed')}", flush=True)


with ThreadPoolExecutor(2) as ex:
    list(ex.map(one, jobs))
