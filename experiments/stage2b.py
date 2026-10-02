"""Stage 2B runner -- the stress tests, pre-registration 2.

    python experiments/stage2b.py --block B --model kimi --wait
    python experiments/stage2b.py --block B --model kimi --practice

Blocks, per model:

    B  traps        4 trap games x 2 framings x 138            = 1,104
    C  sweep        4 games x 3 sizes x 2 framings x 46         = 1,104
    D  effort       Stage 2A's exact questions, gpt-oss at low
                    and at high reasoning effort                 = 1,104 each
    E  endgame      PD rounds 5, 9, 10 x 2 framings x 138        =   828

The same rules as Stage 2A (see experiments/stage2.py): fresh seeds, named and
disguised paired on the same seed, wordings rotated evenly, a fixed shuffled order,
exactly the planned count and never more, resumable, infrastructure failures retried.

Real runs refuse to start until docs/preregistration-2.md exists and matches the
fingerprint below -- the plan has to be registered before its data exists.
`--practice` runs a few questions per cell on separate seeds, to catch bugs; practice
rows go to their own files and are never analysed.
"""
from __future__ import annotations

import argparse
import hashlib
import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from config import CAPABILITY_ORDER, MASTER_SEED
from experiments import stage2
from experiments.stage2 import WAIT_S, run_plan, sleep_until, trial_key
from games.stress import ENDGAME, SWEEP, TRAPS

FRAMINGS = ("named", "disguised")
N = 138
N_PARAPHRASES = 3

# Seed ranges never overlap with each other, with Stage 2A (MASTER_SEED + 0..137)
# or with the Stage 1 practice runs (1000..1019).
SEED_BASE = {"B": MASTER_SEED + 1_000, "C": MASTER_SEED + 2_000,
             "E": MASTER_SEED + 3_000, "D": MASTER_SEED}
PRACTICE_SEED_BASE = 900_000

# Block D (reasoning effort, gpt-oss only) was dropped on 2026-10-02, before any of its
# data existed, so that all four models answer the same questions. Recorded as deviation
# 7. Its plan stays here so the registered design remains readable; real runs refuse it.
DROPPED_BLOCKS = {"D"}

BLOCK_MODELS = {
    "B": CAPABILITY_ORDER,
    "C": CAPABILITY_ORDER,
    "D": ["gptoss120b_low", "gptoss120b_high"],
    "E": CAPABILITY_ORDER,
}

PREREG2 = ROOT / "docs" / "preregistration-2.md"
PREREG2_SHA256 = "ad378d9158fca7872babc3f024783d98e645c5dd2bb8eb4e26095a4705a9dfc0"


def _shuffled(trials: list[tuple], block: str) -> list[tuple]:
    random.Random(SEED_BASE[block] + ord(block)).shuffle(trials)
    return trials


def plan_B(n: int = N, base: int = SEED_BASE["B"]) -> list[tuple]:
    trials = [trial_key(spec.key, f, base + k, k % N_PARAPHRASES)
              for spec in TRAPS for f in FRAMINGS for k in range(n)]
    return _shuffled(trials, "B")


def plan_C(n: int = N, base: int = SEED_BASE["C"]) -> list[tuple]:
    """Question k goes to size k % 3, so each size gets n/3 questions, and wording
    (k // 3) % 3 rotates within each size."""
    trials = [trial_key(levels[k % 3].key, f, base + k, (k // 3) % N_PARAPHRASES)
              for levels in SWEEP.values() for f in FRAMINGS for k in range(n)]
    return _shuffled(trials, "C")


def plan_D(n: int = N, base: int = SEED_BASE["D"]) -> list[tuple]:
    """Stage 2A's own questions, so each effort level is compared with medium
    (Stage 2A) on identical items."""
    if n == N and base == SEED_BASE["D"]:
        return stage2.plan()
    trials = [trial_key(g, f, base + k, k % N_PARAPHRASES)
              for g in ("vickrey", "cournot", "repeated_pd", "public_goods")
              for f in FRAMINGS for k in range(n)]
    return _shuffled(trials, "D")


def plan_E(n: int = N, base: int = SEED_BASE["E"]) -> list[tuple]:
    """All three rounds share seeds, so round 5, 9 and 10 are asked of the same
    labels and the same history -- only the round number differs."""
    trials = [trial_key(spec.key, f, base + k, k % N_PARAPHRASES)
              for spec in ENDGAME for f in FRAMINGS for k in range(n)]
    return _shuffled(trials, "E")


PLANS = {"B": plan_B, "C": plan_C, "D": plan_D, "E": plan_E}
PRACTICE_N = {"B": 1, "C": 3, "D": 1, "E": 1}      # C: one question per size


def prereg2_locked() -> bool:
    return (PREREG2_SHA256 is not None and PREREG2.exists()
            and hashlib.sha256(PREREG2.read_bytes()).hexdigest() == PREREG2_SHA256)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--block", required=True, choices=sorted(PLANS))
    ap.add_argument("--model", required=True)
    ap.add_argument("--practice", action="store_true",
                    help="a few questions per cell on practice seeds, never analysed")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--wait", action="store_true")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()

    if args.block in DROPPED_BLOCKS and not args.practice:
        print(f"Block {args.block} was dropped before data collection (deviation 7).")
        return 2
    if args.model not in BLOCK_MODELS[args.block]:
        print(f"Block {args.block} runs on {BLOCK_MODELS[args.block]}, not {args.model}.")
        return 2

    raw = ROOT / "results" / "raw"
    if args.practice:
        todo_all = PLANS[args.block](n=PRACTICE_N[args.block], base=PRACTICE_SEED_BASE)
        out = raw / f"practice2b_{args.block}_{args.model}.csv"
    else:
        if not prereg2_locked() and not args.status:
            print("STOP: Stage 2B is not registered yet. docs/preregistration-2.md must "
                  "be locked and its fingerprint set in this file before real data "
                  "is collected. (--practice works now.)")
            return 1
        todo_all = PLANS[args.block]()
        out = raw / f"stage2b_{args.block}_{args.model}.csv"

    while True:
        code = run_plan(args.model, todo_all, out, limit=args.limit, status=args.status)
        if not (args.wait and code in WAIT_S):
            return code
        wake = time.strftime("%H:%M", time.localtime(time.time() + WAIT_S[code]))
        print(f"waiting until ~{wake}, then resuming.\n", flush=True)
        sleep_until(time.time() + WAIT_S[code])


if __name__ == "__main__":
    raise SystemExit(main())
