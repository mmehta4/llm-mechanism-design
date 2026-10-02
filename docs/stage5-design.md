# Stage 5 design (draft for pre-registration 4)

**Status:** proposed by Claude (Stage 4 workbook, decisions 1–4) and adopted on 2026-10-03 at
the author's instruction to complete all remaining tasks. The author may revise it before
pre-registration 4 is locked. No subsidy question has been asked of any model.

**Question.** Stage 2A's named 10-round PD, round 1, all three paraphrases. The subsidy is shown
as a **separate rule line** under the unchanged payoff table, stating that it applies to each
player (`games/subsidy.py`). Folding it into the table was rejected: for 1 < τ < 2 that table is
the game of chicken, which brings back the recall confound.

**Levels (per model):**

| τ | Role |
|---|---|
| 0 | baseline; the rule line is kept ("an extra 0 points") so only the number changes between levels |
| 1.5 | Corollary 1: every regular-QRE population cooperates 50%, at any λ |
| 2.5 | the classical "guess": just above the dominance threshold T − R = 2 |
| τ\*(0.9, λ̂ₘ) | the derived mechanism: Theorem 3 at model m's fitted Stage 2A PD λ (named wording), rounded to 0.1 |

**Size.** 100 questions per level per model, 1,600 in total, normal wording only. Seeds are new,
from a separate seed block, so no Stage 2A question is repeated.

**Maths check.** C against D, including the extra payment: the answer is S + τ.

**Outcome.** The cooperation rate. At τ = 1.5 there's no single equilibrium action (rational
play mixes), so "equilibrium play" isn't the measure.

**Planned tests (to be fixed in pre-registration 4):**
1. Halfway point: exact binomial test of the τ = 1.5 cooperation rate against 0.5, per model.
2. Derived vs guessed: cooperation at τ\* vs τ = 2.5, per model, two-proportion test with Holm
   across models; plus each level against its QRE prediction at λ̂ₘ.
3. Calibration: the observed cooperation rate at each level against the QRE curve at λ̂ₘ.

**Caveat.** A model whose fitted λ is at the ceiling or the floor makes τ\* extreme. The gate
records how that is handled: τ\* is capped at 50 points, and that cap is reported.
