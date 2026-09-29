"""Stage 1 power analysis: how many trials per cell does Stage 2 need?

The comparison that matters is named vs disguised, within each game. The pilot
gives an at-equilibrium proportion for every cell, so this plans a two-sample test
of proportions, Bonferroni-corrected across the four games.

Three decisions worth stating, because each one changes the answer:

1. POWER FOR THE SMALLEST EFFECT WORTH DETECTING, NOT FOR THE PILOT'S EFFECT.
   Pilot estimates at n=20 are noisy, and the ones that look big enough to act on
   are disproportionately the ones that happened to come out large. Powering on
   them builds that overestimate into the design. The pilot's effects are shown
   below for context only.

2. A PROPORTION IS A PROXY. The pre-registered analysis fits QRE and compares
   lambda. For the continuous games, reducing each trial to "at equilibrium or not"
   throws away how far off it was, so this proportion-based n is CONSERVATIVE --
   the lambda comparison should need fewer trials. Revisit with a simulation once
   the fitting code exists in Stage 3.

3. BONFERRONI, NOT HOLM. Holm is what the pre-registration will actually use, and
   it is uniformly more powerful. Planning under Bonferroni errs on the safe side.
"""
from __future__ import annotations

import csv
import datetime as dt
import math
import sys
from collections import defaultdict
from pathlib import Path

from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

ROOT = Path(__file__).resolve().parent.parent
GAMES = ["vickrey", "cournot", "repeated_pd", "public_goods"]
NICE = {"vickrey": "Vickrey", "cournot": "Cournot",
        "repeated_pd": "Repeated PD", "public_goods": "Public goods"}

FAMILY_ALPHA = 0.05
ALPHA = FAMILY_ALPHA / len(GAMES)
POWER = 0.80
BASELINE = 0.90          # typical named-framing equilibrium rate in the pilot
SOLVER = NormalIndPower()


def cohens_h(p1: float, p2: float) -> float:
    return abs(proportion_effectsize(p1, p2))


def n_for(p1: float, p2: float) -> float:
    h = cohens_h(p1, p2)
    if h == 0:
        return math.inf
    return SOLVER.solve_power(effect_size=h, alpha=ALPHA, power=POWER,
                              ratio=1.0, alternative="two-sided")


def mde_from(baseline: float, n: int) -> float:
    """Smallest DROP from `baseline` detectable at this n, in proportion units."""
    h = SOLVER.solve_power(nobs1=n, alpha=ALPHA, power=POWER,
                           ratio=1.0, alternative="two-sided")
    phi = 2 * math.asin(math.sqrt(baseline)) - h
    return baseline - (math.sin(phi / 2) ** 2 if phi > 0 else 0.0)


def load(path: Path):
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    cells = defaultdict(lambda: [0, 0])
    for r in rows:
        c = cells[(r["game"], r["framing"])]
        c[0] += 1
        c[1] += r["verdict"] == "AT_EQUILIBRIUM"
    stamps = sorted(dt.datetime.fromisoformat(r["timestamp"]) for r in rows)
    minutes = (stamps[-1] - stamps[0]).total_seconds() / 60 if len(stamps) > 1 else 0
    return cells, len(rows), (len(rows) / minutes if minutes else None)


def main(path: str = "results/raw/pilot_n20.csv") -> int:
    cells, total, rate = load(ROOT / path)
    out = []
    w = out.append

    w("# Power analysis — Stage 1\n")
    w(f"Source: `{path}`, {total} trials. Test: two-sample proportions, two-sided. "
      f"α = {FAMILY_ALPHA} Bonferroni-corrected over {len(GAMES)} games → "
      f"**α = {ALPHA:.4f} per game**. Power = {POWER:.0%}.\n")

    w("## 1. What the pilot observed\n")
    w("| Game | Named | Disguised | Difference | Cohen's h |")
    w("|---|---:|---:|---:|---:|")
    observed = {}
    for g in GAMES:
        nn, en = cells[(g, "named")]
        nd, ed = cells[(g, "disguised")]
        pn, pd = en / nn, ed / nd
        observed[g] = (pn, pd)
        w(f"| {NICE[g]} | {pn:.0%} | {pd:.0%} | {(pd - pn) * 100:+.0f} pts | {cohens_h(pn, pd):.2f} |")

    n_pilot = min(c[0] for c in cells.values())
    mde20 = mde_from(BASELINE, n_pilot)
    w(f"\n## 2. What n={n_pilot} could actually detect\n")
    w(f"From a {BASELINE:.0%} baseline, the pilot could only reliably detect a drop of "
      f"**{mde20 * 100:.0f} percentage points** or more.\n")
    w("So Cournot's 40-point shift and the Prisoner's Dilemma's 95-point shift were "
      "both inside what the pilot could see. **Vickrey (−10) and public goods (−5) "
      "were not.** Their small observed shifts are not evidence of *no* framing "
      "effect — an effect of that size was simply undetectable at this sample. "
      "Stage 2 has to settle whether those two games are genuinely null.\n")

    w("## 3. Trials per cell for a given smallest effect of interest\n")
    w(f"Drop from a {BASELINE:.0%} baseline. **n is per cell** — per game per framing.\n")
    w("| Smallest drop worth detecting | Cohen's h | n per cell |")
    w("|---:|---:|---:|")
    grid = {}
    for drop in (0.30, 0.25, 0.20, 0.15, 0.10):
        n = n_for(BASELINE, BASELINE - drop)
        grid[drop] = math.ceil(n)
        w(f"| {drop * 100:.0f} pts | {cohens_h(BASELINE, BASELINE - drop):.2f} | {math.ceil(n)} |")

    w("\n## 4. For context only — n to detect the pilot's own effects\n")
    w("**Do not plan on these.** They inherit the pilot's noise and its tendency to "
      "overstate whichever effects happened to come out large.\n")
    w("| Game | n per cell |")
    w("|---|---:|")
    for g in GAMES:
        n = n_for(*observed[g])
        w(f"| {NICE[g]} | {'∞ (no difference)' if math.isinf(n) else math.ceil(n)} |")

    rec = grid[0.15]
    rec3 = math.ceil(rec / 3) * 3           # divisible across three paraphrases
    trials = rec3 * len(GAMES) * 2
    w("\n## 5. Recommendation\n")
    w(f"**n = {rec3} per cell**, split evenly across the three paraphrases "
      f"({rec3 // 3} each). That detects a 15-point shift from a 90% baseline at "
      f"80% power after correction — enough to settle whether Vickrey and public "
      f"goods are genuinely null, rather than merely undetected.\n")
    w("The paraphrases are spread *within* each cell rather than multiplying it, so "
      "they cost nothing extra in trials — and if wording turns out to matter, that "
      "shows up as variance rather than being averaged away.\n")
    w("**The smallest effect worth detecting is your decision, not mine** — it goes "
      "in `preregistration-1.md` and has to be fixed before Stage 2 runs. 15 points "
      "is a defensible default: smaller than any effect that would change what the "
      "paper claims, large enough to stay affordable.\n")

    w("## 6. Compute\n")
    w(f"{trials} trials per model ({len(GAMES)} games × 2 framings × {rec3}).\n")
    if rate:
        w(f"- **gpt-oss-120b (Groq free tier):** measured {rate:.1f} trials/min in "
          f"the pilot, token-limited → **~{trials / rate / 60:.1f} hours**")
    w(f"- **qwen2.5:7b (local):** ~28 s/trial → ~{trials * 28 / 3600:.1f} hours, "
      f"though at 75% competence failure most trials would be excluded")
    w("- **Gemini (free tier):** rate limits not published; measure in a short pilot first\n")

    w("## 7. Caveats\n")
    w("- Proportions are a proxy; the real analysis compares fitted λ. Conservative "
      "for the continuous games. Re-run as a simulation in Stage 3.")
    w("- The 90% baseline is the pilot's named-framing rate. The PD's named rate is "
      "0%, so its own planning would differ — but that effect is so large it is "
      "detectable at almost any n.")
    w("- Assumes trials are independent. Seeds are shared across paraphrases, so "
      "within a cell trials are paired by parameter draw — a paired analysis "
      "would be slightly more powerful still.")

    text = "\n".join(out) + "\n"
    (ROOT / "results" / "power_analysis.md").write_text(text, encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(*sys.argv[1:]))
