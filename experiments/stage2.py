"""Stage 2 runner -- the confirmatory experiment described in docs/preregistration-1.md.

Per model: 4 games x 2 framings x 138 questions = 1,104 trials.

Design rules, each one tied to the pre-registration:

* FRESH QUESTIONS. Seeds are MASTER_SEED..MASTER_SEED+137. The practice runs used
  1000..1019, so no Stage 2 question was seen before the predictions were written.
* PAIRED. Question k uses the same seed -- the same private values, the same numbers --
  in the named and the disguised framing, and for every model. Wording is the only
  thing that differs inside a pair.
* WORDINGS ROTATE. Question k uses paraphrase k % 3, so each wording carries 46 of the
  138 questions, identically across framings. That is what makes the wording check
  (Section 5) a fair comparison.
* SHUFFLED ORDER. Trials run in a fixed random order, so named and disguised questions
  are interleaved in time. If a provider silently changes a model halfway through a
  two-day run, the change lands on both framings equally instead of on one.
* STOPPING RULE. The plan is exactly 138 per cell. The runner never adds trials; it
  only re-attempts ones the model never received (INFRA_FAIL).
* RESUMABLE. Every row is appended as it finishes. Re-running the same command skips
  finished trials, so a crash, a closed laptop, or a daily quota costs nothing.
  INFRA_FAIL rows stay in the file as an audit trail; analysis uses the one
  non-infra row per trial.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import random
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from config import CAPABILITY_ORDER, MASTER_SEED
from experiments.trial import INFRA_FAIL, run_trial
from experiments.trial_log import TrialLog
from games import ALL_GAMES

N_PER_CELL = 138
N_PARAPHRASES = 3
FRAMINGS = ("named", "disguised")

PREREG = ROOT / "docs" / "preregistration-1.md"
PREREG_SHA256 = "a70cf95ace715646b5ef000845ab56cc2289d00c267878c2c1943f4643a78a40"

# this many infrastructure failures in a row means the provider is down or a cap
# we did not recognise has been hit -- stop rather than burn the rest of the day
MAX_INFRA_STREAK = 5

EXIT_DONE, EXIT_QUOTA, EXIT_INFRA = 0, 3, 4


def trial_key(game: str, framing: str, seed: int, paraphrase: int) -> tuple:
    return (game, framing, int(seed), int(paraphrase))


def plan(games=None) -> list[tuple]:
    """Every trial one model owes, in the fixed shuffled order."""
    games = list(games or ALL_GAMES)
    trials = [
        trial_key(g, f, MASTER_SEED + k, k % N_PARAPHRASES)
        for g in games for f in FRAMINGS for k in range(N_PER_CELL)
    ]
    # the order is seeded too, so every model -- and every resumed run -- walks the
    # same sequence
    random.Random(MASTER_SEED).shuffle(trials)
    return trials


def finished(path: Path) -> set[tuple]:
    """Trials already answered by the model (anything except INFRA_FAIL)."""
    if not path.exists():
        return set()
    with path.open(newline="", encoding="utf-8") as f:
        return {
            trial_key(r["game"], r["framing"], r["seed"], r["paraphrase_idx"])
            for r in csv.DictReader(f) if r["verdict"] != INFRA_FAIL
        }


def prereg_intact() -> bool:
    return hashlib.sha256(PREREG.read_bytes()).hexdigest() == PREREG_SHA256


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--model", required=True, choices=CAPABILITY_ORDER)
    ap.add_argument("--limit", type=int, default=None,
                    help="stop after this many trials this session (smoke tests)")
    ap.add_argument("--status", action="store_true",
                    help="print progress and exit without calling any model")
    args = ap.parse_args()

    if not prereg_intact():
        print("STOP: docs/preregistration-1.md no longer matches the registered "
              "fingerprint. Stage 2 must run against the plan that was registered.")
        return 1

    out = ROOT / "results" / "raw" / f"stage2_{args.model}.csv"
    todo_all = plan()
    done = finished(out)
    todo = [t for t in todo_all if t not in done]

    print(f"{args.model}: {len(done)}/{len(todo_all)} done, {len(todo)} to go  -> {out.name}")
    if args.status or not todo:
        return EXIT_DONE

    if args.limit is not None:
        todo = todo[:args.limit]

    log = TrialLog(out)
    verdicts, infra_streak, t0 = Counter(), 0, time.time()

    for i, (game, framing, seed, para) in enumerate(todo, 1):
        row = run_trial(game, framing, args.model, seed=seed, paraphrase_idx=para)
        log.write([row])
        verdicts[row["verdict"]] += 1

        n_done = len(done) + sum(v for k, v in verdicts.items() if k != INFRA_FAIL)
        rate = i / max(time.time() - t0, 1e-9) * 3600
        print(f"[{n_done:4d}/{len(todo_all)}] {game:12s} {framing:9s} p{para} "
              f"{row['verdict']:17s} {row['total_latency_s']:6.1f}s  "
              f"~{rate:.0f}/h{'  ' + row['infra'] if row.get('infra') else ''}",
              flush=True)

        if row["verdict"] != INFRA_FAIL:
            infra_streak = 0
            continue
        infra_streak += 1
        if row["infra"] == "quota":
            print("\nDaily quota reached. Nothing is lost -- run the same command "
                  "tomorrow and it carries on from here.")
            return EXIT_QUOTA
        if infra_streak >= MAX_INFRA_STREAK:
            print(f"\n{MAX_INFRA_STREAK} infrastructure failures in a row "
                  f"(last: {row['infra']}). Stopping; re-run later to resume.")
            return EXIT_INFRA

    print("\nthis session:", dict(verdicts))
    remaining = len(todo_all) - len(finished(out))
    print("model complete." if remaining == 0 else f"{remaining} trials still to go.")
    return EXIT_DONE


if __name__ == "__main__":
    raise SystemExit(main())
