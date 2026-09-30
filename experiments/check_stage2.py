"""Is Stage 2 complete? The check to run before any analysis.

    python experiments/check_stage2.py

For every model and every block (Stage 2A and each Stage 2B block) it compares what
was planned with what was answered: every planned question must have an answer, no
answer may exist for a question that was not planned, and each cell must hold exactly
its planned count -- the stopping rule, checked rather than assumed. It also reports
server refusals still waiting to be re-asked, questions set aside after repeated
refusals, and the unreadable-answer rate per model.
"""
from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from config import CAPABILITY_ORDER
from experiments.stage2 import (MAX_TRIES_PER_TRIAL, finished, infra_attempts,
                                plan as plan_a, trial_key)
from experiments.stage2b import BLOCK_MODELS, PLANS

RAW = ROOT / "results" / "raw"


def runs():
    for m in CAPABILITY_ORDER:
        yield m, "2A", plan_a(), RAW / f"stage2_{m}.csv"
    for block in "BCED":
        for m in BLOCK_MODELS[block]:
            yield m, f"2B-{block}", PLANS[block](), RAW / f"stage2b_{block}_{m}.csv"


def main() -> int:
    all_ok = True
    print(f"{'model':18s} {'block':6s} {'answered':>15s} {'refused, to redo':>17s} "
          f"{'set aside':>9s} {'unreadable':>10s}  status")
    for model, block, planned, path in runs():
        planned_set = set(planned)
        done = finished(path)
        extra = done - planned_set
        refused = infra_attempts(path)
        waiting = {t for t in planned_set - done if 0 < refused.get(t, 0) < MAX_TRIES_PER_TRIAL}
        stuck = {t for t in planned_set - done if refused.get(t, 0) >= MAX_TRIES_PER_TRIAL}
        rows = list(csv.DictReader(path.open(encoding="utf-8"))) if path.exists() else []
        answered = [r for r in rows if r["verdict"] != "INFRA_FAIL"]
        dupes = sum(n - 1 for n in Counter(
            trial_key(r["game"], r["framing"], r["seed"], r["paraphrase_idx"])
            for r in answered).values() if n > 1)
        unreadable = sum(r["verdict"] == "PARSE_FAIL" for r in answered)
        complete = done == planned_set and not extra and not dupes
        all_ok &= complete
        status = ("COMPLETE" if complete else
                  "PROBLEM: " + ", ".join(p for p in [
                      f"{len(extra)} unplanned" if extra else "",
                      f"{dupes} answered twice" if dupes else "",
                      f"{len(stuck)} set aside" if stuck else ""] if p)
                  if (extra or dupes or stuck) else "in progress")
        print(f"{model:18s} {block:6s} {len(done & planned_set):>6d} / {len(planned_set):<6d} "
              f"{len(waiting):>17d} {len(stuck):>9d} {unreadable:>10d}  {status}")
    print("\nSTAGE 2 COMPLETE." if all_ok else "\nStage 2 not complete yet.")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
