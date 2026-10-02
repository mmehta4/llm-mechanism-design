"""Stage 3.5, codebook version 2: one main error code per missed answer, in a fixed order.

    python analysis/reasoning_v2.py --practice          # practice runs only
    python analysis/reasoning_v2.py --hand-sample       # fresh 60 for round 2 (needs the lock)
    python analysis/reasoning_v2.py --agreement FILE    # round-2 κ
    python analysis/reasoning_v2.py --model nemotron    # per-block report (needs the lock)

Rules: docs/reasoning-codebook-v2.md. Version 1 (analysis/reasoning.py) is left exactly as
locked; its text patterns are reused here, not changed. Recognition codes come from v1.
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

from analysis.reasoning import (BACKWARD, COOP_NORM, DOMINANCE, GROUP, NUMBER, _has, _num,
                                cohen_kappa, family)
from analysis.reasoning import code as code_v1
from games import GAMES

REASONING_V2_SHA256 = "e761bdc1d885690f7300f426f357d06b5d62c651c3c37b38f045b54a9421d177"
CODEBOOK = ROOT / "docs" / "reasoning-codebook-v2.md"


def _fingerprint() -> str:
    text = Path(__file__).read_text(encoding="utf-8")
    body = "\n".join(l for l in text.splitlines() if not l.startswith("REASONING_V2_SHA256 ="))
    return hashlib.sha256(body.encode() + b"\0" + CODEBOOK.read_bytes()).hexdigest()


def locked() -> bool:
    return REASONING_V2_SHA256 is not None and _fingerprint() == REASONING_V2_SHA256


ORDER = {
    "cournot": ["MISMATCH", "KNEW_AND_DEVIATED", "DUOPOLY_FORMULA", "COLLUSIVE",
                "CLAIMED_NASH_WRONG", "UNCODED"],
    "vickrey": ["TRUTHFUL_DEFAULT", "UNCODED"],
    "repeated_pd": ["LABEL_SWAP", "KNEW_OVERRODE", "COOPERATION_NORM", "UNCODED"],
    "public_goods": ["GROUP_OPTIMUM", "UNCODED"],
}
NASH_CLAIM = r"nash|equilibri"
KNEW = BACKWARD + r"|" + DOMINANCE + r"|nash|subgame|rational"


def label_swap(text: str, chosen: str) -> bool:
    """The reasoning calls the option it CHOSE the dominant one. Only reached for a
    cooperative choice, so in that question's table the claim is backwards."""
    L = re.escape(chosen)
    return bool(re.search(rf"\b{L}\b[^.]{{0,40}}(?i:(?:strictly |weakly )?dominates|is (?:the )?dominant)", text)
                or re.search(rf"(?i:dominant (?:strategy|choice|option|action|move))[^.]{{0,40}}\b{L}\b", text))


def fits(row: dict, p: dict, text: str) -> set[str]:
    """Every version-2 error code whose definition this missed answer meets."""
    game, fam = row["game"], family(row["game"])
    ans, eq = _num(row["observed_action"]), _num(row["equilibrium"])
    out: set[str] = set()
    if fam == "cournot" and ans is not None and eq is not None:
        nums = [float(x) for x in NUMBER.findall(text)]
        if nums and abs(nums[-1] - eq) <= 0.5:
            out.add("MISMATCH")
        elif any(abs(x - eq) <= 0.5 for x in nums):
            out.add("KNEW_AND_DEVIATED")
        if game == "cournot_trap" and abs(ans - (p["a"] - p["c"]) / (3 * p["b"])) <= 0.5:
            out.add("DUOPOLY_FORMULA")
        if abs(ans - (p["a"] - p["c"]) / (2 * p.get("n_firms", 2) * p["b"])) <= 0.5:
            out.add("COLLUSIVE")
        if _has(NASH_CLAIM, text) and not any(abs(x - eq) <= 0.5 for x in nums):
            out.add("CLAIMED_NASH_WRONG")
    if game == "vickrey_trap" and ans is not None and abs(ans - p["value"]) <= 0.5:
        out.add("TRUTHFUL_DEFAULT")
    if fam == "repeated_pd":
        coop = "C" if row["framing"] == "named" else p["coop"]
        chosen = str(row["observed_action"]).strip().upper()
        if chosen == coop.upper():
            if label_swap(text, chosen):
                out.add("LABEL_SWAP")
            if _has(KNEW, text):
                out.add("KNEW_OVERRODE")
            if _has(COOP_NORM, text):
                out.add("COOPERATION_NORM")
    if fam == "public_goods" and ans is not None and eq is not None and ans > eq + 0.5 and _has(GROUP, text):
        out.add("GROUP_OPTIMUM")
    return out


def main_code(row: dict) -> str | None:
    """The first code in the game's fixed order that fits; None if not a missed answer."""
    if row["verdict"] != "STRATEGIC_GAP":
        return None
    p = GAMES[row["game"]].sampler(seed=int(row["seed"]))
    f = fits(row, p, row.get("play_reasoning") or "")
    return next(c for c in ORDER[family(row["game"])] if c in f or c == "UNCODED")


def load(paths: list[Path]) -> list[dict]:
    rows = []
    for path in paths:
        if path.exists():
            with path.open(encoding="utf-8") as f:
                for r in csv.DictReader(f):
                    if r["verdict"] in ("AT_EQUILIBRIUM", "STRATEGIC_GAP"):
                        r["codes"] = code_v1(r)
                        r["main"] = main_code(r)
                        rows.append(r)
    return rows


def report(rows: list[dict], title: str) -> str:
    out = [f"# {title}", "", "Main error code of each missed answer (codebook v2, fixed order).", ""]
    by = defaultdict(list)
    for r in rows:
        if r["main"]:
            by[(family(r["game"]), r["framing"])].append(r["main"])
    for fam, order in ORDER.items():
        out += [f"## {fam}", "", "| Wording | Missed | " + " | ".join(order) + " |",
                "|---|---:|" + "---:|" * len(order)]
        for fr in ("named", "disguised"):
            c = Counter(by[(fam, fr)])
            n = sum(c.values())
            out.append(f"| {fr} | {n} | " + " | ".join(str(c[k]) for k in order) + " |")
        out.append("")
    return "\n".join(out)


def round1_ids() -> set[str]:
    path = ROOT.parent / "STAGE-3.5-HAND-CHECK.md"
    return set(re.findall(r"<!-- id: (.*?) -->", path.read_text(encoding="utf-8"))) if path.exists() else set()


def key(model: str, r: dict) -> str:
    return f"{model}|{r['game']}|{r['framing']}|{r['seed']}|{r['paraphrase_idx']}"


def hand_sample(rows_by_model: dict[str, list[dict]], exclude: set[str]) -> list[dict]:
    rng = random.Random(20261003)
    picked = []
    for model, rows in sorted(rows_by_model.items()):
        rows = [r for r in rows if key(model, r) not in exclude]
        for fr in ("named", "disguised"):
            pool = [r for r in rows if r["framing"] == fr]
            gaps = [r for r in pool if r["verdict"] == "STRATEGIC_GAP"]
            rest = [r for r in pool if r["verdict"] != "STRATEGIC_GAP"]
            n = 8 if fr == "named" else 7
            take = rng.sample(gaps, min(len(gaps), 5))
            take += rng.sample(rest, min(len(rest), n - len(take)))
            picked += [dict(r, model=model) for r in take]
    rng.shuffle(picked)
    return picked


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--practice", action="store_true")
    ap.add_argument("--hand-sample", action="store_true")
    ap.add_argument("--agreement")
    ap.add_argument("--model")
    args = ap.parse_args()
    raw = ROOT / "results" / "raw"
    if args.practice:
        print(report(load([raw / "pilot_n20.csv", *sorted(raw.glob("practice2b_*.csv"))]),
                     "PRACTICE ONLY: codebook v2"))
        return 0
    if not locked():
        print("STOP: codebook v2 is not locked yet.")
        return 1
    from config import CAPABILITY_ORDER
    if args.model:
        parts = []
        for block, path in [("2A", raw / f"stage2_{args.model}.csv")] + [
                (f"2B-{b}", raw / f"stage2b_{b}_{args.model}.csv") for b in "BCDE"]:
            rows = load([path])
            if rows:
                parts.append(report(rows, f"{args.model} · Stage {block} · error codes v2 (exploratory)"))
        text = "\n\n---\n\n".join(parts)
        (ROOT / "results" / "analysis" / f"reasoning_v2_{args.model}.md").write_text(text + "\n", encoding="utf-8")
        print(text)
        return 0
    if args.hand_sample:
        sample = hand_sample({m: load([raw / f"stage2_{m}.csv"]) for m in CAPABILITY_ORDER}, round1_ids())
        lines = ["# Stage 3.5 hand check — round 2", "",
                 "Fresh answers: none of these were in round 1. For each **GAP** answer, pick the "
                 "**first** code in the list under it that fits (definitions: "
                 "`llm-mechanism-design/docs/reasoning-codebook-v2.md`). Only the codes listed "
                 "under an answer are allowed for it. Answers marked `equilibrium` need nothing.", ""]
        for i, r in enumerate(sample, 1):
            gap = r["verdict"] == "STRATEGIC_GAP"
            lines += [f"## {i}. {r['game']} · {r['framing']} · {'GAP' if gap else 'equilibrium'}",
                      f"<!-- id: {key(r['model'], r)} -->", "",
                      f"**Played:** {r['observed_action']} · **equilibrium:** {r['equilibrium']}", "",
                      "**Question:**", "```", r["play_prompt"], "```", "**Reasoning:**", "```",
                      r["play_reasoning"], "```", ""]
            if gap:
                lines += ["Allowed, in order: " + " → ".join(f"`{c}`" for c in ORDER[family(r['game'])]), "",
                          "error: `   `", ""]
        path = ROOT.parent / "STAGE-3.5-HAND-CHECK-2.md"
        path.write_text("\n".join(lines), encoding="utf-8")
        print(f"wrote {len(sample)} answers ({sum(r['verdict'] == 'STRATEGIC_GAP' for r in sample)} GAP) to {path}")
        return 0
    if args.agreement:
        text = Path(args.agreement).read_text(encoding="utf-8")
        rows = {key(m, r): r for m in CAPABILITY_ORDER for r in load([raw / f"stage2_{m}.csv"])}
        hand, auto, fams = [], [], []
        for k, body in re.findall(r"<!-- id: (.*?) -->(.*?)(?=\n## |\Z)", text, re.S):
            r = rows.get(k)
            m = re.search(r"error:\s*`\s*(\w*)\s*`", body)
            if r and r["main"] and m and m.group(1):
                hand.append(m.group(1).upper()); auto.append(r["main"]); fams.append(family(r["game"]))
        n = len(hand)
        po = sum(a == b for a, b in zip(hand, auto)) / n
        hc, ac = Counter(hand), Counter(auto)
        pe = sum(hc[c] * ac[c] for c in set(hc) | set(ac)) / n ** 2
        print(f"main error code: n={n}, agreement {po:.0%}, κ = {(po - pe) / (1 - pe):.2f}")
        for fam in ORDER:
            idx = [i for i, f in enumerate(fams) if f == fam]
            if idx:
                print(f"  {fam}: n={len(idx)}, agreement {sum(hand[i] == auto[i] for i in idx) / len(idx):.0%}")
        for c in sorted(set(hand) | set(auto)):
            if hc[c] >= 5 or ac[c] >= 5:
                print(f"  {c}: yes/no κ = {cohen_kappa([h == c for h in hand], [a == c for a in auto]):.2f} "
                      f"(you {hc[c]}, computer {ac[c]})")
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
