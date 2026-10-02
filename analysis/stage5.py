"""The registered Stage 5 analysis (pre-registration 4, Section 3; docs/stage5-design.md).

    python analysis/stage5.py --model nemotron      # real data: locks + that model's Stage 5 complete
    python analysis/stage5.py --pooled              # all four models (Holm across models)
    python analysis/stage5.py --synthetic           # pipeline check on simulated QRE players

Outcome: the cooperation rate in round 1, over counted answers (maths check passed). Per model:

  1. Derived vs guessed theory, at τ = 2.5: |observed − QRE(λ̂)| vs |observed − 100%|. QRE wins
     if its error is smaller; a bootstrap 95% interval for the difference in errors.
  2. The derived mechanism, at τ*: observed within 90 ± 15 (in practice 75–100). "Target
     exceeded" when the 95% interval lies wholly above 90% (the mechanism overpays).
  3. The stage-game halfway point, at τ = 1.5: exact binomial test against 0.5, Holm across
     models in the pooled report.
  4. Calibration: every level against QRE(λ̂), with QRE's own 95% band from λ's posterior.
  Also: τ = 0.0 against Stage 2A's named PD (does the rule line itself shift behaviour?).

Each model's row is then read with docs/interpretation-key.md ("about 50%" = 95% interval
contains 50; "close" = within ±10 points).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import math
import sys
from pathlib import Path

import numpy as np
from scipy.stats import binomtest
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.proportion import proportion_confint, proportions_ztest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from analysis.fit import FITTED_VERDICTS, fit_cell
from analysis.qre import LAMBDA
from config import CAPABILITY_ORDER
from mechanisms.pd import coop_prob

RAW = ROOT / "results" / "raw"
ALPHA = 0.05
BOOT = 10_000
LOCKED = [ROOT / "analysis" / "gate.py", ROOT / "docs" / "decision-gate.md",
          ROOT / "docs" / "interpretation-key.md", ROOT / "docs" / "stage5-design.md"]

# --- the lock: this file (fingerprint line blanked), the gate code and the three documents
STAGE5_ANALYSIS_SHA256 = "a5257d46757fcc1f3c9375436c7f8be26c3416ef8df764a0c573a4b98b42af82"


def fingerprint() -> str:
    text = Path(__file__).read_text(encoding="utf-8")
    body = "\n".join(l for l in text.splitlines() if not l.startswith("STAGE5_ANALYSIS_SHA256 ="))
    h = hashlib.sha256(body.encode())
    for p in LOCKED:
        h.update(b"\0" + p.read_bytes())
    return h.hexdigest()


def stage5_locked() -> bool:
    return STAGE5_ANALYSIS_SHA256 is not None and fingerprint() == STAGE5_ANALYSIS_SHA256


# --- data --------------------------------------------------------------------------------

def tau_of(game_key: str) -> float:
    return float(game_key.rsplit("_", 1)[1].replace("p", "."))


def load_stage5(path: Path) -> dict[float, list[int]]:
    """{τ: [1 if cooperated else 0, ...]} over counted answers."""
    out: dict[float, list[int]] = {}
    with path.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["verdict"] in FITTED_VERDICTS:
                out.setdefault(tau_of(r["game"]), []).append(int(str(r["observed_action"]).strip().upper() == "C"))
    return out


def stage2a_pd(path: Path):
    """Counted named-wording PD answers from Stage 2A: the λ fit and the τ = 0 comparison."""
    from games import GAMES
    rows = []
    with path.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["game"] == "repeated_pd" and r["framing"] == "named" and r["verdict"] in FITTED_VERDICTS:
                rows.append(r)
    obs = [{"game": "repeated_pd", "params": GAMES["repeated_pd"].sampler(seed=int(r["seed"])),
            "framing": "named", "answer": r["observed_action"]} for r in rows]
    coop = [int(str(r["observed_action"]).strip().upper() == "C") for r in rows]
    return fit_cell(obs), coop


# --- statistics ----------------------------------------------------------------------------

def wilson(k: int, n: int) -> tuple[float, float]:
    return tuple(float(x) for x in proportion_confint(k, n, alpha=ALPHA, method="wilson")) if n else (math.nan, math.nan)


def qre_band(fit, tau: float) -> tuple[float, float, float]:
    """QRE cooperation at τ: at the posterior median, and the 95% band over λ's posterior."""
    post = np.exp(fit.log_post)
    keep = post > 1e-12
    ps = np.array([coop_prob(float(l), tau) for l in LAMBDA[keep]])
    w = post[keep] / post[keep].sum()
    order = np.argsort(ps)
    cw = np.cumsum(w[order])
    q = lambda x: float(ps[order][min(np.searchsorted(cw, x), len(ps) - 1)])
    return coop_prob(fit.median, tau), q(0.025), q(0.975)


def error_difference(x: list[int], p_qre: float, seed: int = 0) -> tuple[float, float, float]:
    """|obs − 1| − |obs − QRE| (positive: QRE closer), with a bootstrap 95% interval."""
    x = np.asarray(x)
    f = lambda m: abs(m - 1.0) - abs(m - p_qre)
    rng = np.random.default_rng(seed)
    boots = [f(rng.choice(x, len(x)).mean()) for _ in range(BOOT)]
    return f(x.mean()), float(np.quantile(boots, 0.025)), float(np.quantile(boots, 0.975))


def pct(k: int, n: int) -> str:
    return f"{k / n:.0%} ({k}/{n})" if n else "–"


# --- the report ----------------------------------------------------------------------------

def model_section(name: str, data: dict[float, list[int]], fit, coop_2a: list[int]) -> tuple[list[str], dict]:
    lam = fit.median
    levels = sorted(data)
    derived = [t for t in levels if t not in (0.0, 1.5, 2.5)]
    out = [f"## {name}  (λ̂ = {lam:.3g})", "",
           "| τ | Cooperation [95% CI] | QRE at λ̂ [band] | Classical | Within ±10 of QRE |",
           "|---:|---:|---:|---:|:---:|"]
    row = {"lam": lam}
    for t in levels:
        x = data[t]; k, n = sum(x), len(x)
        lo, hi = wilson(k, n)
        p, plo, phi = qre_band(fit, t)
        classical = "0%" if t < 1 else ("100%" if t > 2 else f"{t - 1:.0%} (mixed)")
        out.append(f"| {t:g} | {pct(k, n)} [{lo:.0%}, {hi:.0%}] | {p:.0%} [{plo:.0%}, {phi:.0%}] | "
                   f"{classical} | {'✅' if n and abs(k / n - p) <= 0.10 else '❌'} |")
        row[t] = (k, n, p)
    out.append("")
    # 1. derived vs guessed theory at 2.5
    if 2.5 in data and data[2.5]:
        d, lo, hi = error_difference(data[2.5], row[2.5][2])
        winner = "QRE" if d > 0 else "classical"
        out.append(f"**Test 1 (τ = 2.5): QRE vs classical.** |obs − 100%| − |obs − QRE| = {100 * d:+.0f} pts "
                   f"[{100 * lo:+.0f}, {100 * hi:+.0f}]: **{winner} is closer**"
                   + (" (interval includes 0)" if lo <= 0 <= hi else "") + ".")
        row["test1"] = winner
    # 2. derived mechanism at τ*
    if derived:
        t = derived[0]; k, n, _ = row[t]; lo, hi = wilson(k, n)
        within = n and 0.75 <= k / n <= 1.0
        exceeded = n and lo > 0.90
        verdict = ("target exceeded: QRE under-predicts responsiveness; the mechanism overpays" if exceeded
                   else ("within 90 ± 15" if within else "**failed** (below 75%, the registered failure line)"))
        out.append(f"**Test 2 (τ* = {t:g}): the derived mechanism.** {pct(k, n)} [{lo:.0%}, {hi:.0%}]: {verdict}.")
        row["test2"] = verdict
    else:
        out.append("**Test 2:** no separate derived level (λ̂ at or above 3.66; decision-gate.md).")
    # 3. halfway point
    if 1.5 in data and data[1.5]:
        k, n = sum(data[1.5]), len(data[1.5])
        p = float(binomtest(k, n, 0.5).pvalue)
        lo, hi = wilson(k, n)
        row["half"] = (k, n, p, lo, hi)
        out.append(f"**Test 3 (τ = 1.5): stage-game halfway point.** {pct(k, n)} [{lo:.0%}, {hi:.0%}], "
                   f"exact binomial p = {p:.3g} against 50%.")
    # line effect
    if 0.0 in data and data[0.0] and coop_2a:
        k1, n1, k2, n2 = sum(data[0.0]), len(data[0.0]), sum(coop_2a), len(coop_2a)
        p = 1.0 if (k1 + k2) in (0, n1 + n2) else float(proportions_ztest([k1, k2], [n1, n2])[1])
        out.append(f"**Rule line at τ = 0.0 vs Stage 2A (no line):** {pct(k1, n1)} vs {pct(k2, n2)}, p = {p:.3g}.")
    out += ["", f"**Reading (docs/interpretation-key.md):** {interpret(row, data)}", ""]
    return out, row


def interpret(row: dict, data: dict) -> str:
    if "half" not in row:
        return "not enough answers."
    k, n, p, lo, hi = row["half"]
    others = [t for t in data if t != 1.5]
    close = all(abs(row[t][0] / row[t][1] - row[t][2]) <= 0.10 for t in others if row[t][1])
    derived = [t for t in data if t not in (0.0, 1.5, 2.5)]
    parts = []
    if lo <= 0.5 <= hi and close:
        parts.append("QRE describes this model")
    elif lo > 0.5:
        parts.append("well above 50% at τ = 1.5: cooperation norm or repeated-game reasoning "
                     "(the reasoning codes decide which)")
    elif hi < 0.5:
        if 2.5 in data and row[2.5][1] and row[2.5][0] / row[2.5][1] < 0.5:
            parts.append("ignores the subsidy")
        else:
            parts.append("defection bias near indifference: rejects QRE, not a sign of recall")
    else:
        parts.append("about 50% at τ = 1.5, but not close to QRE at every other level")
    if derived:
        t = derived[0]; kd, nd, _ = row[t]
        if nd and kd / nd < 0.75:
            parts.append("the derived mechanism failed (if this model's gate fit is poor, read as "
                         "expected under option 3, not as the mechanism failing; decision-gate.md)")
        elif nd and wilson(kd, nd)[0] > 0.90 and 2.5 in data and row[2.5][1] and row[2.5][0] / row[2.5][1] >= 0.90:
            parts.append("the mechanism worked but overpaid")
    return "; ".join(parts) + "."


def report(models: dict, title: str) -> str:
    out = [f"# {title}", ""]
    halves = {}
    for name, (data, fit, coop_2a) in models.items():
        sec, row = model_section(name, data, fit, coop_2a)
        out += sec
        if "half" in row:
            halves[name] = row["half"][2]
    if len(halves) > 1:
        names = list(halves)
        adj = multipletests([halves[m] for m in names], alpha=ALPHA, method="holm")[1]
        out += ["## Test 3 across models (Holm)", "", "| Model | p | Holm p |", "|---|---:|---:|"]
        out += [f"| {m} | {halves[m]:.3g} | {a:.3g} |" for m, a in zip(names, adj)]
    return "\n".join(out)


# --- a pipeline check that needs no Stage 5 data -----------------------------------------------

def synthetic(lam: float, n: int = 100, seed: int = 0):
    """Simulated QRE players at a known λ: every level should sit on the QRE curve."""
    from games.subsidy import derived_level
    rng = np.random.default_rng(seed)
    data = {t: list((rng.random(n) < coop_prob(lam, t)).astype(int)) for t in (0.0, 1.5, 2.5, derived_level(lam))}
    from analysis.fit import CellFit
    from analysis.qre import LOG_LAMBDA
    log_post = -0.5 * ((LOG_LAMBDA - math.log(lam)) / 0.05) ** 2
    log_post -= np.log(np.exp(log_post).sum())
    fit = CellFit(n=137, n_clipped=0, log_post=log_post)
    coop_2a = list((rng.random(137) < coop_prob(lam, 0.0)).astype(int))
    return data, fit, coop_2a


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", choices=CAPABILITY_ORDER)
    ap.add_argument("--pooled", action="store_true")
    ap.add_argument("--synthetic", action="store_true")
    args = ap.parse_args()
    out_dir = ROOT / "results" / "analysis"
    if args.synthetic:
        models = {"synthetic QRE player, λ = 0.154": synthetic(0.154)}
        text, name = report(models, "PIPELINE CHECK ONLY: simulated QRE players (no real Stage 5 data)"), "practice_stage5_synthetic.md"
    else:
        from analysis.lock import analysis_locked
        from experiments.check_stage2 import block_complete
        from experiments.stage5 import plan
        if not (analysis_locked() and stage5_locked()):
            print("STOP: the Stage 5 analysis is not locked yet.")
            return 1
        names = CAPABILITY_ORDER if args.pooled else [args.model]
        if names == [None]:
            ap.error("give --model or --pooled")
        from experiments.stage2 import finished
        missing = [m for m in names if not (RAW / f"stage5_{m}.csv").exists()
                   or finished(RAW / f"stage5_{m}.csv") != set(plan(m)) or not block_complete(m, "2A")]
        if missing:
            print(f"STOP: Stage 5 (or Stage 2A) not complete for {', '.join(missing)}.")
            return 1
        models = {}
        for m in names:
            fit, coop_2a = stage2a_pd(RAW / f"stage2_{m}.csv")
            models[m] = (load_stage5(RAW / f"stage5_{m}.csv"), fit, coop_2a)
        text = report(models, "Stage 5 confirmatory analysis: " + ("all models" if args.pooled else args.model))
        name = f"stage5_{'pooled' if args.pooled else args.model}.md"
    path = out_dir / name
    path.write_text(text + "\n", encoding="utf-8")
    print(text)
    print(f"\nwritten to {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
