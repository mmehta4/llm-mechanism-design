"""Stage 3.5: code each answer's reasoning with the fixed rules of docs/reasoning-codebook.md.

    python analysis/reasoning.py --practice            # practice runs only
    python analysis/reasoning.py --model nemotron       # real data: needs the lock
    python analysis/reasoning.py --hand-sample          # print 60 answers to code by hand
    python analysis/reasoning.py --agreement FILE       # κ between hand and automatic codes

Every rule is a plain text or number check, so the same answer always gets the same
codes. Exploratory: no pre-registered predictions are tested here.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from games import GAMES

# --- the lock: this file and the codebook, fingerprinted before real data is coded
REASONING_SHA256 = "ba3b36e7a129ffff6fa7877cff06bfcbe8f90eb0643013076c867889dc66304f"
CODEBOOK = ROOT / "docs" / "reasoning-codebook.md"


def _fingerprint() -> str:
    text = Path(__file__).read_text(encoding="utf-8")
    body = "\n".join(l for l in text.splitlines() if not l.startswith("REASONING_SHA256 ="))
    return hashlib.sha256(body.encode() + b"\0" + CODEBOOK.read_bytes()).hexdigest()


def reasoning_locked() -> bool:
    return REASONING_SHA256 is not None and _fingerprint() == REASONING_SHA256


# --- the rules (docs/reasoning-codebook.md) -----------------------------------------

GAME_NAMES = {
    "cournot": [r"cournot", r"duopol", r"oligopol", r"triopol"],
    "vickrey": [r"vickrey", r"second[\s\-‑]?price", r"auction"],
    "repeated_pd": [r"prisoner", r"dilemma"],
    "public_goods": [r"public[\s\-‑]?goods?", r"free[\s\-‑]?rid", r"commons"],
}
CONCEPT = r"nash|equilibri|dominant strateg|best[\s\-‑]?response"
DOMINANCE = r"dominan|dominat|regardless of (what|whether|how)|whatever the other|no matter what"
BEST_RESPONSE = r"best[\s\-‑]?response|reaction function|derivative|first[\s\-‑]?order|maximi[sz]\w* with respect"
BACKWARD = r"backward[\s\-‑]?induction|last round|final round|unravel"
COOP_NORM = r"trust|mutual|reciproc|signal|establish|cooperat|goodwill|relationship"
GROUP = r"everyone|all (the )?(players|operators|participants)|collective|group|total payoff|social|together"

NUMBER = re.compile(r"(?<![\w.])-?\d+(?:\.\d+)?")


def family(game: str) -> str:
    for fam in GAME_NAMES:
        if game.startswith(fam):
            return fam
    raise KeyError(game)


def _has(pattern: str, text: str) -> bool:
    return re.search(pattern, text, re.IGNORECASE) is not None


def _num(x) -> float | None:
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def code(row: dict) -> set[str]:
    """All codebook codes for one answer row (from a Stage 2 results file)."""
    game, fam = row["game"], family(row["game"])
    text = row.get("play_reasoning") or ""
    prompt = row.get("play_prompt") or ""
    p = GAMES[game].sampler(seed=int(row["seed"]))
    codes: set[str] = set()

    # recognition: a name for the game that the question itself does not use
    if any(_has(n, text) and not _has(n, prompt) for n in GAME_NAMES[fam]):
        codes.add("NAMES_GAME")
    if _has(CONCEPT, text):
        codes.add("NAMES_CONCEPT")

    # method
    if _has(DOMINANCE, text):
        codes.add("DOMINANCE")
    if _has(BEST_RESPONSE, text):
        codes.add("BEST_RESPONSE")
    if _has(BACKWARD, text):
        codes.add("BACKWARD_INDUCTION")

    if row["verdict"] != "STRATEGIC_GAP":
        return codes

    # error codes
    ans, eq = _num(row["observed_action"]), _num(row["equilibrium"])
    err: set[str] = set()
    if fam == "cournot" and ans is not None:
        n = p.get("n_firms", 2)
        if abs(ans - (p["a"] - p["c"]) / (2 * n * p["b"])) <= 0.5:
            err.add("COLLUSIVE")
        if game == "cournot_trap" and abs(ans - (p["a"] - p["c"]) / (3 * p["b"])) <= 0.5:
            err.add("DUOPOLY_FORMULA")
    if game == "vickrey_trap" and ans is not None and abs(ans - p["value"]) <= 0.5:
        err.add("TRUTHFUL_DEFAULT")
    if fam == "repeated_pd":
        coop = "C" if row["framing"] == "named" else p["coop"]
        if str(row["observed_action"]).strip().upper() == coop.upper() and _has(COOP_NORM, text):
            err.add("COOPERATION_NORM")
    if fam == "public_goods" and ans is not None and eq is not None and ans > eq + 0.5 and _has(GROUP, text):
        err.add("GROUP_OPTIMUM")
    # Only in Cournot is the equilibrium a number the model must derive; in Vickrey
    # and public goods it is a number given in the question, so mentioning it proves
    # nothing (practice data: three false alarms of exactly that kind).
    if fam == "cournot" and ans is not None and eq is not None and abs(ans - eq) > 0.5:
        nums = [float(x) for x in NUMBER.findall(text)]
        if nums and abs(nums[-1] - eq) <= 0.5:
            err.add("MISMATCH")              # concluded at the equilibrium, wrote another number
        elif any(abs(x - eq) <= 0.5 for x in nums):
            err.add("KNEW_AND_DEVIATED")     # derived it, then chose something else on purpose
    codes |= err or {"UNCODED"}
    return codes


# --- reporting -----------------------------------------------------------------------

ERROR_CODES = ["COLLUSIVE", "DUOPOLY_FORMULA", "TRUTHFUL_DEFAULT", "COOPERATION_NORM",
               "GROUP_OPTIMUM", "MISMATCH", "KNEW_AND_DEVIATED", "UNCODED"]


def load(paths: list[Path]) -> list[dict]:
    rows = []
    for path in paths:
        if not path.exists():
            continue
        with path.open(encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r["verdict"] in ("AT_EQUILIBRIUM", "STRATEGIC_GAP"):
                    r["codes"] = code(r)
                    rows.append(r)
    return rows


def report(rows: list[dict], title: str) -> str:
    out = [f"# {title}", "", "## Did the model name the game? (`NAMES_GAME`)", "",
           "| Game | Normal | Disguised |", "|---|---:|---:|"]
    by = defaultdict(list)
    for r in rows:
        by[(family(r["game"]), r["framing"])].append(r)
    share = lambda rs, c: f"{sum(c in r['codes'] for r in rs) / len(rs):.0%} ({sum(c in r['codes'] for r in rs)}/{len(rs)})" if rs else "–"
    for fam in GAME_NAMES:
        out.append(f"| {fam} | {share(by[(fam, 'named')], 'NAMES_GAME')} | {share(by[(fam, 'disguised')], 'NAMES_GAME')} |")
    out += ["", "## Why the equilibrium was missed (STRATEGIC_GAP answers)", "",
            "| Game | Wording | Gaps | " + " | ".join(ERROR_CODES) + " |",
            "|---|---|---:|" + "---:|" * len(ERROR_CODES)]
    for (fam, fr), rs in sorted(by.items()):
        gaps = [r for r in rs if r["verdict"] == "STRATEGIC_GAP"]
        if not gaps:
            continue
        cells = [str(sum(c in r["codes"] for r in gaps)) for c in ERROR_CODES]
        out.append(f"| {fam} | {fr} | {len(gaps)} | " + " | ".join(cells) + " |")
    out += ["", "## How the model reasoned (all counted answers)", "",
            "| Game | Wording | Names a concept | Dominance | Best response | Backward induction |",
            "|---|---|---:|---:|---:|---:|"]
    for (fam, fr), rs in sorted(by.items()):
        out.append(f"| {fam} | {fr} | " + " | ".join(share(rs, c) for c in
                   ["NAMES_CONCEPT", "DOMINANCE", "BEST_RESPONSE", "BACKWARD_INDUCTION"]) + " |")
    return "\n".join(out)


# --- hand check ----------------------------------------------------------------------

HAND_SEED = 20261002


def hand_sample(rows_by_model: dict[str, list[dict]], k: int = 15) -> list[dict]:
    """15 per model: half normal, half disguised, gaps over-sampled (codebook §4)."""
    rng = random.Random(HAND_SEED)
    picked = []
    for model, rows in sorted(rows_by_model.items()):
        for fr, n in (("named", k // 2), ("disguised", k - k // 2)):
            pool = [r for r in rows if r["framing"] == fr]
            gaps = [r for r in pool if r["verdict"] == "STRATEGIC_GAP"]
            rest = [r for r in pool if r["verdict"] != "STRATEGIC_GAP"]
            take = rng.sample(gaps, min(len(gaps), (n + 1) // 2))
            take += rng.sample(rest, min(len(rest), n - len(take)))
            picked += [dict(r, model=model) for r in take]
    rng.shuffle(picked)
    return picked


def cohen_kappa(a: list[bool], b: list[bool]) -> float:
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--practice", action="store_true")
    ap.add_argument("--model")
    ap.add_argument("--hand-sample", action="store_true")
    ap.add_argument("--agreement")
    args = ap.parse_args()
    raw = ROOT / "results" / "raw"
    out_dir = ROOT / "results" / "analysis"

    if args.practice:
        paths = [raw / "pilot_n20.csv", *sorted(raw.glob("practice2b_*.csv"))]
        text = report(load(paths), "PRACTICE ONLY: reasoning codes (not real Stage 2 data)")
        (out_dir / "practice_reasoning.md").write_text(text + "\n", encoding="utf-8")
        print(text)
        return 0

    if not reasoning_locked():
        print("STOP: the reasoning codebook is not locked yet.")
        return 1

    if args.model:
        paths = [raw / f"stage2_{args.model}.csv", *sorted(raw.glob(f"stage2b_*_{args.model}.csv"))]
        text = report(load(paths), f"Stage 3.5 reasoning codes: {args.model} (exploratory)")
        (out_dir / f"reasoning_{args.model}.md").write_text(text + "\n", encoding="utf-8")
        print(text)
        return 0

    from config import CAPABILITY_ORDER
    if args.hand_sample:
        sample = hand_sample({m: load([raw / f"stage2_{m}.csv"]) for m in CAPABILITY_ORDER})
        path = ROOT.parent / "STAGE-3.5-HAND-CHECK.md"
        lines = ["# Stage 3.5 hand check", "",
                 "For each answer, read the reasoning and fill in two things using the "
                 "definitions in `llm-mechanism-design/docs/reasoning-codebook.md`:",
                 "", "- **names game?** `yes` or `no`",
                 "- **error:** for answers marked GAP, the one error code that fits best "
                 "(COLLUSIVE, TRUTHFUL_DEFAULT, COOPERATION_NORM, GROUP_OPTIMUM, MISMATCH, "
                 "KNEW_AND_DEVIATED, DUOPOLY_FORMULA) or UNCODED. Leave blank if not a GAP.", ""]
        for i, r in enumerate(sample, 1):
            lines += [f"## {i}. {r['game']} · {r['framing']} · {'GAP' if r['verdict'] == 'STRATEGIC_GAP' else 'equilibrium'}",
                      f"<!-- id: {r['model']}|{r['game']}|{r['framing']}|{r['seed']}|{r['paraphrase_idx']} -->",
                      "", f"**Played:** {r['observed_action']} · **equilibrium:** {r['equilibrium']}", "",
                      "**Question:**", "```", r["play_prompt"], "```", "**Reasoning:**", "```",
                      r["play_reasoning"], "```", "", "names game? `   `  ", "error: `   `", ""]
        path.write_text("\n".join(lines), encoding="utf-8")
        print(f"wrote {len(sample)} answers to {path}")
        return 0

    if args.agreement:
        text = Path(args.agreement).read_text(encoding="utf-8")
        blocks = re.findall(r"<!-- id: (.*?) -->(.*?)(?=\n## |\Z)", text, re.S)
        rows = {}
        for m in CAPABILITY_ORDER:
            for r in load([raw / f"stage2_{m}.csv"]):
                rows[f"{m}|{r['game']}|{r['framing']}|{r['seed']}|{r['paraphrase_idx']}"] = r
        name_h, name_a, err_h, err_a = [], [], [], []
        for key, body in blocks:
            r = rows.get(key)
            ng = re.search(r"names game\?\s*`\s*(\w*)\s*`", body)
            er = re.search(r"error:\s*`\s*(\w*)\s*`", body)
            if not r or not ng or not ng.group(1):
                continue
            name_h.append(ng.group(1).lower().startswith("y"))
            name_a.append("NAMES_GAME" in r["codes"])
            if r["verdict"] == "STRATEGIC_GAP" and er and er.group(1):
                err_h.append(er.group(1).upper())
                err_a.append(next((c for c in ERROR_CODES if c in r["codes"]), "UNCODED"))
        print(f"NAMES_GAME: n={len(name_h)}, agreement {sum(a == b for a, b in zip(name_h, name_a)) / max(1, len(name_h)):.0%}, "
              f"κ = {cohen_kappa(name_h, name_a):.2f}")
        if err_h:
            print(f"error code: n={len(err_h)}, agreement {sum(a == b for a, b in zip(err_h, err_a)) / len(err_h):.0%}")
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
