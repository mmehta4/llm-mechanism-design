"""Append trial rows to CSV.

Every row carries its full prompt and raw response. That makes the files large and
is the correct trade: the transcripts are the audit trail, and in Stage 3.5 they
become the primary material rather than a byproduct.
"""
from __future__ import annotations

import csv
import fcntl
from pathlib import Path

FIELDS = [
    "timestamp", "game", "framing", "model_key", "model_api_id", "seed",
    "paraphrase_idx", "params", "equilibrium", "observed_action", "deviation",
    "verdict", "infra", "probe_answer", "probe_correct_answer", "probe_passed", "probe_malformed",
    "play_parse_ok", "probe_parse_ok", "play_error",
    "play_latency_s", "probe_latency_s", "total_latency_s", "cost_usd", "attempts",
    "play_reasoning", "probe_reasoning", "play_prompt", "probe_prompt", "play_raw",
]


class TrialLog:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._new = not self.path.exists()

    def write(self, rows: list[dict]) -> None:
        # Locked while appending: when one block is split across several API keys
        # (--shard), each shard's process appends to the same file.
        with self.path.open("a", newline="", encoding="utf-8") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
                if f.tell() == 0:
                    writer.writeheader()
                self._new = False
                for row in rows:
                    writer.writerow(row)
                f.flush()
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)
