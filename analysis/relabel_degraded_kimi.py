"""One-off (deviation 16): re-ask Kimi's unreadable Stage 2B answers from NVIDIA's degraded days.

On 2026-10-07..09 NVIDIA served Kimi K3 in a degraded state (deviation 15): 219 of Kimi's 236
unreadable Stage 2B answers fall in those three days (16% of that window's answers, against 3%
elsewhere). At the author's decision, those unreadable answers -- and nothing else -- are re-asked.

Each affected row stays in the file as the audit trail, relabelled INFRA_FAIL with
infra = "degraded_server:<original verdict>", so the runner re-asks exactly those questions and
the registered scoring can still be reproduced (the paper reports both).

    python analysis/relabel_degraded_kimi.py
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DAYS = ("2026-10-07", "2026-10-08", "2026-10-09")
UNREADABLE = {"PARSE_FAIL", "PROBE_FORMAT_FAIL"}


def relabel(path: Path) -> int:
    csv.field_size_limit(sys.maxsize)
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields, rows = reader.fieldnames, list(reader)
    n = 0
    for r in rows:
        if r["verdict"] in UNREADABLE and r["timestamp"][:10] in DAYS:
            r["infra"] = f"degraded_server:{r['verdict']}"
            r["verdict"] = "INFRA_FAIL"
            n += 1
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    return n


if __name__ == "__main__":
    for block in "CE":
        p = ROOT / "results" / "raw" / f"stage2b_{block}_kimi.csv"
        print(f"{p.name}: {relabel(p)} unreadable answers from {DAYS[0]}..{DAYS[-1]} set to be re-asked")
