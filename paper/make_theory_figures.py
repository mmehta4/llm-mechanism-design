"""Theory figures for the paper (no data): the PD subsidy curves and the reserve r*(λ).

    python paper/make_theory_figures.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mechanisms.auction import myerson_reserve, optimal_reserve
from mechanisms.pd import coop_prob

OUT = ROOT / "paper" / "figures"
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "font.family": "serif"})


def subsidy_curves():
    taus = np.linspace(0, 20, 401)
    fig, ax = plt.subplots(figsize=(3.4, 2.9))
    for lam, style in [(0.154, "-"), (0.5, "--"), (2.0, "-.")]:
        ax.plot(taus, [coop_prob(lam, t) for t in taus], style, lw=1.3,
                label=fr"QRE, $\lambda={lam:g}$" + (" (Nemotron)" if lam == 0.154 else ""))
    rational = np.clip(taus - 1, 0, 1)
    ax.plot(taus, rational, color="k", lw=1.0, alpha=0.6, label=r"rational ($\lambda\to\infty$)")
    ax.plot([1.5], [0.5], "o", color="k", ms=4)
    ax.annotate("$\\tau=1.5$:\n50% at every $\\lambda$", xy=(1.5, 0.5), xytext=(3.2, 0.12),
                arrowprops=dict(arrowstyle="->", lw=0.7), fontsize=8)
    ax.axvline(16.2, color="grey", lw=0.6, ls=":")
    ax.text(16.4, 0.05, r"$\tau^*$ for 90%" "\n" r"at $\lambda=0.154$", fontsize=7, color="grey")
    ax.set_xlabel(r"cooperation subsidy $\tau$")
    ax.set_ylabel("cooperation rate (round 1)")
    ax.set_ylim(0, 1.02)
    ax.legend(frameon=False, fontsize=7, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2)
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"subsidy_curves.{ext}", dpi=200)


def reserve_curve():
    lams = np.exp(np.linspace(np.log(0.01), np.log(100), 15))
    rs = [optimal_reserve(float(l), grid=np.arange(0, 100.5, 0.5))[0] for l in lams]
    fig, ax = plt.subplots(figsize=(3.4, 2.4))
    ax.semilogx(lams, rs, "o-", ms=3, lw=1.2, label=r"revenue-optimal reserve $r^*(\lambda)$")
    ax.axhline(myerson_reserve(), color="k", lw=0.8, ls="--", label="Myerson (rational): 50")
    ax.set_xlabel(r"bidder precision $\lambda$ (log scale)")
    ax.set_ylabel("reserve price")
    ax.legend(frameon=False, fontsize=7)
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"reserve_curve.{ext}", dpi=200)
    return list(zip(lams.round(3), rs))


if __name__ == "__main__":
    subsidy_curves()
    if "--subsidy-only" not in sys.argv:
        print(reserve_curve())
