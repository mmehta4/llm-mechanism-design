# Analysis plan for Stage 2C (the extreme disguise)

**Purpose:** turn pre-registration 3 (osf.io/cqnsy), Section 3, into exact steps, and lock those
steps together with the code (`analysis/stage2c.py`, `analysis/slips.py`) **before any Stage 2C
answer is analysed**. Where pre-registration 3 left a choice open, the choice is made here and
marked *(choice)*.

**What had been seen when this was written:** Stage 2C collection had started (2026-10-02,
after registration). The author of this plan saw the live board's progress counts and the
verdict of Nemotron's first Stage 2C answer while checking the file format. No Stage 2C
analysis had been run. The code was tested only on made-up Stage 2C answers built from
Stage 2A data (`--synthetic`) and on unit tests.

---

## 1. Pairs

Each Stage 2C question (game g, seed s, wording w) is paired with the two Stage 2A questions
with the same g, s and w: its **normal** twin and its **disguised** twin. A comparison uses a pair
only when **both** of the answers it compares count (maths check passed: `AT_EQUILIBRIUM` or
`STRATEGIC_GAP`). Server refusals never count; they are re-asked during collection.

## 2. Scoring

1. **Fraction-slip rule** (`analysis/slips.py`, fixed in pre-registration 3): applied to every
   numeric answer in both stages. The answer is then equilibrium play if it is within **±0.5** of
   that question's equilibrium, in that question's own units, as in every earlier stage.
2. **Uncorrected results** (the verdicts recorded at collection) are reported beside.
3. **Repeated PD:** the recorded verdict (cooperate/defect in that question's own labels).

*(choice, stated openly)* ±0.5 in the extreme question's own units is more lenient than
±0.5 in the Stage 2A units for two games: ±1.5 on the Vickrey offer (x is a third of
the offer) and ±1 on the Cournot amount (x is half of it). That makes a drop slightly
**harder** to find. The registered test keeps ±0.5 in the question's own units. A
**sensitivity analysis, not registered**, judges extreme answers by their decoded value with
±0.5 in Stage 2A units, and is labelled as such.

## 3. Main test: normal (2A) vs extreme (2C)

- **Per model and game:** paired 2×2 table of equilibrium play; **exact McNemar test**
  (two-sided binomial test on the discordant pairs). **Holm** across the four games within each
  model.
- **Effect size:** paired difference, normal − extreme, with a **95% Agresti–Min interval**
  *(choice)*: add 0.5 to each of the four cells, then the Wald interval.
- **Pooled across models:** the Mantel–Haenszel test for matched pairs. With every pair its own
  stratum, this equals the exact McNemar test on the discordant pairs **summed over the four
  models**, and that is how it is computed. **Holm** across the four games.

## 4. Secondary analyses (registered)

- The same test, **disguised (2A) vs extreme**.
- **Conversion slips** (extreme only): Vickrey answer within 0.5 of the prize, or of prize − 5;
  Cournot answer within 0.5 of K/3, or of K/3 − 4. These are counted per model and game (as a
  share of counted answers and of missed answers). The main test is repeated with conversion
  slips counted as equilibrium play.
- **Fraction slips:** the number of answers the rule changed, per model, game and stage.

## 5. Recognition

- **`NAMES_GAME`** (codebook v1, `analysis/reasoning.py`, κ = 1.00 against hand coding): the
  reasoning names the game, and the question did not.
- Disguised (2A) vs extreme, on pairs where both answers count. **Exact McNemar** per model and
  game, and pooled across models (summed discordant pairs).
- **Exploratory:** within the extreme wording, equilibrium play when the game was named vs when
  it was not (Fisher's exact test, labelled exploratory).

## 6. λ

- Fitted with the locked Stage 3 method (`analysis/qre.py`, `analysis/fit.py`) on the same
  paired, counted, slip-corrected answers.
- Extreme answers are **decoded** into the Stage 2A action space: offer = 3x + 5;
  amount = 2x + 4; contribution = endowment − keep. They are then fitted with the Stage 2A
  game's payoffs, so Vickrey, Cournot and public goods λ are on the Stage 2A scale.
- **Repeated PD:** the extreme payoffs are 2u − 4 of the Stage 2A table. Fitting extreme PD
  answers on the original Stage 2A payoffs gives exactly 2 × the λ fitted on the extreme payoffs,
  which is pre-registration 3's "multiplied by 2": the shift cancels in the logit, and doubling
  every payoff difference doubles λ. This is done without leaving the fixed λ grid, and a unit
  test checks the identity.
- Reported: λ normal, λ extreme and Δλ = normal − extreme, with the ceiling handling of the
  Stage 3 method.

## 7. Predictions check

The report ends with a mechanical check of each committed prediction in pre-registration 3,
Section 2:
- recognition ranges and play changes, pooled over the four models;
- the per-model Cournot drops.

Ranges are read inclusively. *(choice)* Vickrey's "about −10 points" is read as a drop of 5–15
points; the PD's "above the normal-wording rate" as strictly above.

## 8. When it runs

- **Per model:** only when that model's Stage 2A and Stage 2C blocks are both complete
  (`experiments/check_stage2.py`).
- **Pooled:** only when all four models are complete.
- **Lock:** the code refuses real data unless the Stage 3 lock (`analysis/lock.py`) and this
  plan's lock (`STAGE2C_ANALYSIS_SHA256` in `analysis/stage2c.py`, covering that file,
  `analysis/slips.py` and this document) both hold.
- **After the lock:** a bug fix is allowed only as a recorded deviation.
