"""One-off correction: NVIDIA's 403 outage of 2026-09-30 19:22-19:32 UTC.

For about ten minutes NVIDIA refused every request with 403 "Authorization failed".
agents/llm.py did not yet classify 403, so each refusal was scored PARSE_FAIL
("unreadable answer") in a fraction of a second -- about 4,450 trials across Kimi and
Nemotron, which made several blocks look complete.

The model never saw these questions. This relabels them INFRA_FAIL (infra "auth") so
they are re-asked; the rows stay in the files as the audit trail. Two patterns:

  * the play call refused: PARSE_FAIL whose error is a PermissionDeniedError;
  * the maths-check call refused: probe not parsed, and returned in under a second
    during the outage. Real replies take seconds; the handful of genuine maths-check
    format failures (5-25 s, before the outage) are left exactly as they are.

    python analysis/relabel_outage_403.py results/raw/stage2*.csv
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

OUTAGE_FROM = "2026-09-30T19:2"


def refused(r: dict) -> bool:
    if r["verdict"] == "INFRA_FAIL":
        return False
    if (r["play_error"] or "").startswith("PermissionDeniedError"):
        return True
    return (r["probe_parse_ok"] == "False" and r["timestamp"] >= OUTAGE_FROM
            and float(r["probe_latency_s"] or 99) < 1.0)


def relabel(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields, rows = reader.fieldnames, list(reader)
    n = 0
    for r in rows:
        if refused(r):
            r["verdict"], r["infra"] = "INFRA_FAIL", "auth"
            n += 1
    if n:
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
    return n


if __name__ == "__main__":
    for p in sys.argv[1:]:
        if n := relabel(Path(p)):
            print(f"{Path(p).name}: {n} refused requests relabelled INFRA_FAIL")
