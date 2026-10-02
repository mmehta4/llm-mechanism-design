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
- **Corollary 1:** at τ = 1.5, every regular-QRE population cooperates 50%, whatever its λ.

Stage 5 tests whether a mechanism derived from each model's fitted λ does what the theory says,
and whether it beats the classical "guess".

## 1. Design

As in `docs/stage5-design.md`:
- Stage 2A's named 10-round PD, round 1, with the payoffs (5, 3, 1, 0) and three paraphrases.
- The subsidy is stated as a separate rule for each player.
- Four levels per model: τ = 0, 1.5, 2.5, and τ\*ₘ = τ(0.9, λ̂ₘ), where λ̂ₘ is model m's
  Stage 2A named-wording PD λ (posterior median), rounded to 0.1 and capped at 50.
- 100 questions per level per model, using new seeds. Fixed shuffled order; exactly the planned
  count; server refusals re-asked; maths check C-vs-D including the subsidy.

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

**Headline.** Derived beats guessed: cooperation at τ\*ₘ exceeds cooperation at 2.5 for every
model. Whether each model is *steeper than QRE* (cooperation norm), *on the QRE curve*, or
*flatter* (recalled "always defect") is answered by the halfway-point test.

## 3. How the results will be judged

**Which answers count:** the maths check passed. Refusals are re-asked, never counted.

**Test 1, the halfway point (no free parameter):** per model, an exact binomial test of
cooperation at τ = 1.5 against 0.5. Holm across the four models.

**Test 2, derived vs guessed:** per model, cooperation at τ\*ₘ vs at τ = 2.5, a two-sided
two-proportion test with Holm across models. Pooled: Cochran–Mantel–Haenszel across models.

**Test 3, calibration:** per model and level, the observed rate against the QRE prediction at
λ̂ₘ, with a 95% interval. The prediction's own uncertainty from λ̂ₘ's posterior is reported
beside it.

**What counts as the mechanism failing:** cooperation at τ\*ₘ below 75% (more than 15 points
short of the 90% target) for a model with a finite, non-ceiling λ̂ₘ.

## 4. The rules I can't change later

- **Stopping rule:** exactly 100 per level per model.
- **Earlier registrations:** unchanged.

## 5. What I'm disclosing

[GATE] Everything seen before writing: all Stage 2A, 2B and 2C results available at the gate,
and the Stage 4 theory, including that the derived τ\* depends on the fitted λ.

**Authorship.** The Stage 5 design was proposed by Claude and adopted by the author; the
predictions above are the author's.
