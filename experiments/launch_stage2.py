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

import os
import subprocess
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

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
X = lambda m: ("stage2c.py", f"--model {m}")          # Stage 2C, extreme disguise
S = lambda m: ("stage5.py", f"--model {m}")           # Stage 5, the PD subsidy (osf pre-reg 4)

# Deviation 11: with a Cerebras key, gpt-oss-120b's Stage 2B blocks run on Cerebras (same open
# weights, 1M free tokens a day); Stage 2A, Stage 2C and Stage 5 stay on Groq, because they are
# compared question by question. Without the key, everything stays on Groq as registered.
CEREBRAS_ENV = "GPTOSS_PROVIDER=cerebras"
# Item 13: two Groq keys (two people's free-tier accounts; Groq Support confirmed this is
# permitted). Everything stays on Groq as registered; each key serves one sequential chain,
# balanced so both finish about together. This takes precedence over the Cerebras route.
GROQ_ENV = "GROQ_KEY_SLOT=2"
# With two or more Groq keys (each a different person's account, as item 13), every remaining
# gpt-oss block is split evenly across all keys (--shard i/k: disjoint slices of the registered
# plan, same order), so the keys finish together. Still Groq for everything, as registered.
GROQ_KEYS = 1 + next(n for n in range(2, 50) if not os.getenv(f"GROQ_API_KEY_{n}")) - 2
if GROQ_KEYS >= 2:
    GPTOSS_CHAINS = [
        [(f"GROQ_KEY_SLOT={i}",)]
        + [(script, f"{args} --shard {i}/{GROQ_KEYS}") for script, args in
           (S("gptoss120b"), B("B", "gptoss120b"), B("C", "gptoss120b"), B("E", "gptoss120b"))]
        for i in range(1, GROQ_KEYS + 1)
    ]
elif os.getenv("GROQ_API_KEY_2"):
    GPTOSS_CHAINS = [
        [A("gptoss120b"), X("gptoss120b"), S("gptoss120b"), B("E", "gptoss120b")],
        [(GROQ_ENV,), B("B", "gptoss120b"), B("C", "gptoss120b")],
    ]
elif os.getenv("CEREBRAS_API_KEY"):
    GPTOSS_CHAINS = [
        [A("gptoss120b")],
        [X("gptoss120b")],
        [(CEREBRAS_ENV,), B("B", "gptoss120b"), B("C", "gptoss120b"), B("E", "gptoss120b")],
    ]
else:
    GPTOSS_CHAINS = [[A("gptoss120b"), B("B", "gptoss120b"), X("gptoss120b"),
                      B("C", "gptoss120b"), B("E", "gptoss120b")]]

# Item 12: two Gemini keys (two people's free-tier accounts; Google Support confirmed this is
# permitted). Each key serves one sequential chain, so each stays inside its own free limits:
# key 1 runs the traps then the sweep; key 2 runs the extreme disguise then the endgame.
GEMINI_ENV = "GEMINI_KEY_SLOT=2"
if os.getenv("GEMINI_API_KEY_2"):
    GEMINI_CHAINS = [[A("gemini_lite")],
                     [B("B", "gemini_lite"), B("C", "gemini_lite"), ("stage5.py", "--model gemini_lite --shard 1/2")],
                     [(GEMINI_ENV,), X("gemini_lite"), B("E", "gemini_lite"), ("stage5.py", "--model gemini_lite --shard 2/2")]]
else:
    GEMINI_CHAINS = [[A("gemini_lite"), B("B", "gemini_lite"), X("gemini_lite"), B("C", "gemini_lite"),
                      B("E", "gemini_lite")]]

CHAINS = [
    # Groq. Free tier: 200,000 tokens a day, ~170 questions. Traps (Block B) first.
    # Block D was dropped before any of its data existed (deviation 7), so every model
    # now answers exactly the same set of questions.
    # Stage 2C (registration 3) right after the traps on the daily-capped providers.
    *GPTOSS_CHAINS,
    # NVIDIA: no daily cap and ~1 request a minute per run, far under the per-minute cap,
    # so every block runs as its own chain, side by side (order is not registered; each
    # block still has exactly one runner, so no question can be asked twice)
    [A("nemotron")],
    [B("B", "nemotron"), B("C", "nemotron"), B("E", "nemotron")],
    [X("nemotron")],
    [A("kimi")],
    [B("B", "kimi")],
    # deviation 16: Kimi's unreadable answers from NVIDIA's degraded days, re-asked four ways at once
    *[[("stage2b.py", f"--block C --model kimi --shard {i}/4"),
       ("stage2b.py", f"--block E --model kimi --shard {i}/4")] for i in range(1, 5)],
    [X("kimi")],
    # Stage 5 (pre-registration 4): one runner per model, on the NVIDIA account alongside 2B
    # NVIDIA has no daily cap and these runs are far under its per-minute limit; the limit is
    # how long each answer takes, so Stage 5 is split across parallel runs on the one key
    *[[("stage5.py", f"--model nemotron --shard {i}/2")] for i in range(1, 3)],
    *[[("stage5.py", f"--model kimi --shard {i}/4")] for i in range(1, 5)],
    # Google
    *GEMINI_CHAINS,
]


def running(step: tuple[str, str]) -> bool:
    script, args = step
    out = subprocess.run(["ps", "-eo", "command"], capture_output=True, text=True).stdout
    return any("python" in line.split(" ", 1)[0].lower()
               and f"{script} {args}" in line
               for line in out.splitlines())


def label(step: tuple[str, str]) -> str:
    script, args = step
    return ({"stage2.py": "2A ", "stage2b.py": "2B ", "stage2c.py": "2C ", "stage5.py": "S5 "}[script]
            + args.replace("--block ", "").replace("--model ", "").replace("--shard ", "#"))


def dashboard_up() -> bool:
    out = subprocess.run(["lsof", "-ti", ":8792"], capture_output=True, text=True).stdout
    return bool(out.strip())


def old_split_gptoss_running() -> bool:
    """True while a gpt-oss run started without --shard is alive. Split runs must not start
    beside one, or the same question could be asked twice."""
    out = subprocess.run(["ps", "-eo", "command="], capture_output=True, text=True).stdout
    return any("gptoss120b" in line and "experiments/stage" in line
               and f"/{GROQ_KEYS} " not in line + " " and "launch_stage2" not in line
               for line in out.splitlines())


def main() -> None:
    (ROOT / "results" / "logs").mkdir(parents=True, exist_ok=True)
    blocked = GROQ_KEYS >= 2 and old_split_gptoss_running()
    if blocked:
        print("gpt-oss: runs split for a different key count still alive -- stop them first; split runs not started")
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
        env = ""
        if len(chain[0]) == 1:                      # a leading (ENV,) marker: per-chain env
            env, chain = chain[0][0] + " ", chain[1:]
        name = " -> ".join(label(step) for step in chain) + (f"  [{env.strip()}]" if env else "")
        if blocked and chain in [c[1:] for c in GPTOSS_CHAINS]:
            continue
        live = [step for step in chain if running(step)]
        if live:
            print(f"{name}\n    already running ({label(live[0])})")
            continue
        script = "; ".join(
            f"{env}{PY} experiments/{s} {a} --wait "
            f">> results/logs/{s.split('.')[0]}_{a.replace('--block ', '').replace('--model ', '').replace('--shard ', '').replace('/', 'of').replace(' ', '_')}.log 2>&1"
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
