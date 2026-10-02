"""Stage 2C pilot: do deeper disguises stop a model recognising the game?

    python experiments/pilot_deep.py --model nemotron --n 8
    python experiments/pilot_deep.py --model nemotron --summary

For each game, the same practice questions (seeds 950,000+) are asked in three wordings:
the Stage 2A disguise (baseline), deep1 (rephrased rule) and deep2 (abstract). Practice
seeds only, never analysed as data; no registered question is touched.

Measured per wording: how often the reasoning NAMES the game (the validated Stage 3.5
code, κ = 1.00), how often the answer is the equilibrium, and how often the maths check
is passed -- so a disguise that only "works" by making the problem harder shows up.
"""
from __future__ import annotations

import argparse
import csv
import sys
import threading
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from analysis.reasoning import code
from experiments.trial import run_trial
from experiments.trial_log import TrialLog

FAMILIES = ["vickrey", "cournot", "repeated_pd", "public_goods"]
LEVELS = {"baseline (2A disguise)": "", "deep1 rephrased rule": "_deep1", "deep2 abstract": "_deep2"}
SEED_BASE = 950_000


def out_path(model: str) -> Path:
    return ROOT / "results" / "raw" / f"practice2c_{model}.csv"


def run(model: str, n: int, workers: int) -> None:
    jobs = [(fam + suffix, SEED_BASE + k) for fam in FAMILIES for suffix in LEVELS.values()
            for k in range(n)]
    log, lock = TrialLog(out_path(model)), threading.Lock()
    done = 0

    def one(job):
        nonlocal done
        game, seed = job
        row = run_trial(game, "disguised", model, seed=seed, paraphrase_idx=0)
        with lock:
            log.write([row])
            done += 1
            print(f"[{done:3d}/{len(jobs)}] {game:20s} {row['verdict']:17s} "
                  f"{row['total_latency_s']:6.1f}s", flush=True)

    with ThreadPoolExecutor(workers) as ex:
        list(ex.map(one, jobs))


def summary(model: str) -> str:
    rows = [r for r in csv.DictReader(out_path(model).open(encoding="utf-8"))
            if r["verdict"] != "INFRA_FAIL"]
    out = [f"# Stage 2C pilot: deeper disguises ({model}, practice questions only)", "",
           "| Game | Wording | n | Names the game | At equilibrium | Maths check passed |",
           "|---|---|---:|---:|---:|---:|"]
    for fam in FAMILIES:
        for label, suffix in LEVELS.items():
            rs = [r for r in rows if r["game"] == fam + suffix]
            if not rs:
                continue
            counted = [r for r in rs if r["verdict"] in ("AT_EQUILIBRIUM", "STRATEGIC_GAP")]
            names = sum("NAMES_GAME" in code(r) for r in counted)
            eq = sum(r["verdict"] == "AT_EQUILIBRIUM" for r in rs)
            probe = sum(r["probe_passed"] == "True" for r in rs)
            pct = lambda k, n_: f"{k / n_:.0%} ({k}/{n_})" if n_ else "–"
            out.append(f"| {fam} | {label} | {len(rs)} | {pct(names, len(counted))} | "
                       f"{pct(eq, len(rs))} | {pct(probe, len(rs))} |")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="nemotron")
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--summary", action="store_true")
    args = ap.parse_args()
    if not args.summary:
        run(args.model, args.n, args.workers)
    text = summary(args.model)
    (ROOT / "results" / "analysis" / f"pilot_deep_{args.model}.md").write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
