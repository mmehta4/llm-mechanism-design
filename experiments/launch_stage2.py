"""Start -- or resume -- every Stage 2 run, detached from any terminal or app.

    python experiments/launch_stage2.py

Also starts the live console (http://localhost:8792) if it is not already up.

Safe to run any time: a run that is already going is left alone, and a finished
model exits immediately. Each run is started in its own session, so closing the
terminal or the app that launched it does not stop it. `caffeinate -i` keeps the Mac
from idle-sleeping while any run is alive (closing the lid still sleeps it).

Every model runs side by side, the two NVIDIA models included: they share an
account, but at ~1 request a minute each they sit far under its per-minute cap.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = "./venv/bin/python"

# Each chain runs its steps in order; chains run side by side. A step is
# (script, args). Finished steps exit at once, so re-launching is always safe.
#
# Stage 2B (pre-registration 2, osf.io/6hz8d) follows Stage 2A on the providers with
# DAILY caps -- Groq and Google -- because running both at once would only split one
# day's allowance between them. The NVIDIA models have no daily cap, so their 2B
# chain runs alongside their 2A run.
A = lambda m: ("stage2.py", f"--model {m}")
B = lambda block, m: ("stage2b.py", f"--block {block} --model {m}")

CHAINS = [
    # Groq. Free tier: 200,000 tokens a day, ~170 questions. The traps (Block B) go
    # first because they carry the study; Block D, the largest, goes last.
    [A("gptoss120b"), B("B", "gptoss120b"), B("C", "gptoss120b"), B("E", "gptoss120b"),
     B("D", "gptoss120b_low"), B("D", "gptoss120b_high")],
    # NVIDIA
    [A("nemotron")],
    [B("B", "nemotron"), B("C", "nemotron"), B("E", "nemotron")],
    [A("kimi")],
    [B("B", "kimi"), B("C", "kimi"), B("E", "kimi")],
    # Google
    [A("gemini_lite"), B("B", "gemini_lite"), B("C", "gemini_lite"), B("E", "gemini_lite")],
]


def running(step: tuple[str, str]) -> bool:
    script, args = step
    out = subprocess.run(["ps", "-eo", "command"], capture_output=True, text=True).stdout
    return any("python" in line.split(" ", 1)[0].lower()
               and f"{script} {args}" in line
               for line in out.splitlines())


def label(step: tuple[str, str]) -> str:
    script, args = step
    return ("2A " if script == "stage2.py" else "2B ") + args.replace("--block ", "").replace("--model ", "")


def dashboard_up() -> bool:
    out = subprocess.run(["lsof", "-ti", ":8792"], capture_output=True, text=True).stdout
    return bool(out.strip())


def main() -> None:
    (ROOT / "results" / "logs").mkdir(parents=True, exist_ok=True)
    # the live console, detached like the runs so it outlives the app that started it
    if dashboard_up():
        print("live console       already running  http://localhost:8792")
    else:
        subprocess.Popen(
            [PY, "dashboard/server.py"], cwd=ROOT, start_new_session=True,
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        print("live console       started          http://localhost:8792")
    # automatic backup to the private GitHub repository, every 3 hours
    subprocess.Popen(["sh", "scripts/backup_loop.sh"], cwd=ROOT, start_new_session=True,
                     stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("backup to GitHub   running every 3 hours (results/logs/backup.log)")
    for chain in CHAINS:
        name = " -> ".join(label(step) for step in chain)
        live = [step for step in chain if running(step)]
        if live:
            print(f"{name}\n    already running ({label(live[0])})")
            continue
        script = "; ".join(
            f"{PY} experiments/{s} {a} --wait "
            f">> results/logs/{s.split('.')[0]}_{a.replace('--block ', '').replace('--model ', '').replace(' ', '_')}.log 2>&1"
            for s, a in chain
        )
        subprocess.Popen(
            ["caffeinate", "-i", "sh", "-c", script],
            cwd=ROOT, start_new_session=True,
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        print(f"{name}\n    started")


if __name__ == "__main__":
    main()
