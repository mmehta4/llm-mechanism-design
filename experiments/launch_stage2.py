"""Start -- or resume -- every Stage 2 run, detached from any terminal or app.

    python experiments/launch_stage2.py

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

# one chain per provider: models in a chain run in order, chains run side by side
CHAINS = [
    ["gptoss120b"],             # Groq
    # NVIDIA: side by side. Both are slow thinkers, ~1 request a minute each, far
    # under the free tier's per-minute cap, so queueing them only cost days.
    ["nemotron"],
    ["kimi"],
    ["gemini_lite"],            # Google
]


def running(model: str) -> bool:
    out = subprocess.run(["ps", "-eo", "command"], capture_output=True, text=True).stdout
    return any("python" in line.split(" ", 1)[0].lower()
               and f"stage2.py --model {model}" in line
               for line in out.splitlines())


def main() -> None:
    (ROOT / "results" / "logs").mkdir(parents=True, exist_ok=True)
    for chain in CHAINS:
        live = [m for m in chain if running(m)]
        if live:
            print(f"{' -> '.join(chain):18s} already running ({live[0]})")
            continue
        script = "; ".join(
            f"{PY} experiments/stage2.py --model {m} --wait "
            f">> results/logs/stage2_{m}.log 2>&1"
            for m in chain
        )
        subprocess.Popen(
            ["caffeinate", "-i", "sh", "-c", script],
            cwd=ROOT, start_new_session=True,
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        print(f"{' -> '.join(chain):18s} started")


if __name__ == "__main__":
    main()
