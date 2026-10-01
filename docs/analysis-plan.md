# Analysis plan — Stage 3

**Status:** DRAFT. Locked by fingerprint in `analysis/lock.py` before any real Stage 2
answer is fitted. Written while Stage 2 was still running; built and tested only on
simulated data and on the Stage 1 practice run.

This document turns the analysis sections of pre-registration 1 (osf.io/2uqpj, Section 5)
and pre-registration 2 (osf.io/6hz8d, Section 3) into exact procedures. Where the
pre-registrations already decide something, this plan only says how it is computed.
Where they leave a choice open — mainly how the quantal response model is specified —
the choice is made here, before seeing any confirmatory data, with the reason.

---

## 1. Which answers are analysed

- **Counted:** answers whose maths check was passed — AT_EQUILIBRIUM and STRATEGIC_GAP.
- **Excluded, and reported as a rate for every cell:** COMPETENCE_GAP (failed the maths
  check), PARSE_FAIL (unreadable answer), PROBE_FORMAT_FAIL (maths check not answered as
  a number or a single label).
- **Never counted:** server refusals (INFRA_FAIL). They are re-asked until answered.
- A model is analysed only when its block is complete: every planned question has
  exactly one answer (`experiments/check_stage2.py`), and every answer re-scores
  identically from its seed (`experiments/verify_scoring.py`).

## 2. Stage 2A main test (pre-registration 1)

For each model and each of the four games: the share of equilibrium play among counted
answers, normal vs disguised.

- **Test:** two-sided two-proportion z-test. Where both cells are identical at 0% or
  100%, p = 1.
- **Correction:** Holm across the four games, within each model, family-wise α = 0.05.
- **Robustness:** Fisher's exact test reported beside it. If the two disagree about
  significance, both are reported and the z-test stays primary, as registered.
- **Public goods (predicted null):** two one-sided tests (TOST) for equivalence within
  ±13 percentage points. The null is supported only if equivalence is shown; a
  non-significant difference alone is not evidence of no effect.

## 3. λ and Δλ (the headline measure)

**Model.** Logit quantal response: P(move a) ∝ exp(λ · u(a)), where u(a) is the move's
expected payoff. λ is estimated separately for every model × game × wording cell.

**Expected payoffs, per game** (`analysis/qre.py`):

| Game | u(a) and beliefs about the other players | Why |
|---|---|---|
| Repeated PD (incl. trap, sweep, endgame) | Symmetric logit QRE of the stage game: the opponent cooperates with probability p, the fixed point of the model's own response. Continuation play ignored. | With a dominant stage action and a known horizon, continuation play does not change the equilibrium action; modelling all history-dependent strategies would be intractable and unidentified from one decision per question. |
| Public goods (incl. trap, sweep) | u(g) = (M/n − 1)·g. No beliefs needed. | Each token returns M/n to its owner whatever the others do. |
| Cournot (incl. trap, sweep) | Symmetric logit QRE: expected profit given the rivals' mean quantity, which is the fixed point of the model's own response. n = 2, or 3 in the trap. | Profit is linear in the rivals' total, so only their mean matters. |
| Vickrey (incl. trap, sweep) | Logit response to rivals who bid their equilibrium bid (value ÷ the payment multiplier) with values uniform on [10, 100]. | The questions don't state the rivals' values; [10, 100] is the range the questions themselves draw from. |

**Numeric answers** are placed on a grid with step 0.5 that also contains the exact
equilibrium answer. Each answer is matched to the nearest grid point; answers outside the
possible range (e.g. a negative bid) are matched to the nearest end and counted and
reported.

**Estimation.** Posterior over a grid of 481 λ values, log-uniform from 0.001 to 1,000,
with a flat prior on log λ. Reported: posterior median and 95% interval.

**The ceiling.** When more than 5% of the posterior lies in the top 5% of the log-λ range,
the cell is flagged CEILING and reported only as "λ ≥ (2.5th percentile)". For Δλ:
- both wordings at the ceiling → "no difference detectable in λ";
- one wording at the ceiling → a one-sided bound only.
In those cases the main test (Section 2) carries the result.

**Δλ = λ(normal) − λ(disguised)**, from the two independent posteriors: median, 95%
interval and P(Δλ > 0).

**Comparisons are within a game only.** λ is in each game's own payoff units, so λ values
are never compared across games. Normal and disguised wordings of a game have identical
payoffs, so Δλ within a game is comparable.

## 4. Wording check

Equilibrium share by wording (1, 2, 3) within each framing, set against the
normal-vs-disguised change. If the spread between wordings is as large as the change
between framings, the disguise effect for that game is reported as not distinguishable
from a wording effect.

## 5. Stage 2B (pre-registration 2)

- **Block B (traps), main test:** for each trap, the share of correct answers, normal vs
  disguised, Cochran–Mantel–Haenszel test stratified by model, Holm across the four traps.
  Per-model two-proportion tests as secondary.
- **Block B, recall signature:** the share of textbook answers (Vickrey: within 0.5 of the
  value; Cournot: within 0.5 of (a − c)/3b; PD: defect; public goods: 0), normal vs
  disguised, same tests.
- **Block C:** per game, logistic regression of correct ~ wording × size + model; the test
  is the wording × size interaction, Holm across the four games.
- **Block D:** gpt-oss only. Logistic regression of correct ~ wording × effort (low,
  medium = Stage 2A, high, as an ordered variable); the test is the interaction. Maths-check
  pass rates reported for each effort level beside every comparison.
- **Block E:** defection rate by round and wording; normal vs disguised at each round,
  Holm across the three rounds; the trend across rounds 5, 9, 10 within each wording.
- λ is fitted for Stage 2B cells with the same models as Section 3, as secondary
  description.

*(The Stage 2B code is added to the lock before Stage 2B data is analysed.)*

## 6. How the method was checked before the lock

- **Parameter recovery** (`analysis/recovery.py`): for every game, simulated "models" with
  a chosen λ answer the planned questions; the fit must recover λ (95% interval covering
  the true value in ≥ 85% of 20 repetitions), flag a perfect model as CEILING, and recover
  a built-in normal-vs-disguised gap with the right sign.
- **Practice run** (Stage 1, gpt-oss, 20 per cell, already seen and not confirmatory):
  the full pipeline was run end to end. This found and fixed a bug in reading the
  equivalence test, which had printed a negative p-value.

## 7. What happens after the lock

Any change after the lock — including a bug fix — is recorded in
`docs/deviations-from-preregistration.md` with the reason and both results, old and new.
