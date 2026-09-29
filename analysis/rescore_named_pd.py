"""One-off correction: rescore named-PD rows logged before the fix of 2026-09-30.

Those rows compared the model's C/D answer with the disguised X/Y label, so every
one was marked STRATEGIC_GAP. The model's answer, probe answer and all raw text were
recorded correctly; only three DERIVED columns were wrong -- equilibrium, deviation,
verdict. This recomputes exactly those, with the same code live trials now use, and
touches nothing else.

    python analysis/rescore_named_pd.py results/raw/*.csv
"""
from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from experiments.trial import deviation_of, verdict_of


def as_bool(v: str):
    return {"True": True, "False": False}.get(v)


def rescore(path: Path) -> Counter:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields, rows = reader.fieldnames, list(reader)

    changes = Counter()
    for r in rows:
        if r["game"] != "repeated_pd" or r["framing"] != "named" or r["equilibrium"] == "D":
            continue
        before = r["verdict"]
        r["equilibrium"] = "D"
        if as_bool(r["play_parse_ok"]):
            r["deviation"] = deviation_of(r["observed_action"], "D")
        view = {
            "infra": r.get("infra") or None,
            "play_parse_ok": as_bool(r["play_parse_ok"]),
            "probe_malformed": as_bool(r.get("probe_malformed", "")),
            "probe_passed": as_bool(r["probe_passed"]),
            "deviation": r["deviation"] if r["deviation"] != "" else None,
        }
        r["verdict"] = verdict_of(view, "D")
        changes[(before, r["verdict"])] += 1

    if changes:
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
    return changes


if __name__ == "__main__":
    for p in sys.argv[1:]:
        c = rescore(Path(p))
        if c:
            print(f"{Path(p).name}: " + ", ".join(f"{a}->{b} x{n}" for (a, b), n in c.items()))
