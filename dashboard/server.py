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
import urllib.parse
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
    from experiments.stage2b import BLOCK_MODELS, DROPPED_BLOCKS, PLANS
    out = [{"block": "A", "label": BLOCK_NAMES["A"], "runner": model, "total": len(plan_a()),
            "csv": f"stage2_{model}", "cmd": f"stage2.py --model {model}"}]
    for block in "BCED":
        if block in DROPPED_BLOCKS:
            continue
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

    # health alarms -- the 403 outage went unnoticed because 4,450 refusals looked
    # like fast, unreadable answers. Either symptom now raises a visible warning.
    hour = [r for r in answered_all if (age_s(r["timestamp"]) or 1e9) < 3600]
    unreadable = sum(r["verdict"] in ("PARSE_FAIL", "PROBE_FORMAT_FAIL") for r in hour)
    too_fast = sum(float(r.get("total_latency_s") or 99) < 0.5 for r in hour)
    alarms = []
    if len(hour) >= 10 and unreadable / len(hour) > 0.2:
        alarms.append(f"{unreadable} of its last {len(hour)} answers in the past hour are "
                      f"unreadable -- possibly the provider failing, not the model.")
    if too_fast >= 5:
        alarms.append(f"{too_fast} answers in the past hour came back in under half a "
                      f"second, which a real reply cannot do.")

    return {
        "alarms": alarms,
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


def pilot_deep() -> list[dict]:
    """Stage 2C pilot (practice questions only): per model, per game, per wording."""
    from analysis.reasoning import code
    from experiments.pilot_deep import FAMILIES, LEVELS
    out = []
    for path in sorted((ROOT / "results" / "raw").glob("practice2c_*.csv")):
        model = path.stem.replace("practice2c_", "")
        rows = [r for r in read_rows(path) if r.get("verdict") != "INFRA_FAIL"]
        cells = []
        for fam in FAMILIES:
            for label, suffix in LEVELS.items():
                rs = [r for r in rows if r["game"] == fam + suffix]
                counted = [r for r in rs if r["verdict"] in ("AT_EQUILIBRIUM", "STRATEGIC_GAP")]
                cells.append({
                    "game": fam, "wording": label, "n": len(rs),
                    "names": sum("NAMES_GAME" in code(r) for r in counted), "counted": len(counted),
                    "eq": sum(r["verdict"] == "AT_EQUILIBRIUM" for r in rs),
                    "probe": sum(r["probe_passed"] == "True" for r in rs),
                })
        out.append({"model": model, "done": len(rows), "planned": 8 * len(FAMILIES) * len(LEVELS),
                    "cells": cells})
    return out


def state() -> dict:
    from config import CAPABILITY_ORDER, MODELS
    procs = python_commands()
    models = [model_state(m, MODELS[m], procs) for m in CAPABILITY_ORDER]

    commits = []
    for line in sh("git", "log", "--pretty=%h|%ar|%s", "-8").splitlines():
        parts = line.split("|", 2)
        if len(parts) == 3:
            commits.append({"hash": parts[0], "when": parts[1], "subject": parts[2]})

    return {"models": models, "commits": commits, "pilot_deep": pilot_deep(),
            "now": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}


# --- Question browser -----------------------------------------------------------

GAME_NAMES = {"vickrey": "Vickrey auction", "cournot": "Cournot",
              "repeated_pd": "Repeated PD", "public_goods": "Public goods"}
TRAP_NAMES = {"vickrey_trap": "Vickrey · trap: winner pays double",
              "cournot_trap": "Cournot · trap: three firms",
              "repeated_pd_trap": "Repeated PD · trap: cooperating pays more",
              "public_goods_trap": "Public goods · trap: multiplier 5"}


def game_label(key: str) -> str:
    """Readable name for any Stage 2 game key, including the Stage 2B variants."""
    if key in GAME_NAMES:
        return GAME_NAMES[key]
    if key in TRAP_NAMES:
        return TRAP_NAMES[key]
    if key.startswith("repeated_pd_round"):
        return f"Repeated PD · round {key.rsplit('round', 1)[1]} of 10"
    sizes = {"vickrey_n_others": lambda v: f"{int(v) + 1} bidders",
             "cournot_a": lambda v: f"market size ~{int(v)}",
             "public_goods_n_others": lambda v: f"{int(v) + 1} players",
             "repeated_pd_n_rounds": lambda v: f"{int(v)} rounds"}
    for prefix, fmt in sizes.items():
        if key.startswith(prefix):
            base = GAME_NAMES[prefix.split("_n_")[0].split("_a")[0]]
            return f"{base} · {fmt(float(key[len(prefix):]))}"
    return key


def questions(query: dict) -> dict:
    """Every question one model was asked, newest first, filtered and paged."""
    from config import CAPABILITY_ORDER
    model = query.get("model", "")
    if model not in CAPABILITY_ORDER:
        return {"error": f"unknown model {model!r}"}
    raw = ROOT / "results" / "raw"
    rows = []
    for src in sources(model):
        for r in read_rows(raw / f"{src['csv']}.csv"):
            r["_block"], r["_block_label"] = src["block"], src["label"]
            rows.append(r)
    rows.sort(key=lambda r: r["timestamp"], reverse=True)

    games = sorted({r["game"] for r in rows}, key=game_label)
    want = {k: query.get(k, "") for k in ("block", "game", "framing", "verdict")}
    if query.get("refusals") != "1":
        rows = [r for r in rows if r["verdict"] != "INFRA_FAIL"]
    if want["block"]:
        rows = [r for r in rows if r["_block"] == want["block"]]
    if want["game"]:
        rows = [r for r in rows if r["game"] == want["game"]]
    if want["framing"]:
        rows = [r for r in rows if r["framing"] == want["framing"]]
    if want["verdict"]:
        rows = [r for r in rows if r["verdict"] == want["verdict"]]

    offset = max(0, int(query.get("offset", 0) or 0))
    limit = min(100, max(1, int(query.get("limit", 25) or 25)))
    page = rows[offset:offset + limit]
    return {
        "model": model,
        "total": len(rows),
        "offset": offset,
        "blocks": [{"block": s["block"], "label": s["label"]} for s in sources(model)],
        "games": [{"key": g, "label": game_label(g)} for g in games],
        "rows": [{
            "time": r["timestamp"], "age": age_s(r["timestamp"]),
            "block": r["_block"], "block_label": r["_block_label"],
            "game": r["game"], "game_label": game_label(r["game"]),
            "framing": r["framing"], "wording": int(r["paraphrase_idx"]) + 1,
            "seed": r["seed"], "verdict": r["verdict"], "infra": r.get("infra") or "",
            "correct": r["equilibrium"], "played": r["observed_action"],
            "prompt": r["play_prompt"], "reasoning": r["play_reasoning"],
            "raw": r["play_raw"], "error": r["play_error"],
            "probe_prompt": r["probe_prompt"], "probe_answer": r["probe_answer"],
            "probe_correct": r["probe_correct_answer"], "probe_reasoning": r["probe_reasoning"],
            "latency": r["total_latency_s"],
        } for r in page],
    }


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(HERE), **kw)

    def do_GET(self):
        if self.path.startswith("/api/state") or self.path.startswith("/api/questions"):
            if self.path.startswith("/api/state"):
                data = state()
            else:
                q = urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query)
                data = questions({k: v[0] for k, v in q.items()})
            body = json.dumps(data).encode()
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
