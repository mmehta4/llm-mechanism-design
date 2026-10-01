"""The registered Stage 2B analysis (pre-registration 2, Section 3; docs/analysis-plan.md §5).

    python analysis/stage2b.py --block B          # real data: needs both locks + all models done
    python analysis/stage2b.py --block B --practice   # the 2B practice round only

Blocks:

  B  traps     per trap: correct share, normal vs disguised, Cochran–Mantel–Haenszel
               across models, Holm across the four traps; per-model two-proportion
               tests as secondary; and the RECALL SIGNATURE -- the share giving the
               textbook (wrong) answer -- tested the same way.
  C  sweep     per game: logistic regression correct ~ wording × size + model; the test
               is the wording × size interaction, Holm across the four games.
  D  effort    gpt-oss: correct ~ wording × effort (low / medium = Stage 2A / high);
               the test is the interaction; maths-check pass rates per effort beside it.
  E  endgame   defection by round and wording; normal vs disguised at each round, Holm
               across the three rounds; trend across rounds within each wording.

Which answers count is the same as Stage 2A (analysis/fit.py: FITTED_VERDICTS), and a
cell where a regression cannot be estimated -- every answer correct, say -- is reported
as such rather than forced.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import sys
import warnings
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.contingency_tables import StratifiedTable
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.proportion import proportions_ztest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from analysis.fit import FITTED_VERDICTS
from config import CAPABILITY_ORDER
from games import GAMES
from games.stress import ENDGAME, SWEEP, SWEEP_LEVELS, TRAPS

ALPHA = 0.05
RAW = ROOT / "results" / "raw"

# --- the second lock: this file, fingerprinted before any Stage 2B data is analysed
STAGE2B_ANALYSIS_SHA256 = "827809323e35901f430f76934cd9e33db06e4369ccfd5a36126957381771c760"


def stage2b_locked() -> bool:
    text = Path(__file__).read_text(encoding="utf-8")
    # the fingerprint covers the file with its own fingerprint line blanked out
    body = "\n".join(l for l in text.splitlines() if not l.startswith("STAGE2B_ANALYSIS_SHA256 ="))
    return (STAGE2B_ANALYSIS_SHA256 is not None
            and hashlib.sha256(body.encode()).hexdigest() == STAGE2B_ANALYSIS_SHA256)


# --- loading -----------------------------------------------------------------------

def load(path: Path, model: str) -> list[dict]:
    rows = []
    if not path.exists():
        return rows
    with path.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["verdict"] == "INFRA_FAIL":
                continue
            r["model"] = model
            r["params"] = GAMES[r["game"]].sampler(seed=int(r["seed"]))
            r["kept"] = r["verdict"] in FITTED_VERDICTS
            r["correct"] = r["verdict"] == "AT_EQUILIBRIUM"
            rows.append(r)
    return rows


def block_rows(block: str, practice: bool) -> list[dict]:
    rows = []
    if block == "D":
        models = ["gptoss120b_low", "gptoss120b_high"]
    else:
        models = CAPABILITY_ORDER
    for m in models:
        name = f"{'practice2b' if practice else 'stage2b'}_{block}_{m}.csv"
        rows += load(RAW / name, m)
    if block == "D":
        # medium effort is Stage 2A's gpt-oss -- the same questions at the default
        for r in load(RAW / ("pilot_n20.csv" if practice else "stage2_gptoss120b.csv"), "gptoss120b"):
            rows.append(r)
    return rows


# --- helpers -----------------------------------------------------------------------

def holm(pvals: list[float]) -> list[float]:
    idx = [i for i, p in enumerate(pvals) if not np.isnan(p)]
    out = [float("nan")] * len(pvals)
    if idx:
        for i, h in zip(idx, multipletests([pvals[i] for i in idx], alpha=ALPHA, method="holm")[1]):
            out[i] = float(h)
    return out


def two_prop(k1: int, n1: int, k2: int, n2: int) -> float:
    if not (n1 and n2):
        return float("nan")
    if (k1 + k2) in (0, n1 + n2):
        return 1.0
    return float(proportions_ztest(np.array([k1, k2]), np.array([n1, n2]))[1])


def cmh(tables: list[np.ndarray]) -> float:
    """Cochran–Mantel–Haenszel p across models (2×2 per model: wording × outcome)."""
    usable = [t for t in tables if t.sum(axis=1).min() > 0]
    if not usable:
        return float("nan")
    # a model whose two cells are both 0% or both 100% carries no information
    usable = [t for t in usable if 0 < t[:, 0].sum() < t.sum()]
    if not usable:
        return 1.0
    return float(StratifiedTable([t.astype(float) + 0.0 for t in usable]).test_null_odds(correction=True).pvalue)


def pct(k: int, n: int) -> str:
    return f"{k / n:.0%} ({k}/{n})" if n else "–"


def logit_interaction(df: pd.DataFrame, formula: str, term: str) -> tuple[float, float, str]:
    """(coefficient, p) of `term`, or a note when the model cannot be estimated."""
    if df.empty or df["y"].nunique() < 2:
        return float("nan"), float("nan"), "not estimable: every answer has the same outcome"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            res = smf.logit(formula, data=df).fit(disp=False, maxiter=200)
        except Exception as e:                       # perfect separation and similar
            return float("nan"), float("nan"), f"not estimable: {type(e).__name__}"
    if term not in res.params:
        return float("nan"), float("nan"), "not estimable: term dropped"
    # Separation (a group all-correct or all-wrong) does not always raise: the fit
    # "converges" to an enormous coefficient with a useless standard error, which
    # prints like a result. Practice data produced +94.7 with p = 1. Flag it instead.
    coef, se = float(res.params[term]), float(res.bse[term])
    if not np.isfinite(se) or abs(coef) > 10 or se > 10:
        return float("nan"), float("nan"), ("not estimable: separation (a group is "
                                            "all-correct or all-wrong); see the table")
    return coef, float(res.pvalues[term]), ""


# --- Block B: traps ----------------------------------------------------------------

def textbook(r: dict) -> bool:
    """Did the answer equal the famous answer that the trap makes WRONG?"""
    p, a = r["params"], r["observed_action"]
    if r["game"] == "repeated_pd_trap":
        defect = "D" if r["framing"] == "named" else p["defect"]
        return str(a).strip().upper() == defect.upper()
    try:
        x = float(a)
    except (TypeError, ValueError):
        return False
    if r["game"] == "vickrey_trap":
        return abs(x - p["value"]) <= 0.5
    if r["game"] == "cournot_trap":
        return abs(x - (p["a"] - p["c"]) / (3 * p["b"])) <= 0.5
    if r["game"] == "public_goods_trap":
        return abs(x) <= 0.5
    return False


def block_b(rows: list[dict]) -> str:
    out = ["## Block B: traps", ""]
    for measure, fn, label in [("correct", lambda r: r["correct"], "Correct (the trap's own answer)"),
                               ("textbook", textbook, "Recall signature: gave the textbook answer")]:
        out += [f"### {label}", "",
                "| Trap | Normal | Disguised | Change | CMH p | Holm p |", "|---|---:|---:|---:|---:|---:|"]
        ps, lines = [], []
        for spec in TRAPS:
            tables, totals = [], {"named": [0, 0], "disguised": [0, 0]}
            for m in CAPABILITY_ORDER:
                t = np.zeros((2, 2), dtype=int)
                for i, fr in enumerate(("named", "disguised")):
                    rs = [r for r in rows if r["model"] == m and r["game"] == spec.key
                          and r["framing"] == fr and r["kept"]]
                    k = sum(fn(r) for r in rs)
                    t[i] = [k, len(rs) - k]
                    totals[fr][0] += k
                    totals[fr][1] += len(rs)
                tables.append(t)
            p = cmh(tables)
            ps.append(p)
            (kn, nn), (kd, nd) = totals["named"], totals["disguised"]
            change = f"{100 * (kd / nd - kn / nn):+.0f} pts" if nn and nd else "–"
            lines.append([spec.key, pct(kn, nn), pct(kd, nd), change, p])
        for line, h in zip(lines, holm(ps)):
            out.append(f"| {line[0]} | {line[1]} | {line[2]} | {line[3]} | {line[4]:.3g} | {h:.3g} |")
        out.append("")
    out += ["### Per model (secondary): correct, normal → disguised", "",
            "| Trap | " + " | ".join(CAPABILITY_ORDER) + " |", "|---|" + "---|" * len(CAPABILITY_ORDER)]
    for spec in TRAPS:
        cells = []
        for m in CAPABILITY_ORDER:
            kn = [r for r in rows if r["model"] == m and r["game"] == spec.key and r["framing"] == "named" and r["kept"]]
            kd = [r for r in rows if r["model"] == m and r["game"] == spec.key and r["framing"] == "disguised" and r["kept"]]
            a, b = sum(r["correct"] for r in kn), sum(r["correct"] for r in kd)
            p = two_prop(a, len(kn), b, len(kd))
            cells.append(f"{pct(a, len(kn))} → {pct(b, len(kd))}, p={p:.2g}" if kn and kd else "–")
        out.append(f"| {spec.key} | " + " | ".join(cells) + " |")
    return "\n".join(out)


# --- Block C: number sweep -----------------------------------------------------------

def block_c(rows: list[dict]) -> str:
    out = ["## Block C: number sweep", "",
           "| Game | Size | Normal | Disguised |", "|---|---|---:|---:|"]
    ps, notes, coefs = [], [], []
    for game, levels in SWEEP.items():
        df_rows = []
        for size, spec in enumerate(levels):
            line = []
            for fr in ("named", "disguised"):
                rs = [r for r in rows if r["game"] == spec.key and r["framing"] == fr and r["kept"]]
                line.append(pct(sum(r["correct"] for r in rs), len(rs)))
                df_rows += [{"y": int(r["correct"]), "disguised": int(fr == "disguised"),
                             "size": size, "model": r["model"]} for r in rs]
            param, values = SWEEP_LEVELS[game]
            out.append(f"| {game} | {param} = {values[size]:g} | {line[0]} | {line[1]} |")
        df = pd.DataFrame(df_rows)
        formula = "y ~ disguised * size" + (" + C(model)" if not df.empty and df["model"].nunique() > 1 else "")
        c, p, note = logit_interaction(df, formula, "disguised:size")
        ps.append(p); notes.append(note); coefs.append(c)
    out += ["", "**Does the wording effect change with size?** (logistic regression, "
            "interaction wording × size, Holm across games)", "",
            "| Game | Interaction (log-odds per size step) | p | Holm p |", "|---|---:|---:|---:|"]
    for game, c, p, h, note in zip(SWEEP, coefs, ps, holm(ps), notes):
        out.append(f"| {game} | {note or f'{c:+.3g}'} | {p:.3g} | {h:.3g} |")
    return "\n".join(out)


# --- Block D: reasoning effort -------------------------------------------------------

EFFORT = {"gptoss120b_low": 0, "gptoss120b": 1, "gptoss120b_high": 2}
EFFORT_NAME = {0: "low", 1: "medium (Stage 2A)", 2: "high"}


def block_d(rows: list[dict]) -> str:
    out = ["## Block D: reasoning effort (gpt-oss)", ""]
    out += ["### Maths-check pass rate by effort (read before the comparison below)", "",
            "| Effort | Answers | Maths check passed | Kept for analysis |", "|---|---:|---:|---:|"]
    for model, e in EFFORT.items():
        rs = [r for r in rows if r["model"] == model]
        passed = sum(r["probe_passed"] == "True" for r in rs)
        kept = sum(r["kept"] for r in rs)
        out.append(f"| {EFFORT_NAME[e]} | {len(rs)} | {pct(passed, len(rs))} | {pct(kept, len(rs))} |")
    out += ["", "### Correct, normal vs disguised, by effort", "",
            "| Game | Effort | Normal | Disguised | Gap |", "|---|---|---:|---:|---:|"]
    ps, notes, coefs = [], [], []
    for game in ("vickrey", "cournot", "repeated_pd", "public_goods"):
        df_rows = []
        for model, e in EFFORT.items():
            line = []
            shares = []
            for fr in ("named", "disguised"):
                rs = [r for r in rows if r["model"] == model and r["game"] == game and r["framing"] == fr and r["kept"]]
                k = sum(r["correct"] for r in rs)
                line.append(pct(k, len(rs)))
                shares.append(k / len(rs) if rs else float("nan"))
                df_rows += [{"y": int(r["correct"]), "disguised": int(fr == "disguised"), "effort": e} for r in rs]
            gap = 100 * (shares[0] - shares[1])
            out.append(f"| {game} | {EFFORT_NAME[e]} | {line[0]} | {line[1]} | {gap:+.0f} pts |")
        c, p, note = logit_interaction(pd.DataFrame(df_rows), "y ~ disguised * effort", "disguised:effort")
        ps.append(p); notes.append(note); coefs.append(c)
    out += ["", "**Does the wording gap change with effort?** (interaction wording × effort, Holm across games)", "",
            "| Game | Interaction | p | Holm p |", "|---|---:|---:|---:|"]
    for game, c, p, h, note in zip(("vickrey", "cournot", "repeated_pd", "public_goods"), coefs, ps, holm(ps), notes):
        out.append(f"| {game} | {note or f'{c:+.3g}'} | {p:.3g} | {h:.3g} |")
    return "\n".join(out)


# --- Block E: PD endgame -------------------------------------------------------------

def defected(r: dict) -> bool:
    defect = "D" if r["framing"] == "named" else r["params"]["defect"]
    return str(r["observed_action"]).strip().upper() == defect.upper()


def block_e(rows: list[dict]) -> str:
    out = ["## Block E: prisoner's dilemma endgame (defection rate)", "",
           "| Round | Normal | Disguised | Difference | p | Holm p |", "|---|---:|---:|---:|---:|---:|"]
    ps, lines = [], []
    for spec in ENDGAME:
        rnd = spec.key.rsplit("round", 1)[1]
        k = {}
        for fr in ("named", "disguised"):
            rs = [r for r in rows if r["game"] == spec.key and r["framing"] == fr and r["kept"]]
            k[fr] = (sum(defected(r) for r in rs), len(rs))
        p = two_prop(*k["named"], *k["disguised"])
        ps.append(p)
        (a, n), (b, m) = k["named"], k["disguised"]
        diff = f"{100 * (a / n - b / m):+.0f} pts" if n and m else "–"
        lines.append([rnd, pct(a, n), pct(b, m), diff, p])
    for line, h in zip(lines, holm(ps)):
        out.append(f"| {line[0]} | {line[1]} | {line[2]} | {line[3]} | {line[4]:.3g} | {h:.3g} |")
    out += ["", "**Trend across rounds 5 → 9 → 10, within each wording** (logistic regression)", "",
            "| Wording | Change in log-odds of defecting per round | p |", "|---|---:|---:|"]
    for fr in ("named", "disguised"):
        df = pd.DataFrame([{"y": int(defected(r)), "round": int(r["game"].rsplit("round", 1)[1])}
                           for r in rows if r["game"].startswith("repeated_pd_round")
                           and r["framing"] == fr and r["kept"]])
        c, p, note = logit_interaction(df, "y ~ round", "round")
        out.append(f"| {fr} | {note or f'{c:+.3g}'} | {p:.3g} |")
    out += ["", "_The pre-registered discriminator: named defection in round 10 minus round 9 "
            "(predicted +10 to +15 points)._"]
    return "\n".join(out)


BLOCKS = {"B": block_b, "C": block_c, "D": block_d, "E": block_e}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--block", required=True, choices=sorted(BLOCKS))
    ap.add_argument("--practice", action="store_true")
    args = ap.parse_args()
    if not args.practice:
        from analysis.lock import analysis_locked
        from experiments.check_stage2 import block_complete
        from experiments.stage2b import BLOCK_MODELS
        if not (analysis_locked() and stage2b_locked()):
            print("STOP: the Stage 2B analysis is not locked yet.")
            return 1
        missing = [m for m in BLOCK_MODELS[args.block] if not block_complete(m, f"2B-{args.block}")]
        if missing:
            print(f"STOP: block {args.block} not complete for {', '.join(missing)}.")
            return 1
    rows = block_rows(args.block, args.practice)
    title = ("PRACTICE ROUND ONLY (not confirmatory)" if args.practice
             else "Stage 2B confirmatory analysis")
    report = f"# {title}\n\n" + BLOCKS[args.block](rows)
    out = ROOT / "results" / "analysis" / f"{'practice_' if args.practice else ''}stage2b_{args.block}.md"
    out.write_text(report + "\n", encoding="utf-8")
    print(report)
    print(f"\nwritten to {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
