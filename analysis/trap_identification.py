"""Exploratory (not registered): what the Stage 2B traps identify about the retrieval share.

Model (paper, Section 3, Theorem 1). In wording w, a share rho_w of answers is retrieved and
equals the textbook answer t; the rest come from a derivation distribution D_w that gives t
with probability q_w. The observed textbook share among kept answers is

    pi_w = rho_w + (1 - rho_w) q_w.

  (i)  With no further assumption:   0 <= rho_w <= pi_w   (sharp).
  (ii) Under derivation invariance (q_s = q_d = q) for twins s, d, with m = min(pi_s, pi_d):
           (pi_w - m) / (1 - m) <= rho_w <= pi_w   for w = s, d,
       jointly parameterised by q in [0, m] via rho_w = (pi_w - q) / (1 - q)  (sharp).

Kept answers are the registered ones (maths check passed), the textbook answer is
analysis/stage2b.py's textbook(), so the counts match the registered Block B tables.
Intervals (a conservative 95% set): the lower endpoint's 2.5% percentile-bootstrap quantile
(resampling answers within each cell) and the exact Clopper-Pearson 97.5% bound on pi_w.

    python analysis/trap_identification.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.stats import beta

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from analysis.stage2b import block_rows, textbook          # noqa: E402
from config import CAPABILITY_ORDER                        # noqa: E402

TRAPS = ["vickrey_trap", "cournot_trap", "repeated_pd_trap", "public_goods_trap"]
B = 20000
rng = np.random.default_rng(20261109)


def lower(pw: float, m: float) -> float:
    return 0.0 if m >= 1 else (pw - m) / (1 - m)


def main() -> None:
    rows = [r for r in block_rows("B", practice=False) if r["kept"]]
    print("| Model | Trap | Standard t/n | Disguised t/n | rho_s set [95%] | rho_d set [95%] |")
    print("|---|---|---:|---:|---|---|")
    for m in CAPABILITY_ORDER:
        for g in TRAPS:
            cell = {fr: [textbook(r) for r in rows if r["model"] == m and r["game"] == g
                         and r["framing"] == fr] for fr in ("named", "disguised")}
            ns, nd = len(cell["named"]), len(cell["disguised"])
            if ns == 0 or nd == 0:
                print(f"| {m} | {g} | {sum(cell['named'])}/{ns} | {sum(cell['disguised'])}/{nd} | – | – |")
                continue
            ks, kd = sum(cell["named"]), sum(cell["disguised"])
            ps, pd = ks / ns, kd / nd
            mm = min(ps, pd)
            bs_s = rng.binomial(ns, ps, B) / ns
            bs_d = rng.binomial(nd, pd, B) / nd
            bm = np.minimum(bs_s, bs_d)
            out = []
            for pw, bw, k, n in ((ps, bs_s, ks, ns), (pd, bs_d, kd, nd)):
                cp = 1.0 if k == n else float(beta.ppf(0.975, k + 1, n - k))
                lo_b = np.where(bm < 1, (bw - bm) / np.where(bm < 1, 1 - bm, 1), 0.0)
                out.append(f"[{lower(pw, mm):.3f}, {pw:.3f}] [{np.quantile(lo_b, 0.025):.3f}, "
                           f"{cp:.3f}]")
            print(f"| {m} | {g} | {ks}/{ns} | {kd}/{nd} | {out[0]} | {out[1]} |")


if __name__ == "__main__":
    main()
