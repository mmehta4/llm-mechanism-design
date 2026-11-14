"""The registered addendum analysis (docs/preregistration-addendum.md, Section 3; osf.io/ujvpx).

    python analysis/addendum.py               # real data, once every model is complete
    python analysis/addendum.py --synthetic   # pipeline check on made-up answers

Written and committed while collection was still running, before any result was looked at.

Block P (per model, 100 questions per arm): defection in round 1 among answers that count
(maths check passed: AT_EQUILIBRIUM or STRATEGIC_GAP; in the finitely repeated PD the
equilibrium action is defection).
  * C1 = P2 − P1 (stating the rule), C2 = P3 − P4 (loss framing), C3 = P4 − P1 (frame and
    story removed, payoffs positive), C4 = P3 − P1 (concurrent replication of Stage 2C).
  * Two-sided Fisher exact tests. Holm across the four models within each of C1–C3, and
    across the three models with earlier data for C4.
  * Pooled: Cochran–Mantel–Haenszel test stratified by model, with the Mantel–Haenszel
    risk difference.
  * Differences with 95% Newcombe (hybrid score, method 10) intervals.

Block G (gpt-oss): equilibrium play, standard vs extreme on pairs with the same seed and
wording index, exact McNemar; the Stage 2C fraction-slip rule; the registered tolerance and
the matched tolerance (±0.5 after decoding). Descriptive comparison with the original Stage
2A/2C answers on the same seeds.

Then the author's predictions (Section 4) are scored mechanically: ranges are checked as
stated; for a point prediction ("about +20") the table shows whether it lies inside the 95%
interval and whether the sign is right.
"""
from __future__ import annotations

import argparse
import csv
import math
import random
import sys
from collections import defaultdict
from pathlib import Path

from scipy.stats import chi2, fisher_exact
from statsmodels.stats.contingency_tables import StratifiedTable

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from experiments.addendum import (ADDENDUM_MODELS, N_G, N_P, POS_KEY, locked, plan,  # noqa: E402
                                  register)

register()                                    # the two new question types must exist first
from analysis.stage2c import (enrich, holm, mcnemar_exact, paired_diff_ci,  # noqa: E402
                              read)

RAW = ROOT / "results" / "raw"
OUT = ROOT / "results" / "analysis" / "addendum.md"
SUB0 = "repeated_pd_subsidy_0"
ARMS = {"P1": ("repeated_pd", "named"), "P2": (SUB0, "named"),
        "P3": ("repeated_pd_extreme", "disguised"), "P4": (POS_KEY, "disguised")}
CONTRASTS = {"C1": ("P2", "P1", "stating the rule"),
             "C2": ("P3", "P4", "loss framing"),
             "C3": ("P4", "P1", "frame and story removed, payoffs positive"),
             "C4": ("P3", "P1", "concurrent replication of the Stage 2C shift")}
EARLIER = ["gptoss120b", "nemotron", "gemini_lite"]          # models with Stage 2A-5 data
LABEL = {"gptoss120b": "gpt-oss-120b", "nemotron": "Nemotron 3 Ultra",
         "gemini_lite": "Gemini 3.5 Flash Lite", "mistral_large4": "Mistral Large 4"}
G_GAMES = ["cournot", "vickrey"]

# --- Section 4 of the addendum, as written before filing (Kimi K3 is not run, so omitted) ---
ARM_PRED = {  # model: {arm: (point, lo, hi)} in percent
    "gptoss120b": {"P1": (70, 60, 80), "P2": (90, 82, 97), "P3": (86, 78, 94), "P4": (85, 77, 93)},
    "nemotron": {"P1": (60, 50, 70), "P2": (82, 72, 90), "P3": (93, 86, 98), "P4": (92, 85, 98)},
    "gemini_lite": {"P1": (9, 3, 17), "P2": (6, 2, 13), "P3": (85, 77, 92), "P4": (83, 75, 91)},
}
C_POINT = {"C1": {"gptoss120b": 20, "nemotron": 22, "gemini_lite": 0},
           "C3": {"gptoss120b": 15, "nemotron": 32, "gemini_lite": 74},
           "C4": {"gptoss120b": 16, "nemotron": 33, "gemini_lite": 76}}


# --- statistics ------------------------------------------------------------------------

def wilson(k: int, n: int, z: float = 1.959964) -> tuple[float, float]:
    if n == 0:
        return float("nan"), float("nan")
    p = k / n
    c = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    m = (p + z * z / (2 * n)) / (1 + z * z / n)
    return m - c, m + c


def newcombe(k1: int, n1: int, k2: int, n2: int) -> tuple[float, float, float]:
    """p1 − p2 with the Newcombe (1998) hybrid score interval (method 10)."""
    if not (n1 and n2):
        return float("nan"), float("nan"), float("nan")
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = wilson(k1, n1)
    l2, u2 = wilson(k2, n2)
    d = p1 - p2
    return (d, d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2),
            d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2))


def fisher_p(k1: int, n1: int, k2: int, n2: int) -> float:
    if not (n1 and n2):
        return float("nan")
    return float(fisher_exact([[k1, n1 - k1], [k2, n2 - k2]])[1])


def cmh(cells: list[tuple[int, int, int, int]]) -> tuple[float, float]:
    """(Mantel–Haenszel risk difference, CMH p) over strata (k1, n1, k2, n2)."""
    cells = [c for c in cells if c[1] and c[3]]
    if not cells:
        return float("nan"), float("nan")
    w = [n1 * n2 / (n1 + n2) for _, n1, _, n2 in cells]
    rd = sum(wi * (k1 / n1 - k2 / n2) for wi, (k1, n1, k2, n2) in zip(w, cells)) / sum(w)
    tabs = [[[k1, n1 - k1], [k2, n2 - k2]] for k1, n1, k2, n2 in cells]
    try:
        # the p-value from the statistic: statsmodels' own pvalue underflows to 0 below ~1e-16
        p = float(chi2.sf(StratifiedTable(tabs).test_null_odds(correction=False).statistic, 1))
    except Exception:                                       # degenerate (all-0 or all-1) strata
        p = float("nan")
    return rd, p


# --- formatting ------------------------------------------------------------------------

def pct(k: int, n: int) -> str:
    return f"{100 * k / n:.0f}% ({k}/{n})" if n else "–"


def pts(x: float) -> str:
    return "–" if math.isnan(x) else f"{100 * x:+.0f}"


def ci(lo: float, hi: float) -> str:
    return "–" if math.isnan(lo) else f"[{100 * lo:+.0f}, {100 * hi:+.0f}]"


def fp(p: float) -> str:
    if math.isnan(p):
        return "–"
    return f"{p:.1e}" if p < 1e-3 else f"{p:.3f}"


def yes(b: bool | None) -> str:
    return "–" if b is None else ("yes" if b else "**no**")


# --- loading ---------------------------------------------------------------------------

def complete(model: str, rows: list[dict]) -> bool:
    have = {(r["game"], r["framing"], int(r["seed"]), int(r["paraphrase_idx"])) for r in rows}
    return all(t in have for t in plan(model))


def arm_counts(rows: list[dict]) -> dict:
    out = {}
    for arm, (g, f) in ARMS.items():
        kept = [r for r in rows if r["game"] == g and r["framing"] == f and r["kept"]]
        asked = [r for r in rows if r["game"] == g and r["framing"] == f]
        out[arm] = (sum(r["verdict"] == "AT_EQUILIBRIUM" for r in kept), len(kept), len(asked))
    return out


# --- sections --------------------------------------------------------------------------

def block_p(by_model: dict) -> tuple[list[str], dict]:
    counts = {m: arm_counts(rs) for m, rs in by_model.items()}
    out = ["## Block P: defection in round 1", "",
           "Defection among answers that count (maths check passed). In brackets: answers that "
           "count / questions asked.", "",
           "| Model | P1 standard | P2 + rule at τ = 0 | P3 extreme, losses | P4 extreme, positive |",
           "|---|---|---|---|---|"]
    for m, c in counts.items():
        out.append(f"| {LABEL[m]} | " + " | ".join(
            f"{pct(c[a][0], c[a][1])} of {c[a][2]}" for a in ARMS) + " |")
    res = defaultdict(dict)
    for name, (a, b, what) in CONTRASTS.items():
        models = [m for m in counts if name != "C4" or m in EARLIER]
        ps = [fisher_p(counts[m][a][0], counts[m][a][1], counts[m][b][0], counts[m][b][1])
              for m in models]
        out += ["", f"### {name} = {a} − {b}: {what}", "",
                "| Model | Difference (points) | 95% Newcombe | Fisher p | Holm p |",
                "|---|---|---|---|---|"]
        for m, p, h in zip(models, ps, holm(ps)):
            d, lo, hi = newcombe(counts[m][a][0], counts[m][a][1], counts[m][b][0], counts[m][b][1])
            res[name][m] = dict(d=d, lo=lo, hi=hi, p=p, holm=h)
            out.append(f"| {LABEL[m]} | {pts(d)} | {ci(lo, hi)} | {fp(p)} | {fp(h)} |")
        rd, p = cmh([(counts[m][a][0], counts[m][a][1], counts[m][b][0], counts[m][b][1])
                     for m in models])
        res[name]["pooled"] = dict(d=rd, p=p)
        out.append(f"| Pooled (CMH, MH risk difference) | {pts(rd)} | | {fp(p)} | |")
    return out, dict(counts=counts, contrasts=res)


def g_pairs(rows: list[dict]) -> dict:
    """{game: [(standard row, extreme row)]} on the same seed and wording index."""
    idx = {(r["game"], r["seed"], r["paraphrase_idx"]): r for r in rows}
    return {g: [(r, idx.get((f"{g}_extreme", r["seed"], r["paraphrase_idx"])))
                for r in rows if r["game"] == g and r["framing"] == "named"] for g in G_GAMES}


def g_table(pairs, measure: str) -> list[int]:
    n = [0, 0, 0, 0]
    for a, x in pairs:
        if a is None or x is None or not (a["kept"] and x["kept"]):
            continue
        n[{(1, 1): 0, (1, 0): 1, (0, 1): 2, (0, 0): 3}[(int(bool(a[measure])), int(bool(x[measure])))]] += 1
    return n


def original_g() -> dict:
    """The original Stage 2A (named) and Stage 2C answers of gpt-oss on Block G's seeds."""
    a = read(RAW / "stage2_gptoss120b.csv")
    c = read(RAW / "stage2c_gptoss120b.csv")
    return {(r["game"], r["seed"], r["paraphrase_idx"]): r for r in a + c
            if r["fam"] in G_GAMES and (r["framing"] == "named" or r["game"].endswith("_extreme"))}


def block_g(rows: list[dict], orig: dict) -> tuple[list[str], dict]:
    pairs = g_pairs(rows)
    out = ["", "## Block G: gpt-oss, Cournot and Vickrey, standard vs extreme (same seeds)", "",
           "Equilibrium play among answers that count, pairs where both count. Exact McNemar.", "",
           "| Game | Tolerance | Pairs | Standard | Extreme | Difference [95% Agresti–Min] | McNemar p |",
           "|---|---|---|---|---|---|---|"]
    res = {}
    for g in G_GAMES:
        for measure, tol in (("correct", "registered"), ("correct_strict", "matched ±0.5")):
            n11, n10, n01, n00 = g_table(pairs[g], measure)
            tot = n11 + n10 + n01 + n00
            d, lo, hi = paired_diff_ci(n11, n10, n01, n00)
            p = mcnemar_exact(n10, n01) if tot else float("nan")
            res[(g, measure)] = dict(std=(n11 + n10) / tot if tot else float("nan"),
                                     ext=(n11 + n01) / tot if tot else float("nan"), p=p, n=tot)
            out.append(f"| {g} | {tol} | {tot} | {pct(n11 + n10, tot)} | {pct(n11 + n01, tot)} | "
                       f"{pts(d)} {ci(lo, hi)} | {fp(p)} |")
    out += ["", "Against the original answers on the same seeds and wording (each answer counted "
            "if it passed the maths check; registered tolerance):", "",
            "| Game | Wording | Original (2A / 2C) | Addendum | Same answer type on both |",
            "|---|---|---|---|---|"]
    for g in G_GAMES:
        for gk, label in ((g, "standard"), (f"{g}_extreme", "extreme")):
            now = {(r["seed"], r["paraphrase_idx"]): r for r in rows if r["game"] == gk and r["kept"]}
            was = {k[1:]: r for k, r in orig.items() if k[0] == gk and r["kept"]}
            both = sorted(set(now) & set(was))
            k_was = sum(bool(was[s]["correct"]) for s in both)
            k_now = sum(bool(now[s]["correct"]) for s in both)
            agree = sum(bool(was[s]["correct"]) == bool(now[s]["correct"]) for s in both)
            res[(gk, "orig")] = dict(was=k_was / len(both) if both else float("nan"),
                                     now=k_now / len(both) if both else float("nan"))
            out.append(f"| {g} | {label} | {pct(k_was, len(both))} | {pct(k_now, len(both))} | "
                       f"{pct(agree, len(both))} |")
    return out, res


def predictions(p: dict, g: dict | None) -> list[str]:
    counts, con = p["counts"], p["contrasts"]
    out = ["", "## The author's predictions, scored", "",
           "Written before filing (addendum Section 4). Kimi K3's are not scored (not run); "
           "Mistral Large 4 carries none.", "",
           "### Arm levels (defection, %)", "",
           "| Model | Arm | Predicted [range] | Observed | In range |", "|---|---|---|---|---|"]
    hits = total = 0
    for m, arms in ARM_PRED.items():
        if m not in counts:
            continue
        for arm, (pt, lo, hi) in arms.items():
            k, n, _ = counts[m][arm]
            obs = 100 * k / n if n else float("nan")
            ok = None if math.isnan(obs) else lo <= obs <= hi
            hits += bool(ok)
            total += ok is not None
            out.append(f"| {LABEL[m]} | {arm} | {pt} [{lo}–{hi}] | {obs:.0f} | {yes(ok)} |")
    out += ["", f"{hits} of {total} arm levels fell inside the predicted range.", "",
            "### Contrasts", "",
            "| Prediction | Observed | Held |", "|---|---|---|"]

    def c(name, m):
        return con.get(name, {}).get(m)

    def sig(name, m):
        r = c(name, m)
        return None if r is None or math.isnan(r["holm"]) else r["holm"] < 0.05

    def point_row(name, m, pt):
        r = c(name, m)
        if r is None:
            return
        inside = r["lo"] <= pt / 100 <= r["hi"]
        sign = (r["d"] > 0) == (pt > 0) if pt else abs(r["d"]) < 0.08
        out.append(f"| {name} {LABEL[m]} about {pt:+d} | {pts(r['d'])} {ci(r['lo'], r['hi'])} | "
                   f"sign {yes(sign)}; {pt:+d} inside 95% CI {yes(inside)} |")

    for m in ("gptoss120b", "nemotron"):
        point_row("C1", m, C_POINT["C1"][m])
    if c("C1", "gemini_lite"):
        r = c("C1", "gemini_lite")
        out.append(f"| C1 Gemini ≈ 0, abs(C1) < 8 | {pts(r['d'])} | {yes(abs(r['d']) < 0.08)} |")
    out.append(f"| C1 gpt-oss and Nemotron significant after Holm | "
               f"{fp(c('C1', 'gptoss120b')['holm'])}, {fp(c('C1', 'nemotron')['holm'])} | "
               f"{yes(bool(sig('C1', 'gptoss120b')) and bool(sig('C1', 'nemotron')))} |")
    out.append(f"| C1 pooled CMH significant | p = {fp(con['C1']['pooled']['p'])} | "
               f"{yes(con['C1']['pooled']['p'] < 0.05)} |")
    c2 = [m for m in con["C2"] if m in EARLIER]
    out.append(f"| C2 abs(C2) ≤ 8 for every model | " + ", ".join(pts(con['C2'][m]['d']) for m in c2)
               + f" | {yes(all(abs(con['C2'][m]['d']) <= 0.08 for m in c2))} |")
    out.append(f"| C2 no model significant (Holm) | " + ", ".join(fp(con['C2'][m]['holm']) for m in c2)
               + f" | {yes(not any(sig('C2', m) for m in c2))} |")
    pc2 = con["C2"]["pooled"]
    out.append(f"| C2 pooled CMH not significant, estimate within ±5 | {pts(pc2['d'])}, p = {fp(pc2['p'])} | "
               f"{yes(not pc2['p'] < 0.05 and abs(pc2['d']) <= 0.05)} |")
    for m in EARLIER:
        point_row("C3", m, C_POINT["C3"][m])
    out.append(f"| C3 all positive | " + ", ".join(pts(con['C3'][m]['d']) for m in EARLIER)
               + f" | {yes(all(con['C3'][m]['d'] > 0 for m in EARLIER))} |")
    out.append(f"| C3 Nemotron and Gemini significant after Holm | "
               f"{fp(c('C3', 'nemotron')['holm'])}, {fp(c('C3', 'gemini_lite')['holm'])} | "
               f"{yes(bool(sig('C3', 'nemotron')) and bool(sig('C3', 'gemini_lite')))} |")
    for m in EARLIER:
        r, pt = c("C4", m), C_POINT["C4"][m]
        out.append(f"| C4 {LABEL[m]} within ±10 of Stage 2C's {pt:+d} | {pts(r['d'])} | "
                   f"{yes(abs(100 * r['d'] - pt) <= 10)} |")
    out.append(f"| C4 Nemotron and Gemini significant after Holm | "
               f"{fp(c('C4', 'nemotron')['holm'])}, {fp(c('C4', 'gemini_lite')['holm'])} | "
               f"{yes(bool(sig('C4', 'nemotron')) and bool(sig('C4', 'gemini_lite')))} |")
    out.append(f"| C4 pooled CMH p < 1e-10 | p = {fp(con['C4']['pooled']['p'])} | "
               f"{yes(con['C4']['pooled']['p'] < 1e-10)} |")
    if g:
        rc, rv = g[("cournot", "correct")], g[("vickrey", "correct")]
        out += [f"| G Cournot standard 88–100% | {100 * rc['std']:.0f}% | {yes(0.88 <= rc['std'] <= 1)} |",
                f"| G Cournot extreme 18–45% | {100 * rc['ext']:.0f}% | {yes(0.18 <= rc['ext'] <= 0.45)} |",
                f"| G Vickrey standard ≥ 97% | {100 * rv['std']:.0f}% | {yes(rv['std'] >= 0.97)} |",
                f"| G Vickrey extreme 35–65% | {100 * rv['ext']:.0f}% | {yes(0.35 <= rv['ext'] <= 0.65)} |",
                f"| G McNemar p < 1e-6 for both | {fp(rc['p'])}, {fp(rv['p'])} | "
                f"{yes(rc['p'] < 1e-6 and rv['p'] < 1e-6)} |"]
        for gk in ("cournot", "cournot_extreme", "vickrey", "vickrey_extreme"):
            o = g[(gk, "orig")]
            out.append(f"| G {gk} within ±12 of the original on the same seeds | "
                       f"{100 * o['was']:.0f}% → {100 * o['now']:.0f}% | "
                       f"{yes(abs(o['now'] - o['was']) <= 0.12)} |")
    return out


# --- synthetic check -------------------------------------------------------------------

def synthetic(model: str) -> list[dict]:
    """Made-up answers with the real plan's keys (never written to results/)."""
    rng = random.Random(1)
    rows = []
    for g, f, s, p in (t[:4] for t in plan(model)):
        r = {"game": g, "framing": f, "seed": str(s), "paraphrase_idx": str(p),
             "verdict": rng.choice(["AT_EQUILIBRIUM"] * 3 + ["STRATEGIC_GAP"] * 2 + ["COMPETENCE_GAP"]),
             "observed_action": "", "equilibrium": "", "play_reasoning": "", "probe_reasoning": ""}
        if not g.startswith("repeated_pd"):
            r["equilibrium"] = "10"
            r["observed_action"] = "10" if r["verdict"] == "AT_EQUILIBRIUM" else "12"
        rows.append(enrich(r))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--synthetic", action="store_true")
    args = ap.parse_args()
    if not locked():
        print("STOP: the addendum file does not match its lock.")
        return 1
    by_model = {}
    for m in ADDENDUM_MODELS:
        rows = synthetic(m) if args.synthetic else read(RAW / f"addendum_{m}.csv")
        if not args.synthetic and not complete(m, rows):
            print(f"STOP: {m} is not complete yet.")
            return 1
        by_model[m] = rows
    out = ["# Addendum analysis (osf.io/ujvpx)" + (" — SYNTHETIC CHECK, NOT DATA" if args.synthetic else ""),
           "", "Generated by `analysis/addendum.py`.", ""]
    p_lines, p = block_p(by_model)
    g_lines, g = block_g(by_model["gptoss120b"], {} if args.synthetic else original_g())
    if args.synthetic:
        g = None
    out += p_lines + g_lines + predictions(p, g)
    text = "\n".join(out) + "\n"
    if args.synthetic:
        print(text)
    else:
        OUT.write_text(text, encoding="utf-8")
        print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
