"""One-off correction: relabel empty replies logged before 2026-09-30 as infrastructure.

Before agents/llm.py learned to recognise them, a reply with no text at all was
scored PARSE_FAIL ("the model answered in an unreadable form"). Nothing was
answered, so it is an INFRA_FAIL: the trial is re-asked on the next pass and the
original row stays in the file as the audit trail. Rows with any reply text are
untouched.

    python analysis/relabel_empty_replies.py results/raw/stage2*.csv
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path


def relabel(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields, rows = reader.fieldnames, list(reader)
    n = 0
    for r in rows:
        if (r["verdict"] == "PARSE_FAIL" and not (r["play_raw"] or "").strip()
                and r["play_error"] == "structured output returned no parsed object"):
            r["verdict"], r["infra"] = "INFRA_FAIL", "empty_response"
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
            print(f"{Path(p).name}: {n} empty repl{'y' if n == 1 else 'ies'} relabelled INFRA_FAIL")
