"""Stage 5 runner -- the PD cooperation subsidy, pre-registration 4.

    python experiments/stage5.py --model nemotron --wait
    python experiments/stage5.py --model nemotron --status

Per model: Stage 2A's named 10-round PD (round 1) with a subsidy τ paid to every player for
each round they choose C (games/subsidy.py), at the levels fixed in docs/stage5-design.md:

    τ = 0.0, 1.5, 2.5, and τ* = 1.9 + ln 9 / λ̂ (the derived mechanism, 90% target)

100 questions per level, balanced 34/33/33 across the three Stage 2A paraphrases, with new
seeds, in a fixed shuffled order. λ̂ is the model's Stage 2A named-wording PD λ (posterior
median), entered in LAMBDA_HAT at the decision gate. Gate rules (docs/decision-gate.md): τ* is
capped at 50; a model with λ̂ ≥ 3.66 has no separate derived level (τ* ≤ 2.5 there).

Same rules as Stages 2A–2C: exactly the planned count, resumable, server refusals re-asked.
Real runs refuse to start until docs/preregistration-4.md is locked and matches the
fingerprint below, and until the model's λ̂ is entered.
"""
from __future__ import annotations

import argparse
import hashlib
import math
import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from config import CAPABILITY_ORDER, MASTER_SEED
from experiments.stage2 import WAIT_S, run_plan, sleep_until, trial_key
from games import GAMES
from games.probes import PROBES, NumericProbe
from games.subsidy import PROBE, SUBSIDY_LEVELS, derived_level, key_for, spec_for

N = 100
N_PARAPHRASES = 3
SEED0 = MASTER_SEED + 50_000          # a block no earlier stage uses
TAU_CAP = 50.0
LAMBDA_CEILING = math.log(9) / (2.5 - 1.9)    # = 3.66: at or above it, τ* ≤ 2.5

# Filled at the decision gate (2026-10-11) from each model's Stage 2A named-PD fit, posterior
# median (analysis/gate.py, analysis/stage5.stage2a_pd); locked with pre-registration 4.
LAMBDA_HAT: dict[str, float] = {
    "gptoss120b": 0.5787619883491204,      # tau* = 5.7
    "nemotron": 0.15399265260594916,       # tau* = 16.2
    "kimi": 0.007498942093324564,          # tau* capped at 50 (floor rule)
    "gemini_lite": 0.003162277660168379,   # tau* capped at 50 (floor rule)
}

PREREG4 = ROOT / "docs" / "preregistration-4.md"
PREREG4_SHA256 = "f70c9c016bb812c9b4c6fe6fbd96b9152917306f93e41cde0f1e103ce5219f2a"


def levels_for(model: str) -> tuple[float, ...]:
    lam = LAMBDA_HAT[model]
    if lam >= LAMBDA_CEILING:
        return tuple(SUBSIDY_LEVELS)                      # derived level coincides with 2.5
    return tuple(SUBSIDY_LEVELS) + (min(derived_level(lam), TAU_CAP),)


def register(levels: tuple[float, ...]) -> None:
    """Make these subsidy questions runnable -- only ever called after the lock check."""
    for tau in levels:
        key = key_for(tau)
        GAMES.setdefault(key, spec_for(tau))
        PROBES.setdefault((key, "named"), (PROBE, NumericProbe,
                                           lambda S=0.0, tau=0.0, **_: S + tau))


def plan(model: str) -> list[tuple]:
    trials = [trial_key(key_for(tau), "named", SEED0 + k, k % N_PARAPHRASES)
              for tau in levels_for(model) for k in range(N)]
    random.Random(MASTER_SEED + ord("5")).shuffle(trials)
    return trials


def prereg4_locked() -> bool:
    return (PREREG4_SHA256 is not None and PREREG4.exists()
            and hashlib.sha256(PREREG4.read_bytes()).hexdigest() == PREREG4_SHA256)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, choices=CAPABILITY_ORDER)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--wait", action="store_true")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()
    if args.model not in LAMBDA_HAT:
        print(f"STOP: no fitted λ for {args.model} yet (entered at the decision gate).")
        return 1
    if not prereg4_locked() and not args.status:
        print("STOP: Stage 5 is not registered yet (docs/preregistration-4.md).")
        return 1
    register(levels_for(args.model))
    out = ROOT / "results" / "raw" / f"stage5_{args.model}.csv"
    while True:
        code = run_plan(args.model, plan(args.model), out, limit=args.limit, status=args.status)
        if not (args.wait and code in WAIT_S):
            return code
        wake = time.strftime("%H:%M", time.localtime(time.time() + WAIT_S[code]))
        print(f"waiting until ~{wake}, then resuming.\n", flush=True)
        sleep_until(time.time() + WAIT_S[code])


if __name__ == "__main__":
    raise SystemExit(main())
