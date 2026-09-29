"""Live project console.

Reads the real files on disk every time it is polled -- each model's Stage 2 CSV,
its log, the process table, the git log -- so the page shows actual state rather
than a snapshot. Standard library only, so it needs no install and cannot drift from
the project's own dependencies.
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import statistics
import subprocess
import sys
from collections import defaultdict
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
PORT = 8792


def sh(*args: str) -> str:
    try:
        return subprocess.run(args, cwd=ROOT, capture_output=True, text=True,
                              timeout=10).stdout.strip()
    except Exception:
        return ""


# --- Stage 2 --------------------------------------------------------------------

GAMES = ["vickrey", "cournot", "repeated_pd", "public_goods"]


def model_process(model: str) -> bool:
    """Is a Python process running Stage 2 for this model?

    Only the interpreter itself counts. The caffeinate and `sh -c` wrappers carry
    the same arguments -- the Nemotron wrapper even names Kimi, which is queued
    behind it -- and must not make a waiting model look live.
    """
    for line in sh("ps", "-eo", "command").splitlines():
        exe = line.split(" ", 1)[0].lower()
        if "python" in exe and f"stage2.py --model {model}" in line:
            return True
    return False


def log_tail(model: str, n: int = 6) -> list[str]:
    path = ROOT / "results" / "logs" / f"stage2_{model}.log"
    try:
        with path.open("rb") as f:
            f.seek(0, 2)
            f.seek(max(0, f.tell() - 4000))
            lines = f.read().decode("utf-8", "replace").splitlines()
        return [l for l in lines if l.strip()][-n:]
    except OSError:
        return []


def age_s(ts: str) -> float | None:
    try:
        return (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(ts)).total_seconds()
    except (TypeError, ValueError):
        return None


def stage2_model(model: str, spec, total: int) -> dict:
    path = ROOT / "results" / "raw" / f"stage2_{model}.csv"
    rows = []
    if path.exists():
        with path.open(encoding="utf-8") as f:
            rows = list(csv.DictReader(f))

    answered = [r for r in rows if r.get("verdict") != "INFRA_FAIL"]
    keys = {(r["game"], r["framing"], r["seed"], r["paraphrase_idx"]) for r in answered}
    verdicts = defaultdict(int)
    for r in answered:
        verdicts[r["verdict"]] += 1

    cells = {}
    for g in GAMES:
        for fr in ("named", "disguised"):
            rs = [r for r in answered if r["game"] == g and r["framing"] == fr]
            at = sum(r["verdict"] == "AT_EQUILIBRIUM" for r in rs)
            cells[f"{g}|{fr}"] = {"n": len(rs), "at_eq": at}

    recent_hour = [r for r in answered if (age_s(r["timestamp"]) or 1e9) < 3600]
    lat = [float(r["total_latency_s"]) for r in answered[-40:] if r.get("total_latency_s")]

    # real pace = time between consecutive finished questions, which includes pacer
    # waits that latency alone misses; gaps over 15 min are pauses or restarts
    stamps = [dt.datetime.fromisoformat(r["timestamp"]) for r in answered[-31:]]
    gaps = [(b - a).total_seconds() for a, b in zip(stamps, stamps[1:])]
    gaps = [g for g in gaps if 0 <= g < 900]
    if model_process(model) and rows:
        since = age_s(rows[-1]["timestamp"]) or 0
        if since < 900:
            gaps.append(since)        # the question in flight counts too

    tail = log_tail(model)
    last = tail[-1] if tail else ""
    running = model_process(model)
    if len(keys) >= total:
        status = "complete"
    elif running and last.startswith("waiting until"):
        status = "paused"
    elif running:
        status = "running"
    elif model == "kimi" and model_process("nemotron"):
        status = "queued"
    else:
        status = "stopped"

    pause_reason = ""
    if status == "paused":
        prev = " ".join(tail[-3:-1]).lower()
        pause_reason = "daily" if "daily quota" in prev else "outage"

    return {
        "key": model,
        "api_id": spec.api_id,
        "provider": spec.provider,
        "done": len(keys),
        "total": total,
        "infra_fails": len(rows) - len(answered),
        "status": status,
        "pause_reason": pause_reason,
        "resume_at": last.replace("waiting until ~", "").split(",")[0] if status == "paused" else "",
        "since_last_s": age_s(rows[-1]["timestamp"]) if rows else None,
        "last_hour": len(recent_hour),
        "median_latency": round(statistics.median(lat), 1) if lat else None,
        "sec_per_q": round(statistics.mean(gaps), 1) if len(gaps) >= 2 else None,
        "verdicts": dict(verdicts),
        "cells": cells,
        "recent": [
            {"game": r["game"], "framing": r["framing"], "verdict": r["verdict"],
             "latency": r.get("total_latency_s"), "age": age_s(r["timestamp"]),
             "infra": r.get("infra")}
            for r in rows[-8:][::-1]
        ],
    }


def state() -> dict:
    from config import CAPABILITY_ORDER, MODELS
    from experiments.stage2 import plan
    total = len(plan()) // 1          # trials per model
    models = [stage2_model(m, MODELS[m], total) for m in CAPABILITY_ORDER]

    commits = []
    for line in sh("git", "log", "--pretty=%h|%ar|%s", "-8").splitlines():
        parts = line.split("|", 2)
        if len(parts) == 3:
            commits.append({"hash": parts[0], "when": parts[1], "subject": parts[2]})

    return {"models": models, "commits": commits,
            "now": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(HERE), **kw)

    def do_GET(self):
        if self.path.startswith("/api/state"):
            body = json.dumps(state()).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def log_message(self, *a):
        pass          # polling every 2s would otherwise flood the terminal


if __name__ == "__main__":
    print(f"live console on http://localhost:{PORT}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
