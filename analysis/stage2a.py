"""The registered Stage 2A analysis (pre-registration 1, Section 5), one model at a time.

    python analysis/stage2a.py --model nemotron          # real data: needs the lock
    python analysis/stage2a.py --practice                # Stage 1 practice run only

Per model, for each of the four games:

  * Which answers count: maths check passed (AT_EQUILIBRIUM or STRATEGIC_GAP). The
    excluded share is reported for every cell, never hidden.
  * Main test: share of equilibrium play, normal vs disguised -- two-sided
    two-proportion z-test, Holm-corrected across the four games. Fisher's exact test is
    reported beside it as a robustness check.
  * Public goods, the one predicted null: equivalence test (two one-sided tests)
    against ±13 points at the same corrected threshold.
  * Headline: λ for each wording and Δλ = λ(normal) − λ(disguised), from analysis/fit.py.
  * Wording check: equilibrium share by wording (1, 2, 3) within each framing, set
    against the normal-vs-disguised gap.

Real Stage 2A data is refused until (a) the analysis is locked -- docs/analysis-plan.md
and this code match the fingerprint in analysis/lock.py -- and (b) that model's Stage 2A
block is complete. Fitting real answers with a method that could still be changed is
the analysis equivalent of writing predictions after seeing results.
"""
from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import fisher_exact
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.proportion import proportions_ztest, tost_proportions_2indep

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from analysis.fit import FITTED_VERDICTS, delta_lambda, fit_cell
from games import GAMES

GAMES_2A = ["vickrey", "cournot", "repeated_pd", "public_goods"]
NAMES = {"vickrey": "Vickrey auction", "cournot": "Cournot", "repeated_pd": "Repeated PD",
         "public_goods": "Public goods"}
ALPHA = 0.05
EQUIVALENCE_MARGIN = 0.13          # pre-registration 1, Section 5


def load(path: Path) -> list[dict]:
    """Answered rows (server refusals dropped), with params rebuilt from the seed."""
    rows = []
    with path.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["verdict"] == "INFRA_FAIL":
                continue
            r["params"] = GAMES[r["game"]].sampler(seed=int(r["seed"]))
            rows.append(r)
    return rows


def analyse(rows: list[dict], title: str) -> str:
    cells = defaultdict(list)
    for r in rows:
        cells[(r["game"], r["framing"])].append(r)

    out = [f"# {title}", ""]
    out += ["## Main test: share of equilibrium play, normal vs disguised", "",
            "| Game | Normal | Disguised | Change | z-test p | Holm p | Fisher p | Excluded (n / d) |",
            "|---|---:|---:|---:|---:|---:|---:|---:|"]
    stats, pvals = {}, []
    for g in GAMES_2A:
        s = {}
        for fr in ("named", "disguised"):
            rs = cells[(g, fr)]
            kept = [r for r in rs if r["verdict"] in FITTED_VERDICTS]
            s[fr] = {"n_all": len(rs), "n": len(kept),
                     "eq": sum(r["verdict"] == "AT_EQUILIBRIUM" for r in kept), "kept": kept}
        a, b = s["named"], s["disguised"]
        if a["n"] and b["n"]:
            counts, nobs = np.array([a["eq"], b["eq"]]), np.array([a["n"], b["n"]])
            if counts.sum() in (0, nobs.sum()):
                p = 1.0                       # both cells identical at 0% or 100%
            else:
                p = float(proportions_ztest(counts, nobs)[1])
            fp = float(fisher_exact([[a["eq"], a["n"] - a["eq"]], [b["eq"], b["n"] - b["eq"]]])[1])
        else:
            p = fp = float("nan")
        s["p"], s["fisher"] = p, fp
        stats[g] = s
        pvals.append(p)
    valid = [i for i, p in enumerate(pvals) if not np.isnan(p)]
    holm = [float("nan")] * len(pvals)
    if valid:
        adj = multipletests([pvals[i] for i in valid], alpha=ALPHA, method="holm")[1]
        for i, h in zip(valid, adj):
            holm[i] = float(h)
    for i, g in enumerate(GAMES_2A):
        s = stats[g]
        a, b = s["named"], s["disguised"]
        ra = a["eq"] / a["n"] if a["n"] else float("nan")
        rb = b["eq"] / b["n"] if b["n"] else float("nan")
        exc = f"{a['n_all'] - a['n']} / {b['n_all'] - b['n']}"
        out.append(f"| {NAMES[g]} | {ra:.0%} ({a['eq']}/{a['n']}) | {rb:.0%} ({b['eq']}/{b['n']}) | "
                   f"{100 * (rb - ra):+.0f} pts | {s['p']:.3g} | {holm[i]:.3g} | {s['fisher']:.3g} | {exc} |")
        s["holm"] = holm[i]

    pg = stats["public_goods"]
    a, b = pg["named"], pg["disguised"]
    out += ["", "## Public goods: equivalence test (the predicted null)", ""]
    if a["n"] and b["n"]:
        # .pvalue, not [0]: indexing returned the test statistic, which printed a
        # negative "p" and called a 20-question practice cell equivalent
        tp = float(tost_proportions_2indep(a["eq"], a["n"], b["eq"], b["n"],
                                           -EQUIVALENCE_MARGIN, EQUIVALENCE_MARGIN).pvalue)
        verdict = ("equivalent within ±13 points" if tp < ALPHA
                   else "equivalence NOT shown (the null is not supported)")
        out.append(f"TOST p = {tp:.3g} against ±13 points: **{verdict}**. "
                   f"(Threshold {ALPHA}; the Holm-corrected threshold for this game is "
                   f"applied when the four-game family is reported together.)")
    else:
        out.append("Not enough answers.")

    out += ["", "## Headline: λ and Δλ (quantal response fits)", "",
            "| Game | λ normal | λ disguised | Δλ = normal − disguised |",
            "|---|---|---|---|"]
    for g in GAMES_2A:
        fits = {}
        for fr in ("named", "disguised"):
            obs = [{"game": r["game"], "params": r["params"], "framing": fr,
                    "answer": r["observed_action"]} for r in stats[g][fr]["kept"]]
            fits[fr] = fit_cell(obs) if obs else None
        if fits["named"] and fits["disguised"]:
            d = delta_lambda(fits["named"], fits["disguised"])
            out.append(f"| {NAMES[g]} | {fits['named'].summary()} | "
                       f"{fits['disguised'].summary()} | {d.summary()} |")
        else:
            out.append(f"| {NAMES[g]} | – | – | not enough answers |")

    out += ["", "## Wording check: equilibrium share by wording", "",
            "| Game | Framing | Wording 1 | Wording 2 | Wording 3 | Spread |", "|---|---|---:|---:|---:|---:|"]
    for g in GAMES_2A:
        for fr in ("named", "disguised"):
            shares = []
            for w in ("0", "1", "2"):
                k = [r for r in stats[g][fr]["kept"] if r["paraphrase_idx"] == w]
                shares.append(sum(r["verdict"] == "AT_EQUILIBRIUM" for r in k) / len(k) if k else float("nan"))
            valid_s = [x for x in shares if not np.isnan(x)]
            spread = 100 * (max(valid_s) - min(valid_s)) if valid_s else float("nan")
            pct = lambda x: "–" if np.isnan(x) else f"{x:.0%}"
            out.append(f"| {NAMES[g]} | {fr} | " + " | ".join(pct(x) for x in shares)
                       + (" | – |" if len(valid_s) < 2 else f" | {spread:.0f} pts |"))
    out += ["", "_If the spread between wordings is as large as the normal-vs-disguised change, "
            "the disguise effect for that game is not distinguishable from a wording effect._"]
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model")
    ap.add_argument("--practice", action="store_true",
                    help="run on the Stage 1 practice run (already seen, not confirmatory)")
    args = ap.parse_args()

    if args.practice:
        rows = load(ROOT / "results" / "raw" / "pilot_n20.csv")
        report = analyse(rows, "PRACTICE RUN ONLY: Stage 1, gpt-oss-120b, 20 per cell (not confirmatory)")
        out = ROOT / "results" / "analysis" / "practice_stage2a.md"
    else:
        from analysis.lock import analysis_locked
        from experiments.check_stage2 import block_complete
        if not analysis_locked():
            print("STOP: the analysis is not locked yet (analysis/lock.py). Real Stage 2A "
                  "data is only fitted with a method that can no longer change.")
            return 1
        if not block_complete(args.model, "2A"):
            print(f"STOP: {args.model}'s Stage 2A block is not complete yet.")
            return 1
        rows = load(ROOT / "results" / "raw" / f"stage2_{args.model}.csv")
        report = analyse(rows, f"Stage 2A confirmatory analysis: {args.model}")
        out = ROOT / "results" / "analysis" / f"stage2a_{args.model}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report + "\n", encoding="utf-8")
    print(report)
    print(f"\nwritten to {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
