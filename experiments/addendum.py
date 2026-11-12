"""Addendum runner: concurrent controls for the prisoner's dilemma and for model drift.

    python experiments/addendum.py --model nemotron --status
    python experiments/addendum.py --model nemotron --wait

Registered as an OSF addendum (docs/preregistration-addendum.md) BEFORE any of this data
existed. Every arm of one model is asked in a single shuffled order, so the arms are collected
at the same time and model drift cannot separate them.

Block P (gpt-oss, Nemotron, Gemini, Mistral Large 4), 100 questions per arm, new seeds MASTER_SEED + 60_000 + k, paraphrase
k % 3, round 1 of the 10-round PD:
  P1  repeated_pd, named                Stage 2A standard wording, no subsidy rule
  P2  repeated_pd_subsidy_0, named      Stage 5's rule stated at tau = 0
  P3  repeated_pd_extreme, disguised    Stage 2C extreme wording, payoffs 2u - 4 (6, 2, -2, -4)
  P4  repeated_pd_extreme_pos, disg.    the same text, payoffs 2u + 1 (11, 7, 3, 1): no losses
Block G (gpt-oss only), 69 questions per arm: the Stage 2A/2C paired seeds MASTER_SEED + k,
k = 0..68, paraphrase k % 3, asked again in both wordings:
  cournot named, cournot_extreme disguised, vickrey named, vickrey_extreme disguised

Same models, settings, schemas, probes, scoring and re-ask rules as Stages 2A-5.
"""
from __future__ import annotations

import argparse
import hashlib
import random
import sys
import time
from dataclasses import replace
from functools import partial
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from config import CAPABILITY_ORDER, MASTER_SEED                       # noqa: E402
from experiments.stage2 import WAIT_S, run_plan, shard, sleep_until, trial_key  # noqa: E402
from games import GAMES, repeated_pd                                   # noqa: E402
from games.extreme import EXTREME_GAMES                                # noqa: E402
from games.probes import PROBES, NumericProbe                          # noqa: E402
from games.subsidy import PROBE as SUBSIDY_PROBE, key_for, spec_for    # noqa: E402

N_P, N_G, N_PARAPHRASES = 100, 69, 3
# Kimi K3 was retired on NVIDIA on 2026-10-15; Mistral Large 4 replaces it (Block P only).
ADDENDUM_MODELS = ["gptoss120b", "nemotron", "gemini_lite", "mistral_large4"]
SEED_P = MASTER_SEED + 60_000          # a block no earlier stage uses (2A 0..137, 2B 1k-3k, 5: 50k)
POS_KEY = "repeated_pd_extreme_pos"
POS_PAYOFFS = dict(T=11.0, R=7.0, P=3.0, S=1.0)    # 2u + 1 of (5, 3, 1, 0)

PREREG = ROOT / "docs" / "preregistration-addendum.md"
PREREG_SHA256: str | None = "74912ffd4ed422fa4879a98dfe2674d32c909425525ea030fc4081b1761160ac"   # locked 2026-11-13 (amended: Kimi K3 retired)


def register() -> None:
    """Make the two new question types runnable (only after the lock check)."""
    base = EXTREME_GAMES["repeated_pd_extreme"]
    GAMES.setdefault(POS_KEY, replace(base, key=POS_KEY,
                                      sampler=partial(repeated_pd.sample, **POS_PAYOFFS)))
    PROBES.setdefault((POS_KEY, "disguised"), PROBES[("repeated_pd_extreme", "disguised")])
    sub = key_for(0.0)
    GAMES.setdefault(sub, spec_for(0.0))
    PROBES.setdefault((sub, "named"), (SUBSIDY_PROBE, NumericProbe,
                                       lambda S=0.0, tau=0.0, **_: S + tau))


def plan(model: str) -> list[tuple]:
    arms = [("repeated_pd", "named"), (key_for(0.0), "named"),
            ("repeated_pd_extreme", "disguised"), (POS_KEY, "disguised")]
    trials = [trial_key(g, f, SEED_P + k, k % N_PARAPHRASES) for g, f in arms for k in range(N_P)]
    if model == "gptoss120b":
        arms_g = [("cournot", "named"), ("cournot_extreme", "disguised"),
                  ("vickrey", "named"), ("vickrey_extreme", "disguised")]
        trials += [trial_key(g, f, MASTER_SEED + k, k % N_PARAPHRASES)
                   for g, f in arms_g for k in range(N_G)]
    random.Random(MASTER_SEED + ord("A")).shuffle(trials)
    return trials


def locked() -> bool:
    return (PREREG_SHA256 is not None and PREREG.exists()
            and hashlib.sha256(PREREG.read_bytes()).hexdigest() == PREREG_SHA256)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, choices=ADDENDUM_MODELS)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--wait", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--shard", default=None, help="i/k: this process asks every k-th question")
    args = ap.parse_args()
    if not locked() and not args.status:
        print("STOP: the addendum is not registered and locked yet (docs/preregistration-addendum.md).")
        return 1
    register()
    out = ROOT / "results" / "raw" / f"addendum_{args.model}.csv"
    while True:
        code = run_plan(args.model, shard(plan(args.model), args.shard), out, limit=args.limit,
                        status=args.status)
        if not (args.wait and code in WAIT_S):
            return code
        wake = time.strftime("%H:%M", time.localtime(time.time() + WAIT_S[code]))
        print(f"waiting until ~{wake}, then resuming.\n", flush=True)
        sleep_until(time.time() + WAIT_S[code])


if __name__ == "__main__":
    raise SystemExit(main())
