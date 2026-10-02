"""The registered Stage 2C analysis (pre-registration 3, Section 3; docs/analysis-plan-2c.md).

    python analysis/stage2c.py --model nemotron     # real data: locks + 2A and 2C complete
    python analysis/stage2c.py --pooled             # all four models, once all are complete
    python analysis/stage2c.py --synthetic          # pipeline check on made-up 2C answers

Each Stage 2C (extreme) question is paired with the Stage 2A questions that have the same
game, seed and wording index: its normal twin and its disguised twin. A pair is used when
both of its answers count (maths check passed: AT_EQUILIBRIUM or STRATEGIC_GAP).

  * Scoring: every numeric answer, in both stages, goes through the fraction-slip rule
    (analysis/slips.py) and is then compared with that question's equilibrium (±0.5, as
    everywhere else). Uncorrected results -- the recorded verdicts -- are shown beside.
  * Main test: equilibrium play, normal (2A) vs extreme (2C), on pairs. Exact McNemar per
    model and game, Holm across the four games within each model; the paired difference
    (normal − extreme) with a 95% Agresti–Min interval. Pooled across models: the
    Mantel–Haenszel test for matched pairs, which with every pair its own stratum is the
    exact McNemar test on the discordant pairs summed over models; Holm across games.
  * Secondary: the same, disguised (2A) vs extreme.
  * Recognition: NAMES_GAME (analysis/reasoning.py, κ = 1.00), extreme vs disguised,
    exact McNemar per model and game. Exploratory: play when named vs not, within 2C.
  * Fraction slips and conversion slips counted; a secondary main test counts
    conversion slips (right strategy, answer left in the wrong unit) as equilibrium play.
  * λ: 2C answers decoded into the Stage 2A action space and fitted on the Stage 2A
    payoffs, so all four λ are on the Stage 2A scale (see decode() for the PD).

Real Stage 2C data is refused until (a) the Stage 3 analysis lock holds (analysis/lock.py,
which covers qre.py and fit.py), (b) this file, analysis/slips.py and the plan match the
fingerprint below, and (c) the model's Stage 2A and Stage 2C blocks are complete.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import math
import sys
from collections import defaultdict
from pathlib import Path

from scipy.stats import binomtest, fisher_exact
from statsmodels.stats.multitest import multipletests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from analysis.fit import FITTED_VERDICTS, delta_lambda, fit_cell
from analysis.reasoning import code as code_v1
from analysis.slips import corrected, scored
from config import CAPABILITY_ORDER
from games import GAMES

GAMES_2C = ["vickrey", "cournot", "repeated_pd", "public_goods"]
NAMES = {"vickrey": "Vickrey auction", "cournot": "Cournot", "repeated_pd": "Repeated PD",
         "public_goods": "Public goods"}
ALPHA = 0.05
TOL = 0.5
RAW = ROOT / "results" / "raw"
PLAN = ROOT / "docs" / "analysis-plan-2c.md"
SLIPS = ROOT / "analysis" / "slips.py"

# --- the lock: this file (fingerprint line blanked), the slip rule and the plan in words
STAGE2C_ANALYSIS_SHA256 = None


def fingerprint() -> str:
    text = Path(__file__).read_text(encoding="utf-8")
    body = "\n".join(l for l in text.splitlines() if not l.startswith("STAGE2C_ANALYSIS_SHA256 ="))
    return hashlib.sha256(body.encode() + b"\0" + SLIPS.read_bytes() + b"\0"
                          + PLAN.read_bytes()).hexdigest()


def stage2c_locked() -> bool:
    return STAGE2C_ANALYSIS_SHA256 is not None and fingerprint() == STAGE2C_ANALYSIS_SHA256


# --- one answer, scored ----------------------------------------------------------------

def family(game: str) -> str:
    return next(f for f in GAMES_2C if game.startswith(f))


def enrich(r: dict) -> dict:
    """Add everything the comparison needs to one answer row (either stage)."""
    fam = family(r["game"])
    r["fam"] = fam
    r["params"] = GAMES[r["game"]].sampler(seed=int(r["seed"]))
    r["kept"] = r["verdict"] in FITTED_VERDICTS
    r["correct_raw"] = r["verdict"] == "AT_EQUILIBRIUM"
    r["slip"] = False
    if fam == "repeated_pd":
        r["score"] = r["observed_action"]
        r["correct"] = r["correct_raw"]
    else:
        text = r.get("play_reasoning") or ""
        c = corrected(r["observed_action"], text)
        try:
            r["slip"] = c is not None and abs(c - float(r["observed_action"])) > 1e-9
        except (TypeError, ValueError):
            r["slip"] = False
        r["score"] = scored(r["observed_action"], text)
        r["correct"] = (r["kept"] and r["score"] is not None
                        and abs(r["score"] - float(r["equilibrium"])) <= TOL)
    r["correct_strict"] = r["correct"]
    if r["game"].endswith("_extreme") and fam != "repeated_pd" and r["correct"] is not None \
            and r["kept"] and r["score"] is not None:
        _, p2a, _, ans = decode(r)
        r["correct_strict"] = abs(ans - float(p2a["equilibrium"])) <= TOL
    r["names"] = "NAMES_GAME" in code_v1(r)
    r["conversion"] = conversion_slip(r)
    return r


def conversion_slip(r: dict) -> bool:
    """Right strategy, wrong unit (2C only): the offer or amount instead of the number.
    Vickrey: within 0.5 of the prize, or of prize − 5. Cournot: within 0.5 of K/3 (the
    amount A), or of K/3 − 4. Never true for an answer that is already correct."""
    if not r["game"].endswith("_extreme") or r.get("correct") or r.get("score") is None:
        return False
    p, s = r["params"], r["score"]
    if r["fam"] == "vickrey":
        targets = (p["value"], p["value"] - 5)
    elif r["fam"] == "cournot":
        targets = (p["K"] / 3, p["K"] / 3 - 4)
    else:
        return False
    return any(abs(s - t) <= TOL for t in targets)


def decode(r: dict):
    """A 2C answer in the Stage 2A action space: (2A game key, 2A params, framing, answer).

    Vickrey offer = 3x + 5; Cournot amount = 2x + 4; public goods contribution =
    endowment − keep. The PD is fitted on the ORIGINAL Stage 2A payoffs. The 2C table is
    2u − 4 of the 2A table, so every payoff difference doubles: λ·(2Δu) = (2λ)·Δu, and a
    fit on the original payoffs returns exactly 2 × the λ fitted on the 2C payoffs. That
    is pre-registration 3's "multiplied by 2" (the shift cancels in the logit), done
    without leaving the fixed λ grid. The 2C letters are the 2A disguised letters (same
    seed, same draw), checked here rather than assumed.
    """
    fam, seed = r["fam"], int(r["seed"])
    p2a = GAMES[fam].sampler(seed=seed)
    if fam == "repeated_pd":
        assert (p2a["coop"], p2a["defect"]) == (r["params"]["coop"], r["params"]["defect"])
        return fam, p2a, "disguised", r["score"]
    x = r["score"]
    if fam == "vickrey":
        return fam, p2a, "disguised", 3 * x + 5
    if fam == "cournot":
        return fam, p2a, "disguised", 2 * x + 4
    return fam, p2a, "disguised", r["params"]["endowment"] - x


# --- loading and pairing ---------------------------------------------------------------

def read(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [enrich(r) for r in csv.DictReader(f) if r["verdict"] != "INFRA_FAIL"]


def pairs_for(rows_2a: list[dict], rows_2c: list[dict]) -> dict:
    """{game family: [(normal row, disguised row, extreme row), ...]} -- 2A twins may be
    None if missing; the comparisons below drop a pair whose two compared answers do not
    both count."""
    index = {(r["game"], r["framing"], r["seed"], r["paraphrase_idx"]): r for r in rows_2a}
    out = defaultdict(list)
    for x in rows_2c:
        k = (x["seed"], x["paraphrase_idx"])
        out[x["fam"]].append((index.get((x["fam"], "named") + k),
                              index.get((x["fam"], "disguised") + k), x))
    return out


# --- statistics ------------------------------------------------------------------------

def holm(ps: list[float]) -> list[float]:
    idx = [i for i, p in enumerate(ps) if not math.isnan(p)]
    out = [float("nan")] * len(ps)
    if idx:
        for i, h in zip(idx, multipletests([ps[i] for i in idx], alpha=ALPHA, method="holm")[1]):
            out[i] = float(h)
    return out


def mcnemar_exact(b: int, c: int) -> float:
    """Two-sided exact McNemar: b and c are the two kinds of discordant pair."""
    return 1.0 if b + c == 0 else float(binomtest(b, b + c, 0.5).pvalue)


def paired_diff_ci(n11: int, n10: int, n01: int, n00: int) -> tuple[float, float, float]:
    """Difference first − second in paired proportions, with the Agresti–Min (2005) 95%
    interval: add 0.5 to each of the four cells, then the Wald interval."""
    n = n11 + n10 + n01 + n00
    if n == 0:
        return float("nan"), float("nan"), float("nan")
    d = (n10 - n01) / n
    a10, a01, m = n10 + 0.5, n01 + 0.5, n + 2
    da = (a10 - a01) / m
    se = math.sqrt(max(((a10 + a01) - (a10 - a01) ** 2 / m) / m ** 2, 0.0))
    return d, max(-1.0, da - 1.96 * se), min(1.0, da + 1.96 * se)


def table(pairs, first: str, measure: str):
    """Paired 2×2 counts for `measure` in the first wording vs the extreme one."""
    i = {"normal": 0, "disguised": 1}[first]
    n = [0, 0, 0, 0]                                    # n11, n10, n01, n00
    for t in pairs:
        a, x = t[i], t[2]
        if a is None or not (a["kept"] and x["kept"]):
            continue
        n[{(1, 1): 0, (1, 0): 1, (0, 1): 2, (0, 0): 3}[(int(bool(a[measure])), int(bool(x[measure])))]] += 1
    return n


def pct(k: int, n: int) -> str:
    return f"{k / n:.0%} ({k}/{n})" if n else "–"


def fmt_p(p: float) -> str:
    return "–" if math.isnan(p) else f"{p:.3g}"


def fmt_diff(d, lo, hi) -> str:
    return "–" if math.isnan(d) else f"{100 * d:+.0f} pts [{100 * lo:+.0f}, {100 * hi:+.0f}]"


# --- the report ------------------------------------------------------------------------

def comparison(by_model: dict, first: str, measure: str, title: str) -> list[str]:
    """Per model (Holm across games) and pooled (Holm across games)."""
    lab = {"normal": "Normal (2A)", "disguised": "Disguised (2A)"}[first]
    out = [f"### {title}", "",
           f"| Model | Game | Pairs | {lab} | Extreme (2C) | {first.capitalize()} − extreme [95% CI] | McNemar p | Holm p |",
           "|---|---|---:|---:|---:|---:|---:|---:|"]
    pooled = {g: [0, 0, 0, 0] for g in GAMES_2C}
    for m, pairs in by_model.items():
        lines, ps = [], []
        for g in GAMES_2C:
            n = table(pairs.get(g, []), first, measure)
            pooled[g] = [a + b for a, b in zip(pooled[g], n)]
            tot = sum(n)
            p = mcnemar_exact(n[1], n[2]) if tot else float("nan")
            ps.append(p)
            lines.append((g, tot, pct(n[0] + n[1], tot), pct(n[0] + n[2], tot), paired_diff_ci(*n), p))
        for (g, tot, a, x, ci, p), h in zip(lines, holm(ps)):
            out.append(f"| {m} | {NAMES[g]} | {tot} | {a} | {x} | {fmt_diff(*ci)} | {fmt_p(p)} | {fmt_p(h)} |")
    if len(by_model) > 1:
        ps = [mcnemar_exact(pooled[g][1], pooled[g][2]) if sum(pooled[g]) else float("nan") for g in GAMES_2C]
        for g, p, h in zip(GAMES_2C, ps, holm(ps)):
            n, tot = pooled[g], sum(pooled[g])
            out.append(f"| **all models** | {NAMES[g]} | {tot} | {pct(n[0] + n[1], tot)} | "
                       f"{pct(n[0] + n[2], tot)} | {fmt_diff(*paired_diff_ci(*n))} | {fmt_p(p)} | {fmt_p(h)} |")
    out.append("")
    return out


def counts_section(by_model: dict) -> list[str]:
    out = ["## Which answers count", "",
           "| Model | Game | 2C answered | 2C counted | Normal pairs | Disguised pairs |",
           "|---|---|---:|---:|---:|---:|"]
    for m, pairs in by_model.items():
        for g in GAMES_2C:
            ts = pairs.get(g, [])
            out.append(f"| {m} | {NAMES[g]} | {len(ts)} | {sum(t[2]['kept'] for t in ts)} | "
                       f"{sum(table(ts, 'normal', 'correct'))} | {sum(table(ts, 'disguised', 'correct'))} |")
    return out + [""]


def recognition_section(by_model: dict) -> list[str]:
    out = ["## Recognition: did the model name the game? (`NAMES_GAME`)", "",
           "| Model | Game | Pairs | Disguised (2A) | Extreme (2C) | McNemar p |", "|---|---|---:|---:|---:|---:|"]
    pooled = {g: [0, 0, 0, 0] for g in GAMES_2C}
    for m, pairs in by_model.items():
        for g in GAMES_2C:
            n = table(pairs.get(g, []), "disguised", "names")
            pooled[g] = [a + b for a, b in zip(pooled[g], n)]
            tot = sum(n)
            out.append(f"| {m} | {NAMES[g]} | {tot} | {pct(n[0] + n[1], tot)} | {pct(n[0] + n[2], tot)} | "
                       f"{fmt_p(mcnemar_exact(n[1], n[2]) if tot else float('nan'))} |")
    if len(by_model) > 1:
        for g in GAMES_2C:
            n, tot = pooled[g], sum(pooled[g])
            out.append(f"| **all models** | {NAMES[g]} | {tot} | {pct(n[0] + n[1], tot)} | "
                       f"{pct(n[0] + n[2], tot)} | {fmt_p(mcnemar_exact(n[1], n[2]) if tot else float('nan'))} |")
    out += ["", "### Exploratory: equilibrium play within the extreme wording, named vs not named", "",
            "| Model | Game | Named the game | Did not | Fisher p (exploratory) |", "|---|---|---:|---:|---:|"]
    for m, pairs in by_model.items():
        for g in GAMES_2C:
            xs = [t[2] for t in pairs.get(g, []) if t[2]["kept"]]
            a = [x for x in xs if x["names"]]
            b = [x for x in xs if not x["names"]]
            ka, kb = sum(x["correct"] for x in a), sum(x["correct"] for x in b)
            p = (float(fisher_exact([[ka, len(a) - ka], [kb, len(b) - kb]])[1])
                 if a and b else float("nan"))
            out.append(f"| {m} | {NAMES[g]} | {pct(ka, len(a))} | {pct(kb, len(b))} | {fmt_p(p)} |")
    return out + [""]


def slips_section(by_model: dict) -> list[str]:
    out = ["## Fraction slips corrected (counted answers)", "",
           "| Model | Game | Normal (2A) | Disguised (2A) | Extreme (2C) |", "|---|---|---:|---:|---:|"]
    for m, pairs in by_model.items():
        for g in ("vickrey", "cournot", "public_goods"):
            ts = pairs.get(g, [])
            cells = []
            for i in range(3):
                rs = [t[i] for t in ts if t[i] is not None and t[i]["kept"]]
                cells.append(pct(sum(r["slip"] for r in rs), len(rs)))
            out.append(f"| {m} | {NAMES[g]} | " + " | ".join(cells) + " |")
    out += ["", "## Conversion slips (extreme only: right strategy, answer in the wrong unit)", "",
            "| Model | Game | Counted 2C answers | Conversion slips | Missed answers that are conversion slips |",
            "|---|---|---:|---:|---:|"]
    for m, pairs in by_model.items():
        for g in ("vickrey", "cournot"):
            xs = [t[2] for t in pairs.get(g, []) if t[2]["kept"]]
            miss = [x for x in xs if not x["correct"]]
            k = sum(x["conversion"] for x in xs)
            out.append(f"| {m} | {NAMES[g]} | {len(xs)} | {pct(k, len(xs))} | {pct(k, len(miss))} |")
    return out + [""]


def lambda_section(by_model: dict) -> list[str]:
    out = ["## λ on the Stage 2A scale (paired counted answers, slip-corrected)", "",
           "| Model | Game | λ normal (2A) | λ extreme (2C, decoded) | Δλ = normal − extreme |",
           "|---|---|---|---|---|"]
    for m, pairs in by_model.items():
        for g in GAMES_2C:
            ts = [t for t in pairs.get(g, []) if t[0] is not None and t[0]["kept"] and t[2]["kept"]
                  and t[0]["score"] is not None and t[2]["score"] is not None]
            if not ts:
                out.append(f"| {m} | {NAMES[g]} | – | – | not enough answers |")
                continue
            normal = [{"game": g, "params": t[0]["params"], "framing": "named", "answer": t[0]["score"]}
                      for t in ts]
            extreme = []
            for t in ts:
                key, p2a, fr, ans = decode(t[2])
                extreme.append({"game": key, "params": p2a, "framing": fr, "answer": ans})
            fn, fx = fit_cell(normal), fit_cell(extreme)
            out.append(f"| {m} | {NAMES[g]} | {fn.summary()} | {fx.summary()} | "
                       f"{delta_lambda(fn, fx).summary()} |")
    return out + [""]


PREDICTIONS = [
    # (game, measure, low, high, text) -- pre-registration 3, Section 2, all models pooled
    ("vickrey", "names", 0.85, 0.95, "recognition ~90% (85–95)"),
    ("cournot", "names", 0.20, 0.35, "recognition ~25% (20–35)"),
    ("repeated_pd", "names", 0.45, 0.65, "recognition ~55% (45–65)"),
    ("public_goods", "names", 0.90, 1.00, "recognition ~95% (90–100)"),
]
DROPS = {   # normal − extreme, points
    "vickrey": (0.05, 0.15, "play ~10 points lower than normal"),
    "cournot": (0.35, 0.45, "play 35–45 points lower than normal"),
    "public_goods": (-0.05, 0.05, "play within ±5 points of normal"),
}
COURNOT_BY_MODEL = {"nemotron": (0.35, 1.0, "≥ 35"), "gemini_lite": (0.20, 0.35, "20–35"),
                    "kimi": (-1.0, 0.15, "≤ 15"), "gptoss120b": (-1.0, 0.15, "≤ 15")}


def predictions_section(by_model: dict) -> list[str]:
    """A mechanical check of each committed prediction against the pooled result."""
    def pooled(g, first, measure):
        n = [0, 0, 0, 0]
        for pairs in by_model.values():
            n = [a + b for a, b in zip(n, table(pairs.get(g, []), first, measure))]
        return n

    hit = lambda v, lo, hi: "✅ met" if lo - 1e-9 <= v <= hi + 1e-9 else "❌ not met"
    scope = ("all models pooled unless stated" if len(by_model) > 1 else
             "THIS MODEL ONLY; the registered check is the pooled report")
    out = [f"## Predictions vs results ({scope})", "",
           "| Prediction | Result | Verdict |", "|---|---|---|"]
    for g, measure, lo, hi, text in PREDICTIONS:
        n = pooled(g, "disguised", "names")
        tot = sum(n)
        v = (n[0] + n[2]) / tot if tot else float("nan")
        out.append(f"| {NAMES[g]}: {text} | {pct(n[0] + n[2], tot)} | {hit(v, lo, hi) if tot else '–'} |")
    for g, (lo, hi, text) in DROPS.items():
        n = pooled(g, "normal", "correct")
        tot = sum(n)
        d = (n[1] - n[2]) / tot if tot else float("nan")
        out.append(f"| {NAMES[g]}: {text} | {100 * d:+.0f} pts | {hit(d, lo, hi) if tot else '–'} |")
    nn, nd = pooled("repeated_pd", "normal", "correct"), pooled("repeated_pd", "disguised", "correct")
    if sum(nn) and sum(nd):
        x = (nn[0] + nn[2]) / sum(nn)
        ok = 0.80 <= x <= 0.90 and nn[2] > nn[1] and nd[2] >= nd[1]
        out.append(f"| Repeated PD: extreme play 80–90%, above normal, at or above disguised | "
                   f"{x:.0%}; normal − extreme {100 * (nn[1] - nn[2]) / sum(nn):+.0f} pts, "
                   f"disguised − extreme {100 * (nd[1] - nd[2]) / sum(nd):+.0f} pts | "
                   f"{'✅ met' if ok else '❌ not met'} |")
    for m, (lo, hi, text) in COURNOT_BY_MODEL.items():
        if m not in by_model:
            continue
        n = table(by_model[m].get("cournot", []), "normal", "correct")
        tot = sum(n)
        d = (n[1] - n[2]) / tot if tot else float("nan")
        out.append(f"| Cournot drop, {m}: {text} points | {100 * d:+.0f} pts | {hit(d, lo, hi) if tot else '–'} |")
    out += ["", "_Ranges are read inclusively. Conversion-slip share of each drop: see the "
            "conversion-slip table (predicted 5–15 points of the Cournot and Vickrey drops)._", ""]
    return out


def report(by_model: dict, title: str) -> str:
    out = [f"# {title}", ""]
    out += counts_section(by_model)
    out += ["## Main test: equilibrium play, normal (2A) vs extreme (2C)", ""]
    out += comparison(by_model, "normal", "correct", "Fraction-slip corrected (registered)")
    out += comparison(by_model, "normal", "correct_raw", "Uncorrected (recorded verdicts), for comparison")
    out += comparison(by_model, "normal", "conv_ok", "Secondary: conversion slips counted as equilibrium play")
    out += comparison(by_model, "normal", "correct_strict",
                      "Sensitivity (not registered): extreme answers judged with the Stage 2A "
                      "tolerance after decoding (±0.5 on the offer, amount or contribution)")
    out += ["## Secondary: disguised (2A) vs extreme (2C)", ""]
    out += comparison(by_model, "disguised", "correct", "Fraction-slip corrected")
    out += recognition_section(by_model)
    out += slips_section(by_model)
    out += lambda_section(by_model)
    out += predictions_section(by_model)
    return "\n".join(out)


def model_pairs(rows_2a: list[dict], rows_2c: list[dict]) -> dict:
    for r in rows_2a + rows_2c:
        r["conv_ok"] = r["correct"] or r["conversion"]
    return pairs_for(rows_2a, rows_2c)


# --- a pipeline check that needs no Stage 2C data --------------------------------------

def synthetic_2c(rows_2a: list[dict]) -> list[dict]:
    """Made-up extreme answers: each normal-wording 2A answer, encoded into the extreme
    question's units with the same reasoning text. The comparison must then show no
    difference at all, and λ(extreme) must equal λ(normal) -- a check of the pairing,
    the decoding and the scoring, run on data already analysed (Stage 2A)."""
    out = []
    for r in rows_2a:
        if r["framing"] != "named":
            continue
        fam, key = r["fam"], r["fam"] + "_extreme"
        s = dict(r, game=key, framing="disguised")
        p = GAMES[key].sampler(seed=int(r["seed"]))
        s["equilibrium"] = p["equilibrium"]
        if fam == "repeated_pd":
            s["observed_action"] = p["coop"] if str(r["observed_action"]).upper() == "C" else p["defect"]
        elif r["score"] is not None:
            x = {"vickrey": lambda v: (v - 5) / 3, "cournot": lambda v: (v - 4) / 2,
                 "public_goods": lambda v: p["endowment"] - v}[fam](r["score"])
            s["observed_action"] = x
            s["play_reasoning"] = ""           # the slip rule already applied on the 2A side
        if r["kept"]:
            s["verdict"] = "AT_EQUILIBRIUM" if r["correct"] else "STRATEGIC_GAP"
        out.append(enrich({k: v for k, v in s.items() if k not in
                           ("fam", "params", "kept", "correct_raw", "slip", "score", "correct",
                            "correct_strict", "names", "conversion", "conv_ok")}))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", choices=CAPABILITY_ORDER)
    ap.add_argument("--pooled", action="store_true")
    ap.add_argument("--synthetic", action="store_true")
    args = ap.parse_args()
    out_dir = ROOT / "results" / "analysis"

    if args.synthetic:
        rows_2a = read(RAW / "stage2_nemotron.csv")
        by_model = {"nemotron (synthetic 2C)": model_pairs(rows_2a, synthetic_2c(rows_2a))}
        text = report(by_model, "PIPELINE CHECK ONLY: made-up Stage 2C answers built from "
                                "Nemotron's Stage 2A normal answers (no real Stage 2C data)")
        path = out_dir / "practice_stage2c_synthetic.md"
    else:
        from analysis.lock import analysis_locked
        from experiments.check_stage2 import block_complete
        if not (analysis_locked() and stage2c_locked()):
            print("STOP: the Stage 2C analysis is not locked yet.")
            return 1
        models = CAPABILITY_ORDER if args.pooled else [args.model]
        if not models or models == [None]:
            ap.error("give --model or --pooled")
        missing = [m for m in models if not (block_complete(m, "2A") and block_complete(m, "2C"))]
        if missing:
            print(f"STOP: Stage 2A or 2C not complete for {', '.join(missing)}.")
            return 1
        by_model = {m: model_pairs(read(RAW / f"stage2_{m}.csv"), read(RAW / f"stage2c_{m}.csv"))
                    for m in models}
        text = report(by_model, "Stage 2C confirmatory analysis: " + ("all models" if args.pooled else args.model))
        path = out_dir / f"stage2c_{'pooled' if args.pooled else args.model}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text + "\n", encoding="utf-8")
    print(text)
    print(f"\nwritten to {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
