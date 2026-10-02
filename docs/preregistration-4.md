# Pre-registration 4: a mechanism derived for noisy agents (DRAFT, not locked)

**Status:** draft. To be completed at the decision gate (once all Stage 2A fits are in), then
locked and registered on OSF **before any subsidy question is asked**. Items marked
[GATE] need the Stage 2A fits.
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

[GATE] Fitted λ̂ₘ and τ\*ₘ:

| Model | λ̂ (PD, named) | τ\* for 90% |
|---|---:|---:|
| Nemotron | 0.154 | 16.2 |
| gpt-oss-120b | | |
| Kimi K3 | | |
| Gemini 3.5 Flash Lite | | |

## 2. Predictions

**Nemotron.** Written by the author on 2026-10-03, in git before any subsidy question existed
(`docs/stage4-informal-predictions.md`), restated here:
- **Cooperation by level:** 41% at τ = 0; 65% at 1.5; 95% at 5; 98% at 10. [AUTHOR] Guesses at
  τ = 2.5 and τ\* = 16.2 are still to be written.
- **The view:** steeper than QRE. Nemotron's low PD λ is a cooperation norm absorbed as
  "noise", so once a subsidy makes cooperation pay, cooperation jumps.

[GATE] **The other three models:** the author's numbers at τ = 0, 1.5, 2.5 and τ\*ₘ.

**Headline (author's amendment).** The comparison is between the two theories'
*predictions*, not "more subsidy gives more cooperation". At τ = 2.5, QRE's prediction is closer
to the observed rate than classical theory's 100%; and at τ\*ₘ the observed rate is within
90 ± 15. [AUTHOR] For which models do you predict each of these holds?

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

[GATE] Everything seen before writing: all Stage 2A, 2B and 2C results available at the gate,
and the Stage 4 theory, including that the derived τ\* depends on the fitted λ.

**Authorship.** The Stage 5 design was proposed by Claude and confirmed by the author with two
amendments: the headline test and the stage-game caveat. The gate criteria, the interpretation
key and the predictions are the author's.
