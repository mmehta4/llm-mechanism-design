"""Live project console.

Reads the real files on disk every time it is polled -- the running pilot's CSV, the
git log, the test suite, the module tree -- so the page shows actual state rather
than a snapshot. Standard library only, so it needs no install and cannot drift from
the project's own dependencies.
"""
from __future__ import annotations

import csv
import json
import statistics
import subprocess
import sys
from collections import defaultdict
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
PORT = 8792


def sh(*args: str) -> str:
    try:
        return subprocess.run(args, cwd=ROOT, capture_output=True, text=True,
                              timeout=10).stdout.strip()
    except Exception:
        return ""


def running_processes() -> list[dict]:
    """Direct ps, filtered in Python.

    Deliberately NOT `bash -lc "... | grep ..."`: a login shell sources the user's
    full profile, which on a poll every two seconds is both slow and enough to eat
    the timeout budget the git and test calls need.
    """
    out = sh("ps", "-eo", "pid,etime,pcpu,command")
    procs = []
    for line in out.splitlines()[1:]:
        if "experiments/" not in line or "grep" in line:
            continue
        parts = line.split(None, 3)
        if len(parts) == 4:
            procs.append({"pid": parts[0], "elapsed": parts[1],
                          "cpu": parts[2], "cmd": parts[3][-90:]})
    return procs


def read_run(path: Path) -> dict:
    rows = []
    try:
        with path.open(encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception:
        return {"name": path.name, "trials": 0, "cells": [], "error": "unreadable"}

    cells = defaultdict(list)
    for r in rows:
        cells[(r.get("game", "?"), r.get("framing", "?"))].append(r)

    out = []
    for (game, framing), rs in sorted(cells.items()):
        devs = [float(r["deviation"]) for r in rs
                if r.get("deviation") not in ("", "None", None)]
        verdicts = defaultdict(int)
        for r in rs:
            verdicts[r.get("verdict", "?")] += 1
        at_eq = verdicts.get("AT_EQUILIBRIUM", 0)
        out.append({
            "game": game, "framing": framing, "n": len(rs),
            "at_eq": at_eq, "at_eq_pct": round(100 * at_eq / len(rs), 1) if rs else 0,
            "mean": round(statistics.mean(devs), 3) if devs else None,
            "sd": round(statistics.stdev(devs), 3) if len(devs) > 1 else 0.0,
            "verdicts": dict(verdicts),
        })

    lat = [float(r["total_latency_s"]) for r in rows if r.get("total_latency_s")]
    models = sorted({r.get("model_key", "?") for r in rows})
    return {
        "name": path.name,
        "trials": len(rows),
        "models": models,
        "median_latency": round(sorted(lat)[len(lat) // 2], 2) if lat else None,
        "cells": out,
        "recent": [
            {"game": r.get("game"), "framing": r.get("framing"),
             "dev": r.get("deviation"), "verdict": r.get("verdict"),
             "latency": r.get("total_latency_s")}
            for r in rows[-12:][::-1]
        ],
    }


def state() -> dict:
    raw = ROOT / "results" / "raw"
    runs = [read_run(p) for p in sorted(raw.glob("*.csv"), key=lambda p: -p.stat().st_mtime)]

    modules = []
    for d in ["theory", "games", "agents", "experiments", "tests"]:
        files = sorted((ROOT / d).glob("*.py"))
        for f in files:
            if f.name == "__init__.py":
                continue
            modules.append({"path": f"{d}/{f.name}",
                            "lines": sum(1 for _ in f.open(encoding="utf-8", errors="replace"))})

    commits = []
    for line in sh("git", "log", "--pretty=%h|%ar|%s", "-12").splitlines():
        parts = line.split("|", 2)
        if len(parts) == 3:
            commits.append({"hash": parts[0], "when": parts[1], "subject": parts[2]})

    return {
        "processes": running_processes(),
        "runs": runs,
        "modules": modules,
        "module_lines": sum(m["lines"] for m in modules),
        "commits": commits,
    }


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
