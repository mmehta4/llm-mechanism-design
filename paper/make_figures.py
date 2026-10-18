"""Data figures for the paper. Each figure includes only models whose block is complete, so
re-running this as Stage 2 finishes fills the figures in.

    python paper/make_figures.py

Style (dataviz method): wording is the one categorical channel -- normal = slot 1 (blue),
disguised = slot 2 (orange), extreme = slot 3 (aqua), validated all-pairs for colour-vision
deficiency; models are separated by position (small multiples / x position), never by colour.
"""
from __future__ import annotations

import csv
import math
import sys
import textwrap
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np
from statsmodels.stats.proportion import proportion_confint

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from analysis.reasoning import code as code_v1
from analysis.slips import scored
from config import CAPABILITY_ORDER
from experiments.check_stage2 import block_complete
from games import GAMES

OUT = ROOT / "paper" / "figures"
RAW = ROOT / "results" / "raw"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
NAME = {"gptoss120b": "gpt-oss-120b", "nemotron": "Nemotron 3 Ultra", "kimi": "Kimi K3",
        "gemini_lite": "Gemini 3.5 Flash Lite"}
SHORT = {"gptoss120b": "gpt-oss", "nemotron": "Nemotron", "kimi": "Kimi", "gemini_lite": "Gemini"}
GAME_NAME = {"vickrey": "Vickrey auction", "cournot": "Cournot duopoly",
             "repeated_pd": "Repeated PD", "public_goods": "Public goods"}
GAMES4 = list(GAME_NAME)
COUNTED = {"AT_EQUILIBRIUM", "STRATEGIC_GAP"}

plt.rcParams.update({
    "font.family": "serif", "font.size": 8.5, "axes.edgecolor": INK2, "axes.labelcolor": INK,
    "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
    "legend.frameon": False, "savefig.bbox": "tight", "savefig.pad_inches": 0.03,
})


def read(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["verdict"] != "INFRA_FAIL"]


def save(fig, name: str) -> None:
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"{name}.{ext}", dpi=220)
    plt.close(fig)


def rate(rows, fn):
    k, n = sum(fn(r) for r in rows), len(rows)
    if not n:
        return np.nan, np.nan, np.nan, 0
    lo, hi = proportion_confint(k, n, method="wilson")
    return k / n, lo, hi, n


def eq_play(r) -> bool:
    return r["verdict"] == "AT_EQUILIBRIUM"


def names(r) -> bool:
    return "NAMES_GAME" in code_v1(r)


def complete(block: str) -> list[str]:
    return [m for m in CAPABILITY_ORDER if block_complete(m, block)]


# --- Figure: the design, one question in three wordings ------------------------------------

def design_figure() -> None:
    s = 20260845
    named = GAMES["cournot"].prompt("named", 0, **GAMES["cournot"].sampler(seed=s))
    disg = GAMES["cournot"].prompt("disguised", 0, **GAMES["cournot"].sampler(seed=s))
    ext = GAMES["cournot_extreme"].prompt("disguised", 0, **GAMES["cournot_extreme"].sampler(seed=s))
    p = GAMES["cournot"].sampler(seed=s)
    eq_n = p["equilibrium"]
    eq_x = GAMES["cournot_extreme"].sampler(seed=s)["equilibrium"]
    panels = [("Normal (Stage 2A)", named, BLUE, f"equilibrium: produce {eq_n:.1f}"),
              ("Disguised (Stage 2A)", disg, ORANGE, f"equilibrium: open {eq_n:.1f} (same numbers, no game words)"),
              ("Extreme (Stage 2C)", ext, AQUA, f"equilibrium: x = {eq_x:.2f}, i.e. amount 2x + 4 = {2 * eq_x + 4:.1f}")]
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 3.3))
    for ax, (title, text, color, foot) in zip(axes, panels):
        ax.axis("off")
        ax.add_patch(FancyBboxPatch((0.02, 0.10), 0.96, 0.80, boxstyle="round,pad=0.01,rounding_size=0.03",
                                    transform=ax.transAxes, facecolor="#fcfcfb", edgecolor=GRID, lw=0.8))
        ax.add_patch(FancyBboxPatch((0.02, 0.86), 0.96, 0.04, boxstyle="square,pad=0", transform=ax.transAxes,
                                    facecolor=color, edgecolor="none"))
        ax.text(0.5, 0.95, title, ha="center", va="center", transform=ax.transAxes, fontsize=8.5,
                weight="bold", color=INK)
        wrapped = "\n".join(textwrap.fill(line, 37) for line in text.split("\n"))
        ax.text(0.06, 0.83, wrapped, ha="left", va="top", transform=ax.transAxes, fontsize=5.5,
                family="monospace", color=INK, linespacing=1.25)
        ax.text(0.5, 0.03, textwrap.fill(foot, 34), ha="center", va="center", transform=ax.transAxes,
                fontsize=6.4, color=INK2)
    fig.suptitle("One Cournot question, identical numbers, three wordings; each answer is followed by "
                 "a maths check in the same wording", fontsize=8, color=INK2, y=1.0)
    save(fig, "design")


# --- Figure: Stage 2A, equilibrium play and recognition, normal vs disguised ------------------

def dumbbell(ax, models, rows_by_model, game, fn, ylabel=None):
    xs = np.arange(len(models))
    for i, m in enumerate(models):
        pts = []
        for fr, color, dx in (("named", BLUE, -0.12), ("disguised", ORANGE, 0.12)):
            rs = [r for r in rows_by_model[m] if r["game"] == game and r["framing"] == fr and r["verdict"] in COUNTED]
            v, lo, hi, n = rate(rs, fn)
            if n:
                ax.plot([i + dx] * 2, [lo, hi], color=color, lw=1.6, solid_capstyle="round")
                ax.plot(i + dx, v, "o", ms=5.5, color=color, mec="#fcfcfb", mew=1.4, zorder=3)
            pts.append((i + dx, v))
        ax.plot([pts[0][0], pts[1][0]], [pts[0][1], pts[1][1]], color=INK2, lw=0.7, alpha=0.6, zorder=1)
    ax.set_xticks(xs, [SHORT[m] for m in models])
    ax.set_ylim(-0.03, 1.05)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1], ["0%", "25%", "50%", "75%", "100%"])
    ax.set_title(GAME_NAME[game], fontsize=8.5, color=INK)
    if ylabel:
        ax.set_ylabel(ylabel)


def stage2a_figure() -> list[str]:
    models = complete("2A")
    rows = {m: read(RAW / f"stage2_{m}.csv") for m in models}
    fig, axes = plt.subplots(2, 4, figsize=(7.2, 3.9), sharey=True)
    for j, g in enumerate(GAMES4):
        dumbbell(axes[0, j], models, rows, g, eq_play, "equilibrium play" if j == 0 else None)
        dumbbell(axes[1, j], models, rows, g, names, "names the game" if j == 0 else None)
    h = [plt.Line2D([], [], marker="o", color=c, lw=0, ms=5.5) for c in (BLUE, ORANGE)]
    fig.legend(h, ["normal wording", "disguised wording (same numbers)"], loc="upper center", ncol=2,
               bbox_to_anchor=(0.5, 1.04))
    fig.tight_layout(h_pad=1.2)
    save(fig, "stage2a")
    return models


# --- Figure: the extreme disguise (Stage 2C), paired with Stage 2A ----------------------------

def stage2c_figure() -> list[str]:
    models = [m for m in CAPABILITY_ORDER if block_complete(m, "2A") and block_complete(m, "2C")]
    if not models:
        return []
    fig, axes = plt.subplots(2, 4, figsize=(7.2, 3.9), sharey=True)
    for j, g in enumerate(GAMES4):
        for row, (fn, label) in enumerate(((None, "equilibrium play\n(slip-corrected)"), (names, "names the game"))):
            ax = axes[row, j]
            for i, m in enumerate(models):
                a = [r for r in read(RAW / f"stage2_{m}.csv") if r["game"] == g and r["verdict"] in COUNTED]
                x = [r for r in read(RAW / f"stage2c_{m}.csv") if r["game"] == g + "_extreme" and r["verdict"] in COUNTED]
                series = [("named", [r for r in a if r["framing"] == "named"], BLUE, -0.2),
                          ("disguised", [r for r in a if r["framing"] == "disguised"], ORANGE, 0.0),
                          ("extreme", x, AQUA, 0.2)]
                pts = []
                for _, rs, color, dx in series:
                    f = fn or corrected_eq
                    v, lo, hi, n = rate(rs, f)
                    if n:
                        ax.plot([i + dx] * 2, [lo, hi], color=color, lw=1.6)
                        ax.plot(i + dx, v, "o", ms=5, color=color, mec="#fcfcfb", mew=1.3, zorder=3)
                        pts.append((i + dx, v))
                ax.plot(*zip(*pts), color=INK2, lw=0.7, alpha=0.6, zorder=1)
            ax.set_xticks(range(len(models)), [SHORT[m] for m in models])
            ax.set_ylim(-0.03, 1.05)
            ax.set_yticks([0, 0.5, 1], ["0%", "50%", "100%"])
            if row == 0:
                ax.set_title(GAME_NAME[g], fontsize=8.5)
            if j == 0:
                ax.set_ylabel(label)
    h = [plt.Line2D([], [], marker="o", color=c, lw=0, ms=5) for c in (BLUE, ORANGE, AQUA)]
    fig.legend(h, ["normal (2A)", "disguised (2A)", "extreme (2C)"], loc="upper center", ncol=3,
               bbox_to_anchor=(0.5, 1.04))
    fig.tight_layout(h_pad=1.2)
    save(fig, "stage2c")
    return models


def corrected_eq(r) -> bool:
    """Equilibrium play with the registered fraction-slip correction (pre-registration 3)."""
    p = GAMES[r["game"]].sampler(seed=int(r["seed"]))
    if r["game"].startswith("repeated_pd"):
        return r["verdict"] == "AT_EQUILIBRIUM"
    s = scored(r["observed_action"], r.get("play_reasoning") or "")
    return s is not None and abs(s - float(r["equilibrium"])) <= 0.5


# --- Figure: why the equilibrium was missed (reasoning codes) --------------------------------

MISS_CODES = [("COOPERATION_NORM", "cooperation norm"), ("MISMATCH", "fraction slip"),
              ("COLLUSIVE", "collusive quantity"), ("GROUP_OPTIMUM", "group optimum"),
              ("OTHER", "other / uncoded")]
MISS_COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#c3c2b7"]


def misses_figure() -> None:
    from analysis.reasoning_v2 import main_code
    models = complete("2A")
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.4), sharey=True)
    for ax, fr in zip(axes, ("named", "disguised")):
        labels, stacks = [], []
        for m in models:
            rs = [r for r in read(RAW / f"stage2_{m}.csv") if r["framing"] == fr and r["verdict"] == "STRATEGIC_GAP"]
            c = Counter()
            for r in rs:
                k = main_code(r)
                c[k if k in dict(MISS_CODES) else "OTHER"] += 1
            labels.append(f"{SHORT[m]} (n={len(rs)})")
            stacks.append([c[k] for k, _ in MISS_CODES])
        left = np.zeros(len(models))
        for k, (code_, lab) in enumerate(MISS_CODES):
            vals = np.array([s[k] for s in stacks], dtype=float)
            ax.barh(range(len(models)), vals, left=left, height=0.55, color=MISS_COLORS[k],
                    edgecolor="#fcfcfb", linewidth=1.5, label=lab)
            left += vals
        ax.set_yticks(range(len(models)), labels)
        ax.invert_yaxis()
        ax.set_title(f"{fr} wording: missed answers by reason", fontsize=8.5)
        ax.set_xlabel("missed answers (all four games)")
        ax.grid(axis="y", visible=False)
    axes[0].legend(loc="upper center", bbox_to_anchor=(1.05, 1.32), ncol=5, fontsize=7)
    fig.tight_layout()
    save(fig, "misses")


# --- Figure: Stage 5, cooperation against the subsidy, with both theories' predictions --------

def classical_coop(tau: float) -> float:
    """The stage-game equilibrium cooperation rate: 0 below P - S = 1, the symmetric mixed
    equilibrium p = tau - 1 in between (chicken), 1 above T - R = 2."""
    return float(np.clip(tau - 1.0, 0.0, 1.0))


def stage5_panel(ax, title, data, fit, lam_hat, tau_star):
    from analysis.stage5 import qre_band
    from mechanisms.pd import coop_prob
    grid = np.concatenate([np.linspace(0, 3, 121), np.geomspace(3.01, 60, 160)])
    if fit is not None:
        band = np.array([qre_band(fit, t) for t in grid])
        ax.fill_between(grid, band[:, 1], band[:, 2], color=BLUE, alpha=0.14, lw=0)
    ax.plot(grid, [coop_prob(lam_hat, t) for t in grid], color=BLUE, lw=1.4, label="QRE at fitted $\\hat\\lambda$")
    ax.plot(grid, [classical_coop(t) for t in grid], color=INK2, lw=1.1, ls=(0, (4, 2)), label="classical (stage game)")
    ax.axhline(0.9, color=AQUA, lw=0.8, ls=":", zorder=1)
    if tau_star is not None:
        ax.axvline(tau_star, color=AQUA, lw=0.8, ls=":", zorder=1)
        ax.text(tau_star, 0.03, f" $\\tau^*$={tau_star:g}" + (" (cap)" if tau_star >= 50 else ""), color=AQUA, fontsize=6.5, ha="right" if tau_star >= 50 else "left", va="bottom")
    for tau in sorted(data):
        x = data[tau]
        k, n = int(sum(x)), len(x)
        if not n:
            continue
        lo, hi = proportion_confint(k, n, method="wilson")
        ax.plot([tau, tau], [lo, hi], color=ORANGE, lw=1.6)
        ax.plot(tau, k / n, "o", ms=5.5, color=ORANGE, mec="#fcfcfb", mew=1.4, zorder=4)
    ax.set_xscale("asinh", linear_width=3.0)          # smooth: linear near 0, log beyond
    ax.set_xlim(-0.2, 62)
    ax.set_xticks([0, 1.5, 2.5, 5, 10, 20, 50], ["0", "1.5", "2.5", "5", "10", "20", "50"])
    ax.set_xticks([1, 2, 3, 4, 30, 40], minor=True)
    ax.tick_params(axis="x", labelsize=6.5)
    ax.set_ylim(-0.03, 1.05)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 0.9, 1], ["0%", "25%", "50%", "75%", "90%", "100%"])
    ax.set_title(title, fontsize=8.5)


def stage5_figure(synthetic: bool = False) -> list[str]:
    from analysis.stage5 import load_stage5, stage2a_pd
    from experiments.stage2 import finished
    from experiments.stage5 import LAMBDA_HAT, levels_for, plan
    if synthetic:
        from analysis.stage5 import synthetic as synth
        panels = []
        for m in CAPABILITY_ORDER:
            lam = LAMBDA_HAT[m]
            data, fit, _ = synth(lam, seed=1)
            levels = levels_for(m)
            derived = [t for t in data if t not in (0.0, 1.5, 2.5)]
            for t in derived:                         # the cap, as in experiments/stage5.levels_for
                v = data.pop(t)
                if len(levels) > 3:
                    rng = np.random.default_rng(2)
                    from mechanisms.pd import coop_prob
                    data[levels[3]] = list((rng.random(len(v)) < coop_prob(lam, levels[3])).astype(int))
            panels.append((NAME[m] + " (synthetic)", data, fit, lam, levels[3] if len(levels) > 3 else None))
        models = list(CAPABILITY_ORDER)
    else:
        models = [m for m in CAPABILITY_ORDER if (RAW / f"stage5_{m}.csv").exists()
                  and finished(RAW / f"stage5_{m}.csv") == set(plan(m)) and block_complete(m, "2A")]
        if not models:
            return []
        panels = []
        for m in models:
            fit, _ = stage2a_pd(RAW / f"stage2_{m}.csv")
            levels = levels_for(m)
            panels.append((NAME[m], load_stage5(RAW / f"stage5_{m}.csv"), fit, LAMBDA_HAT[m],
                           levels[3] if len(levels) > 3 else None))
    rows = 1 if len(panels) <= 2 else 2
    cols = math.ceil(len(panels) / rows)
    fig, axes = plt.subplots(rows, cols, figsize=(7.2, 2.35 * rows + 0.5), sharey=True, sharex=True, squeeze=False)
    for ax, args in zip(axes.flat, panels):
        stage5_panel(ax, *args)
    for ax in axes.flat[len(panels):]:
        ax.set_visible(False)
    for ax in axes[:, 0]:
        ax.set_ylabel("cooperation in round 1")
    for ax in axes[-1]:
        ax.set_xlabel("subsidy $\\tau$ per cooperative round (asinh scale)")
    h = [plt.Line2D([], [], color=BLUE, lw=1.4), plt.Line2D([], [], color=INK2, lw=1.1, ls=(0, (4, 2))),
         plt.Line2D([], [], marker="o", color=ORANGE, lw=1.6, ms=5), plt.Line2D([], [], color=AQUA, lw=0.8, ls=":")]
    fig.legend(h, ["QRE at the fitted $\\hat\\lambda$ (band: 95% over $\\lambda$)", "classical stage-game equilibrium",
                   "observed (95% Wilson interval)", "90% target and derived subsidy $\\tau^*$"],
               loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.0 + 0.45 / (2.35 * rows + 0.5)), fontsize=7)
    fig.tight_layout(w_pad=0.6)
    save(fig, "stage5_synthetic" if synthetic else "stage5")
    return models


# --- Figure: Stage 2B endgame, defection by round, normal vs disguised ----------------------

def endgame_figure() -> list[str]:
    from analysis.stage2b import block_rows, defected
    models = [m for m in CAPABILITY_ORDER if block_complete(m, "2B-E")]
    if not models:
        return []
    rows = [r for r in block_rows("E", False) if r["model"] in models and r["kept"]]
    rounds = (5, 9, 10)
    fig, axes = plt.subplots(1, len(models), figsize=(7.2, 2.35), sharey=True, squeeze=False)
    for ax, m in zip(axes[0], models):
        ax.axhline(1.0, color=INK2, lw=0.9, ls=(0, (4, 2)), zorder=1)
        for fr, color, dx in (("named", BLUE, -0.12), ("disguised", ORANGE, 0.12)):
            pts = []
            for k, rd in enumerate(rounds):
                rs = [r for r in rows if r["model"] == m and r["framing"] == fr and r["game"] == f"repeated_pd_round{rd}"]
                v, lo, hi, n = rate(rs, defected)
                if n:
                    ax.plot([k + dx] * 2, [lo, hi], color=color, lw=1.6)
                    ax.plot(k + dx, v, "o", ms=5.5, color=color, mec="#fcfcfb", mew=1.4, zorder=3)
                    pts.append((k + dx, v))
            ax.plot(*zip(*pts), color=color, lw=1.1, alpha=0.75, zorder=2)
        ax.set_xticks(range(3), ["5", "9", "10 (last)"])
        ax.set_xlabel("round of 10")
        ax.set_ylim(-0.03, 1.05)
        ax.set_yticks([0, 0.25, 0.5, 0.75, 1], ["0%", "25%", "50%", "75%", "100%"])
        ax.set_title(NAME[m], fontsize=8.5)
    axes[0][0].set_ylabel("defection")
    h = [plt.Line2D([], [], marker="o", color=c, lw=1.1, ms=5) for c in (BLUE, ORANGE)] + \
        [plt.Line2D([], [], color=INK2, lw=0.9, ls=(0, (4, 2)))]
    fig.legend(h, ["normal wording", "disguised wording", "backward induction (defect always)"],
               loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.08), fontsize=7.5)
    fig.tight_layout(w_pad=0.8)
    save(fig, "endgame")
    return models


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    design_figure()
    print("stage2a models:", stage2a_figure())
    print("stage2c models:", stage2c_figure())
    print("stage5 models:", stage5_figure())
    print("endgame models:", endgame_figure())
    # misses_figure()  -- withheld: relies on KNEW_OVERRODE (hand-check kappa 0.49)
