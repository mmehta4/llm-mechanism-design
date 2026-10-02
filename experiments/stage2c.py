"""Stage 2C runner -- the extreme disguise, pre-registration 3.

    python experiments/stage2c.py --model kimi --wait
    python experiments/stage2c.py --model kimi --status

Per model: 4 games x 138 questions = 552, all in the extreme wording (games/extreme.py).

Question k uses the SAME seed and the same wording index as Stage 2A question k
(MASTER_SEED + k, wording k % 3), so every Stage 2A question now exists in three
versions with identical numbers: normal, disguised (2A) and extreme (2C). That pairing is
what the analysis compares.

Same rules as Stages 2A and 2B: fixed shuffled order, exactly the planned count, resumable,
server refusals re-asked. Real runs refuse to start until docs/preregistration-3.md is
locked and matches the fingerprint below.
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
from experiments.stage2 import WAIT_S, run_plan, sleep_until, trial_key
from games.extreme import EXTREME_GAMES

N = 138
N_PARAPHRASES = 3
PREREG3 = ROOT / "docs" / "preregistration-3.md"
PREREG3_SHA256 = "cda56ed6445045cfc1f7d78a804d22d97cd9bf243139c039520ab57d9054aead"


def plan() -> list[tuple]:
    trials = [trial_key(key, "disguised", MASTER_SEED + k, k % N_PARAPHRASES)
              for key in EXTREME_GAMES for k in range(N)]
    random.Random(MASTER_SEED + ord("X")).shuffle(trials)
    return trials


def prereg3_locked() -> bool:
    return (PREREG3_SHA256 is not None and PREREG3.exists()
            and hashlib.sha256(PREREG3.read_bytes()).hexdigest() == PREREG3_SHA256)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, choices=CAPABILITY_ORDER)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--wait", action="store_true")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()
    if not prereg3_locked() and not args.status:
        print("STOP: Stage 2C is not registered yet (docs/preregistration-3.md).")
        return 1
    out = ROOT / "results" / "raw" / f"stage2c_{args.model}.csv"
    while True:
        code = run_plan(args.model, plan(), out, limit=args.limit, status=args.status)
        if not (args.wait and code in WAIT_S):
            return code
        wake = time.strftime("%H:%M", time.localtime(time.time() + WAIT_S[code]))
        print(f"waiting until ~{wake}, then resuming.\n", flush=True)
        sleep_until(time.time() + WAIT_S[code])


if __name__ == "__main__":
    raise SystemExit(main())
