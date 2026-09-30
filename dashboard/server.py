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


def python_commands() -> list[str]:
    """Command lines of running Python processes -- only the interpreter counts, not
    the caffeinate / sh wrappers that carry the same arguments."""
    return [line for line in sh("ps", "-eo", "command").splitlines()
            if "python" in line.split(" ", 1)[0].lower()]


def log_tail(name: str, n: int = 6) -> list[str]:
    path = ROOT / "results" / "logs" / f"{name}.log"
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


BLOCK_NAMES = {"A": "Stage 2A · confirmatory", "B": "Traps", "C": "Number sweep",
               "E": "PD endgame", "D": "Think harder"}


def read_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def sources(model: str) -> list[dict]:
    """Every run that belongs to one model: its Stage 2A run and each Stage 2B block."""
    from experiments.stage2 import plan as plan_a
    from experiments.stage2b import BLOCK_MODELS, PLANS
    out = [{"block": "A", "label": BLOCK_NAMES["A"], "runner": model, "total": len(plan_a()),
            "csv": f"stage2_{model}", "cmd": f"stage2.py --model {model}"}]
    for block in "BCED":
        for runner in BLOCK_MODELS[block]:
            if runner != model and not (block == "D" and runner.startswith(model + "_")):
                continue
            label = BLOCK_NAMES[block]
            if block == "D":
                label += f" ({runner.rsplit('_', 1)[-1]} effort)"
            out.append({"block": block, "label": label, "runner": runner,
                        "total": len(PLANS[block]()), "csv": f"stage2b_{block}_{runner}",
                        "cmd": f"stage2b.py --block {block} --model {runner}"})
    return out


def model_state(model: str, spec, procs: list[str]) -> dict:
    """One model across ALL its questions: Stage 2A plus every Stage 2B block."""
    raw = ROOT / "results" / "raw"
    blocks, answered_all, rows_all = [], [], []
    for src in sources(model):
        rows = read_rows(raw / f"{src['csv']}.csv")
        answered = [r for r in rows if r.get("verdict") != "INFRA_FAIL"]
        keys = {(r["game"], r["framing"], r["seed"], r["paraphrase_idx"]) for r in answered}
        live = any(src["cmd"] in c for c in procs)
        tail = log_tail(src["csv"]) if live else []
        waiting = bool(tail) and tail[-1].startswith("waiting until")
        blocks.append({
            "block": src["block"], "label": src["label"], "done": len(keys),
            "total": src["total"], "running": live and not waiting, "waiting": live and waiting,
            "resume_at": tail[-1].replace("waiting until ~", "").split(",")[0] if waiting else "",
            "pause_reason": ("daily" if "daily quota" in " ".join(tail[-3:-1]).lower()
                             else "outage") if waiting else "",
        })
        for r in rows:
            r["_block"] = src["block"]
        rows_all += rows
        answered_all += answered

    rows_all.sort(key=lambda r: r["timestamp"])
    answered_all.sort(key=lambda r: r["timestamp"])
    done = sum(b["done"] for b in blocks)
    total = sum(b["total"] for b in blocks)

    verdicts = defaultdict(int)
    for r in answered_all:
        verdicts[r["verdict"]] += 1

    a_rows = [r for r in answered_all if r["_block"] == "A"]
    cells = {}
    for g in GAMES:
        for fr in ("named", "disguised"):
            rs = [r for r in a_rows if r["game"] == g and r["framing"] == fr]
            cells[f"{g}|{fr}"] = {"n": len(rs),
                                  "at_eq": sum(r["verdict"] == "AT_EQUILIBRIUM" for r in rs)}

    # real pace across everything this model is doing, parallel runs included: time
    # between consecutive finished questions; gaps over 15 min are pauses or restarts
    stamps = [dt.datetime.fromisoformat(r["timestamp"]) for r in answered_all[-31:]]
    gaps = [(y - x).total_seconds() for x, y in zip(stamps, stamps[1:])]
    gaps = [g for g in gaps if 0 <= g < 900]
    running = [b for b in blocks if b["running"]]
    if running and rows_all:
        since = age_s(rows_all[-1]["timestamp"]) or 0
        if since < 900:
            gaps.append(since)

    waiting = [b for b in blocks if b["waiting"]]
    if done >= total:
        status = "complete"
    elif running:
        status = "running"
    elif waiting:
        status = "paused"
    else:
        status = "stopped"

    lat = [float(r["total_latency_s"]) for r in answered_all[-40:] if r.get("total_latency_s")]
    return {
        "key": model,
        "api_id": spec.api_id,
        "provider": spec.provider,
        "done": done,
        "total": total,
        "blocks": blocks,
        "infra_fails": len(rows_all) - len(answered_all),
        "status": status,
        "pause_reason": waiting[0]["pause_reason"] if status == "paused" else "",
        "resume_at": waiting[0]["resume_at"] if status == "paused" else "",
        "since_last_s": age_s(rows_all[-1]["timestamp"]) if rows_all else None,
        "last_hour": sum(1 for r in answered_all if (age_s(r["timestamp"]) or 1e9) < 3600),
        "median_latency": round(statistics.median(lat), 1) if lat else None,
        "sec_per_q": round(statistics.mean(gaps), 1) if len(gaps) >= 2 else None,
        "verdicts": dict(verdicts),
        "cells": cells,
        "recent": [
            {"block": r["_block"], "game": r["game"], "framing": r["framing"],
             "verdict": r["verdict"], "age": age_s(r["timestamp"]), "infra": r.get("infra")}
            for r in rows_all[-8:][::-1]
        ],
    }


def state() -> dict:
    from config import CAPABILITY_ORDER, MODELS
    procs = python_commands()
    models = [model_state(m, MODELS[m], procs) for m in CAPABILITY_ORDER]

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
