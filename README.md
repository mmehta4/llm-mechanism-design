# Do LLM Agents Play Equilibrium?

Testing whether LLM agents behave the way classical game theory predicts in games
with provably known equilibria — and, where they don't, designing and testing a
corrective mechanism.

> **Status: Phase 0.** Scaffolding only. No findings yet. This paragraph will be
> replaced by the headline result once Phase 8 produces one.

## Setup

```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then add your API keys
python scripts/smoke_test.py
```

The smoke test runs one real Vickrey auction trial against a live model and
reports the deviation from the dominant-strategy equilibrium. If it prints a
deviation, the pipeline works.

## Layout

| Path | Contents |
|---|---|
| `games/` | Game environments — payoff logic and rules, named and disguised variants |
| `theory/` | Equilibrium calculators, unit-tested against textbook solutions |
| `agents/` | LLM wrappers, plus scripted control agents (random, heuristic, theoretical) |
| `mechanisms/` | The corrective mechanism — the project's actual contribution |
| `experiments/` | Scripts running the baseline and mechanism-test matrices |
| `analysis/` | Statistics, significance testing, figures |
| `results/raw/` | Raw trial data, committed so results can be rechecked without API spend |
| `interactive/` | Run-it-yourself demo (built last, Phase 14) |
| `docs/` | Pre-registrations and methodology notes |

## Reproducibility

Every trial row records the exact model version string, the effort level, and the
random seed. Raw results are committed to the repository so any statistic in the
writeup can be recomputed without spending API credit. See `docs/reproducibility.md`
for what can and cannot be pinned.
