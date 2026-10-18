# Equilibrium or Retrieval?

**Do LLM agents derive or recall game-theoretic equilibria, and what that means for mechanism design.**

Meet Mehta · Independent researcher · October 2026 · [Paper (PDF)](paper/main.pdf)

LLMs play textbook games well, but a model can reach the textbook answer by deriving it from the
rules or by recognising a famous game and recalling its answer. This study separates the two with
*isomorphic twins*. Each question is asked in its standard wording and in disguised wordings that
keep the numbers, rules and information but drop the game's vocabulary. Every answer is paired
with a maths check in the same wording.

Four models from four developers answer **20,368 questions** in four pre-registered studies, covering a Vickrey auction,
a Cournot duopoly, a finitely repeated prisoner's dilemma and a public goods game.

## Main results

| | gpt-oss-120b | Nemotron 3 Ultra | Kimi K3 | Gemini 3.5 Flash Lite |
|---|---|---|---|---|
| Cournot equilibrium play, normal → disguised → extreme | 96 → 80 → 30% | stays 88–100% | stays 99–100% | 96 → 4% |
| Traps (the textbook answer is wrong) | falls in under the standard wording | not fooled | not fooled | fails the trap arithmetic |
| Pattern | graded retrieval | hidden but still solved | hidden but still solved | retrieval and comprehension limits |

- **Prisoner's dilemma:** recognising the game retrieves a script of cooperation, and removing the
  familiar wording raises defection in every model.
- **Endgame:** every model defects in the announced last round, and three of the four cooperate
  earlier, as people do.
- **Quantal response:** logit QRE fails pre-registered calibration for every model.
- **Mechanism design:** a cooperation subsidy derived from fitted QRE reaches its 90% target but
  overpays by up to 20 times, and classical theory predicts the response better.
  - The paper proves why: below the subsidy's halfway point, no regular QRE produces cooperation
    above one half.

## Pre-registrations (OSF)

| Study | Registration | Locked document |
|---|---|---|
| Stage 2A: normal vs disguised | [osf.io/2uqpj](https://osf.io/2uqpj) | `docs/preregistration-1.md` |
| Stage 2B: traps, size sweep, endgame | [osf.io/6hz8d](https://osf.io/6hz8d) | `docs/preregistration-2.md` |
| Stage 2C: extreme disguise | [osf.io/cqnsy](https://osf.io/cqnsy) | `docs/preregistration-3.md` |
| Stage 5: the subsidy test | [osf.io/qg43y](https://osf.io/qg43y) | `docs/preregistration-4.md` |

- **Fingerprints:** each document's SHA-256 is recorded in git and matches the file uploaded to
  OSF.
- **Locked analysis code:** the analysis scripts are fingerprinted too, and they refuse to run on
  real data if they have been changed.
- **Deviations:** every departure from the registrations is in
  `docs/deviations-from-preregistration.md`.

## Reproducing the results

Every answer is committed in `results/raw/`, so every number in the paper can be recomputed
without any API calls.

```bash
python3.12 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python -m pytest -q                              # 225 tests: games, theory, mechanisms, analyses

python analysis/stage2a.py --model nemotron      # Stage 2A, one model at a time
python analysis/stage2b.py --block B             # traps (also: --block C, --block E)
python analysis/stage2c.py --pooled              # extreme disguise
python analysis/stage5.py --pooled               # subsidy test
python analysis/gate.py                          # QRE calibration (decision gate)
python paper/make_figures.py                     # data figures
```

The outputs are written to `results/analysis/`. Each answer row records the exact model version
string, seed, paraphrase, full prompt, raw reply and reasoning.

To collect new data, copy `.env.example` to `.env`, add your own API keys, and run the scripts in
`experiments/`.

## Layout

| Path | Contents |
|---|---|
| `games/` | The games in every wording, the traps, the subsidy rule and the maths checks |
| `theory/` | Equilibrium calculators, tested against textbook solutions |
| `mechanisms/` | QRE solvers for the auction (payment multiplier, reserve) and the PD subsidy |
| `agents/` | Model wrappers |
| `experiments/` | Data-collection runners for each study (resumable; each question is asked exactly once) |
| `analysis/` | The locked, registered analyses; QRE fitting; reasoning codes |
| `results/raw/` | Every answer, one CSV per model and block |
| `results/analysis/` | Analysis outputs |
| `paper/` | LaTeX source, figures and the compiled PDF |
| `docs/` | Pre-registrations, analysis plans, codebooks, deviations log |
| `tests/` | Unit tests |

## Citation

```bibtex
@misc{mehta2026equilibrium,
  author = {Mehta, Meet},
  title  = {Equilibrium or Retrieval? Do {LLM} Agents Derive or Recall Game-Theoretic Equilibria,
            and What That Means for Mechanism Design},
  year   = {2026},
  note   = {Pre-registrations: osf.io/2uqpj, osf.io/6hz8d, osf.io/cqnsy, osf.io/qg43y},
  url    = {https://github.com/mmehta4/llm-mechanism-design}
}
```

Claude (Anthropic) assisted with code, typesetting and drafting. The research questions,
predictions and decisions are the author's.
