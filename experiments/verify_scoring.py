"""Re-score every Stage 2 answer from scratch -- the check to run before analysis.

    python experiments/verify_scoring.py

For each answered trial it rebuilds, from the seed alone, the question that should
have been asked, its game-theory answer, the maths check and its answer key, then
re-derives the verdict, and compares all of it with what was recorded. Written after
the practice-run PD bug, where answers were scored against the wrong labels for days
without anything looking wrong.
"""
from __future__ import annotations

import csv
import math
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from experiments.trial import deviation_of, equilibrium_for, verdict_of
from games import GAMES
from games.probes import is_malformed, probe_for, probe_passed


def same(a, stored: str) -> bool:
    if isinstance(a, str):
        return a == stored
    try:
        return math.isclose(float(a), float(stored))
    except (TypeError, ValueError):
        return False


def main() -> int:
    checked, problems = 0, Counter()
    for path in sorted((ROOT / "results" / "raw").glob("stage2*.csv")):
        with path.open(encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r["verdict"] == "INFRA_FAIL":
                    continue
                checked += 1
                spec = GAMES[r["game"]]
                p = spec.sampler(seed=int(r["seed"]))
                eq = equilibrium_for(p, r["framing"])
                if spec.prompt(r["framing"], int(r["paraphrase_idx"]), **p) != r["play_prompt"]:
                    problems[f"{path.name}: question differs from plan"] += 1
                if not same(eq, r["equilibrium"]):
                    problems[f"{path.name}: wrong game-theory answer stored"] += 1
                probe_prompt, _, probe_correct = probe_for(r["game"], r["framing"], **p)
                if probe_prompt != r["probe_prompt"] or not same(probe_correct, r["probe_correct_answer"]):
                    problems[f"{path.name}: maths check differs"] += 1
                parsed = r["probe_parse_ok"] == "True"
                play_ok = r["play_parse_ok"] == "True"
                view = {
                    "infra": None,
                    "play_parse_ok": play_ok,
                    "probe_malformed": is_malformed(r["probe_answer"] or None, probe_correct) if parsed else True,
                    "probe_passed": probe_passed(r["probe_answer"], probe_correct) if parsed else None,
                    "deviation": deviation_of(r["observed_action"], eq) if play_ok else None,
                }
                if verdict_of(view, eq) != r["verdict"]:
                    problems[f"{path.name}: verdict {r['verdict']} re-derives differently"] += 1
    print(f"answers re-checked: {checked}")
    if not problems:
        print("every question, answer key, maths check and verdict matches. OK.")
        return 0
    for k, n in problems.most_common():
        print(f"  PROBLEM  {k}: {n}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
