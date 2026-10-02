"""The decision gate (docs/decision-gate.md), and each model's λ̂ for Stage 5.

    python analysis/gate.py                 # all four models; needs every Stage 2A complete
    python analysis/gate.py --practice      # Stage 1 practice run only (gpt-oss, 20 per cell)

Criteria, fixed by the author before three of the four models' fits existed:

  * Good fit (held-out calibration). Per model and game, in the normal wording: fit λ on two
    of the three paraphrases, predict the held-out paraphrase's equilibrium-play rate, and
    count it calibrated if within ±10 points of the observed rate. Rotate the held-out
    paraphrase through all three; the game is calibrated if at least 2 of 3 rotations are.
    The model's fits are good if at least 3 of its 4 games are calibrated.
  * Hard fail: an observed rate no λ ≥ 0 can produce makes that game's fit poor, whatever the
    ±10 rule says (for example PD defection below 50%: QRE cooperation is at most ½).
  * λ is not compared across games (it scales with the payoffs), so option 1 of
    pre-registration 1's gate is untestable; the gate chooses between option 2 (good fits,
    game by game) and option 3 (poor fits).

λ̂ for Stage 5 is the posterior median of the model's Stage 2A named-wording PD fit
(analysis/fit.py), over all counted answers.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from analysis.fit import FITTED_VERDICTS, fit_cell
from analysis.qre import (LAMBDA, cournot_grid, cournot_logprobs, logit_logprobs, pd_coop_prob,
                          pg_grid, pg_utilities, vickrey_grid, vickrey_utilities)
from config import CAPABILITY_ORDER
from games import GAMES

GAMES_2A = ["vickrey", "cournot", "repeated_pd", "public_goods"]
TOL = 0.5
BAND = 0.10
RAW = ROOT / "results" / "raw"


def eq_prob(game: str, params: dict, lam: float) -> float:
    """QRE probability, at precision λ, that one answer counts as equilibrium play
    (within ±0.5 of the equilibrium for numeric games; defection for the PD)."""
    lam_arr = np.array([lam])
    if game == "repeated_pd":
        return float(1 - pd_coop_prob(params["T"], params["R"], params["P"], params["S"], lam_arr)[0])
    if game == "public_goods":
        grid = pg_grid(params)
        lp = logit_logprobs(pg_utilities(params, grid), lam_arr)[0]
    elif game == "cournot":
        grid = cournot_grid(params)
        lp = cournot_logprobs(params, grid, lam_arr)[0]
    else:
        grid = vickrey_grid(params)
        lp = logit_logprobs(vickrey_utilities(params, grid), lam_arr)[0]
    near = np.abs(grid - float(params["equilibrium"])) <= TOL + 1e-9
    return float(np.exp(lp[near]).sum())


def load(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["framing"] == "named" and r["verdict"] in FITTED_VERDICTS:
                r["params"] = GAMES[r["game"]].sampler(seed=int(r["seed"]))
                rows.append(r)
    return rows


def obs(rs):
    return [{"game": r["game"], "params": r["params"], "framing": "named",
             "answer": r["observed_action"]} for r in rs]


def calibration(rows: list[dict], game: str) -> dict:
    rs = [r for r in rows if r["game"] == game]
    rotations = []
    for held in ("0", "1", "2"):
        train = [r for r in rs if r["paraphrase_idx"] != held]
        test = [r for r in rs if r["paraphrase_idx"] == held]
        if not train or not test:
            continue
        lam = fit_cell(obs(train)).median
        predicted = float(np.mean([eq_prob(game, r["params"], lam) for r in test]))
        observed = float(np.mean([r["verdict"] == "AT_EQUILIBRIUM" for r in test]))
        rotations.append({"held": int(held) + 1, "lam": lam, "predicted": predicted,
                          "observed": observed, "ok": abs(predicted - observed) <= BAND + 1e-12})
    observed_all = float(np.mean([r["verdict"] == "AT_EQUILIBRIUM" for r in rs])) if rs else float("nan")
    # the lowest rate QRE can produce is its λ = 0 rate (uniform play); below it, no λ fits
    floor = float(np.mean([eq_prob(game, r["params"], float(LAMBDA[0])) for r in rs])) if rs else float("nan")
    hard_fail = bool(rs) and observed_all < floor - 1e-9
    calibrated = sum(r["ok"] for r in rotations) >= 2 and not hard_fail
    return {"rotations": rotations, "observed": observed_all, "floor": floor,
            "hard_fail": hard_fail, "calibrated": calibrated, "n": len(rs)}


def lambda_hat(rows: list[dict]) -> float:
    return fit_cell(obs([r for r in rows if r["game"] == "repeated_pd"])).median


def report(per_model: dict[str, list[dict]], title: str) -> str:
    out = [f"# {title}", "", "Criteria: `docs/decision-gate.md` (held-out calibration ±10 points; a game "
           "is calibrated in ≥ 2 of 3 rotations; a model's fits are good in ≥ 3 of 4 games).", ""]
    verdicts = {}
    for m, rows in per_model.items():
        out += [f"## {m}", "", "| Game | Held out | λ (trained on the other two) | Predicted | Observed | Within ±10 |",
                "|---|---:|---:|---:|---:|:---:|"]
        good_games = 0
        for g in GAMES_2A:
            c = calibration(rows, g)
            for r in c["rotations"]:
                out.append(f"| {g} | wording {r['held']} | {r['lam']:.3g} | {r['predicted']:.0%} | "
                           f"{r['observed']:.0%} | {'✅' if r['ok'] else '❌'} |")
            note = "hard fail: below what any λ ≥ 0 produces" if c["hard_fail"] else ""
            out.append(f"| **{g}** | | | | **{c['observed']:.0%}** | **{'calibrated' if c['calibrated'] else 'not calibrated'}** {note} |")
            good_games += c["calibrated"]
        good = good_games >= 3
        verdicts[m] = good
        lam = lambda_hat(rows)
        out += ["", f"**Fits: {'GOOD' if good else 'POOR'}** ({good_games}/4 games calibrated). "
                f"Stage 5 λ̂ (named PD, posterior median): **{lam:.3g}**.", ""]
    n_good = sum(verdicts.values())
    option = 2 if n_good == len(verdicts) else (3 if n_good == 0 else None)
    out += ["## Gate", "",
            "λ is not compared across games, so option 1 is untestable (decision-gate.md).", ""]
    if option == 2:
        out.append("**Option 2: fits are good for every model; derive game by game** (the PD subsidy, Stage 5).")
    elif option == 3:
        out.append("**Option 3: fits are poor for every model; Stage 4 studies why.**")
    else:
        out.append("**Mixed:** fits good for " + ", ".join(m for m, v in verdicts.items() if v)
                   + "; poor for " + ", ".join(m for m, v in verdicts.items() if not v)
                   + ". The mixed case follows the rule in docs/decision-gate.md (\"Mixed results\").")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--practice", action="store_true")
    args = ap.parse_args()
    if args.practice:
        per_model = {"gptoss120b (practice)": load(RAW / "pilot_n20.csv")}
        title, name = "PRACTICE ONLY: decision gate on the Stage 1 practice run", "practice_gate.md"
    else:
        from analysis.lock import analysis_locked
        from analysis.stage5 import stage5_locked
        from experiments.check_stage2 import block_complete
        if not (analysis_locked() and stage5_locked()):
            print("STOP: the gate and Stage 5 analysis are not locked yet.")
            return 1
        missing = [m for m in CAPABILITY_ORDER if not block_complete(m, "2A")]
        if missing:
            print(f"STOP: Stage 2A not complete for {', '.join(missing)}.")
            return 1
        per_model = {m: load(RAW / f"stage2_{m}.csv") for m in CAPABILITY_ORDER}
        title, name = "Decision gate (all four models)", "gate.md"
    text = report(per_model, title)
    path = ROOT / "results" / "analysis" / name
    path.write_text(text + "\n", encoding="utf-8")
    print(text)
    print(f"\nwritten to {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
