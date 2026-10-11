# Pre-registration 4: a mechanism derived for noisy agents

**Status:** completed at the decision gate on 2026-10-11; locked before any Stage 5 question is
asked.
**Scope:** Stage 5, the prisoner's dilemma with a cooperation subsidy, four models,
1,600 questions.
**Relation to earlier registrations:** pre-registrations 1–3 (osf.io/2uqpj, osf.io/6hz8d,
osf.io/cqnsy) are unchanged.

---

## 0. Why this study

Stages 2A to 2C measure how the models play. Stage 4 derived what rules should do for players
who are noisy in the logit-QRE sense (`docs/stage4-theory.md`):
- **Theorem 3:** the subsidy for target cooperation p\* is τ(p\*, λ) = ΔU(p\*) + logit(p\*)/λ.
- **Corollary 1:** at τ = 1.5, every regular-QRE population cooperates 50% in the stage game, whatever its λ.

Stage 5 tests whether a mechanism derived from each model's fitted λ does what the theory says,
and whether it beats the classical "guess".

## 1. Design

As in `docs/stage5-design.md` (confirmed by the author, with amendments):
- Stage 2A's named 10-round PD, round 1.
- The subsidy is a separate rule line: "each player is paid an extra τ points in every round in
  which that player chooses C". τ is written to one decimal, 0.0 included.
- Levels: τ = 0.0, 1.5, 2.5 and τ\*ₘ = 1.9 + ln 9 / λ̂ₘ (rounded to 0.1). Capped at 50 if
  λ̂ₘ < 0.046; dropped if λ̂ₘ ≥ 3.66 (`docs/decision-gate.md`).
- 100 per level per model, balanced 34/33/33 across the three paraphrases, with new seeds.
- The maths check is C against D, including the subsidy.

**Stage-game assumption.** τ = 1.5 makes the stage game chicken. In the 10-round game, round-1
cooperation is then subgame-perfect (Benoît & Krishna, 1985), so the 50% prediction holds only
for the stage-game QRE. Stated as a limitation.

**Fitted λ̂ₘ and τ\*ₘ** (`analysis/gate.py`, posterior median of each model's Stage 2A
named-wording PD fit):

| Model | λ̂ (PD, named) | τ\* for 90% | Note |
|---|---:|---:|---|
| gpt-oss-120b | 0.579 | 5.7 | |
| Nemotron 3 Ultra | 0.154 | 16.2 | |
| Kimi K3 | 0.0075 | 50.0 | floor rule: λ̂ < 0.046, so τ\* is capped at 50 (uncapped: 294.9) |
| Gemini 3.5 Flash Lite | 0.0032 | 50.0 | floor rule: capped at 50 (uncapped: 697.2); λ̂ is at the lower edge of the grid |

The exact values used by the runner are in `experiments/stage5.py` (`LAMBDA_HAT`).

## 1b. The decision gate (run 2026-10-11)

**Result** (`results/analysis/gate.md`), by the author's criteria in `docs/decision-gate.md`:
fits are **poor for all four models**, so pre-registration 1's gate gives **option 3**.

| Model | Games calibrated (held-out ±10 points) |
|---|---:|
| gpt-oss-120b | 0 of 4 |
| Nemotron | 1 of 4 |
| Kimi | 1 of 4 (PD hard fail: cooperation above 50%) |
| Gemini | 1 of 4 (PD hard fail) |

**Disclosed with the result: a grid artifact in the Vickrey cells.**
- At the top of the registered λ grid (λ = 1000), QRE predicts 82–90% equilibrium play, while
  every model plays it 100%. So the Vickrey cells cannot pass the ±10 rule at any precision.
- Counting Vickrey as calibrated for every model would not change the verdict: no model would
  reach 3 of 4.
- The remaining failures are substantive. The models' departures from equilibrium are rare,
  large and discrete (fraction slips, collusive quantities, cooperation norms), not
  payoff-scaled logit noise.

**What the author decided, after seeing the gate (2026-10-11).** The registered gate text says
that under option 3 "Stage 4 is about why". The author's mixed-results rule (decision-gate.md),
written before the fits, already committed to running Stage 5 for every model and reading a
derived-level failure of a poor-fit model as expected under option 3, not as the mechanism
failing. The author applies the same rule here, where every model has a poor fit. Stage 5 runs
for all four models, as designed, as the direct test of *why* QRE fails.

- **Tests 1 and 3 are the informative ones:** QRE vs classical at τ = 2.5, and the stage-game
  halfway point at τ = 1.5.
- **A Test 2 failure** (cooperation below 75% at τ\*) is reported as "expected under option 3".

## 2. Predictions

**Authorship.** Written by the author on 2026-10-03. That was before the Stage 2A analyses of
gpt-oss-120b, Kimi K3 and Gemini 3.5 Flash Lite existed; only Nemotron's had been run. Nemotron's
values at τ = 0 and 1.5 repeat the author's informal predictions committed earlier that day
(`docs/stage4-informal-predictions.md`).

**Cooperation rate (%) by subsidy level:**

| Model | τ = 0 | τ = 1.5 | τ = 2.5 | τ\* |
|---|---:|---:|---:|---:|
| Nemotron | 41 | 65 | 90 | 98 |
| gpt-oss-120b | 10 | 45 | 95 | 99 (likely no separate τ\*: λ at the ceiling, gate rule 4c) |
| Kimi K3 | 25 | 60 | 90 | 97 |
| Gemini 3.5 Flash Lite | 20 | 45 | 70 | 85 |

**Shape, relative to the QRE curve at each model's λ̂:**

| Model | Prediction |
|---|---|
| Nemotron | steeper than QRE (cooperation norm) |
| gpt-oss-120b | on the QRE curve (sharp: high λ, near-classical) |
| Kimi K3 | steeper than QRE (cooperation norm) |
| Gemini 3.5 Flash Lite | flatter (weakest at integrating the added rule) |

**Headline as originally worded** (τ\* gives more cooperation than 2.5): yes, for every model
with a separate τ\*. This is near-mechanical, since τ\* > 2.5 whenever λ < 3.66.

**Headline as amended (the real prediction):** at τ = 2.5, **classical theory (100%) predicts
better than QRE for Nemotron and Kimi**, and τ\* overshoots 90% (the mechanism overpays).
**QRE's prediction is closest only for Gemini 3.5 Flash Lite.**

**Reasoning.** The low PD λ values mostly reflect a cooperation norm, not insensitivity to
payoffs. Once the subsidy makes C dominant, the models respond almost classically, and a λ
fitted on the plain PD under-predicts that response.

## 3. How the results will be judged

**Which answers count:** the maths check passed. Refusals are re-asked, never counted.

**Test 1, derived vs guessed theory, at τ = 2.5:** per model, the absolute error
of QRE's prediction (at λ̂ₘ) against that of classical theory (100%). QRE wins if its error is
smaller; a bootstrap 95% interval for the difference in errors is reported.

**Test 2, the derived mechanism, at τ\*ₘ:** per model, is the observed rate within 90 ± 15?
A 95% interval is reported.

**Test 3, the stage-game halfway point, at τ = 1.5:** an exact binomial test against 0.5, with
Holm across models. It is read with the interpretation key (`docs/interpretation-key.md`),
including the repeated-game reading.

**Test 4, calibration:** each level against the QRE curve at λ̂ₘ, with intervals.

**The decision gate** uses the author's criteria in `docs/decision-gate.md` (held-out
calibration ±10 points in at least 3 of 4 games; λ not compared across games; floor and
ceiling rules). **Interpretations** follow `docs/interpretation-key.md`.

**What counts as the mechanism failing:** cooperation at τ\*ₘ below 75% (more than 15 points
short of the 90% target), for a model whose derived level was not dropped.

## 4. The rules I can't change later

- **Stopping rule:** exactly 100 per level per model.
- **Earlier registrations:** unchanged.

## 5. What I'm disclosing

**What had been seen when this was completed (2026-10-11):**
- **Stage 2A results for all four models:** the complete registered analyses, including the PD
  fits that set λ̂ and τ\*.
- **Stage 2C results for all four models:** the complete registered analyses.
- **The decision gate output.**
- **Stage 2B:** the live board showed answers for every block. The registered Stage 2B analyses
  had not been run, and no block was complete for every model.
- **The Stage 4 theory,** including that τ\* depends on λ̂.

**Written before those results:**
- the predictions in Section 2 (2026-10-03, before three of the four models' Stage 2A fits);
- the gate criteria and the interpretation key (`docs/decision-gate.md`,
  `docs/interpretation-key.md`).

**Written after them:** the decision to run Stage 5 under option 3 (Section 1b).

**Authorship.** The Stage 5 design was proposed by Claude and confirmed by the author with two
amendments: the headline test and the stage-game caveat. The amendments, the gate criteria, the
interpretation key and the predictions are the author's.