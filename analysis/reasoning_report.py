"""Per-block reasoning reports, using the LOCKED rules in analysis/reasoning.py unchanged.

    python analysis/reasoning_report.py nemotron

analysis/reasoning.py --model pools a model's Stage 2A and Stage 2B answers by game
family, which mixes ordinary games with traps. This writes one report per block instead.
It only calls the locked functions; it adds no rule of its own.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from analysis.reasoning import load, reasoning_locked, report

if __name__ == "__main__":
    model = sys.argv[1]
    if not reasoning_locked():
        raise SystemExit("STOP: the reasoning codebook is not locked.")
    raw, out = ROOT / "results" / "raw", ROOT / "results" / "analysis"
    files = [("2A", raw / f"stage2_{model}.csv")] + [
        (f"2B-{b}", raw / f"stage2b_{b}_{model}.csv") for b in "BCDE"]
    parts = []
    for block, path in files:
        rows = load([path])
        if rows:
            parts.append(report(rows, f"{model} · Stage {block} · reasoning codes (exploratory)"))
    text = "\n\n---\n\n".join(parts)
    (out / f"reasoning_{model}.md").write_text(text + "\n", encoding="utf-8")
    print(text)
