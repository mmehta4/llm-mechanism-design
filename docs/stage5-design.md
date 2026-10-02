# Stage 5 design (for pre-registration 4)

**Status:** proposed by Claude and **confirmed by the author on 2026-10-03** (final workbook,
Tasks 1–2), with the author's amendments. No subsidy question has been asked of any model.

## Question

- Stage 2A's named 10-round PD, round 1.
- The subsidy is a **separate rule line** under the unchanged table:
  > On top of these scores, each player is paid an extra τ points in every round in which that player chooses C.
- **"That player", not "they"** (author's fix): elsewhere in the question "they" means the other
  player, so "they choose C" could be misread as "you are paid when your opponent cooperates".
- τ is written to one decimal at every level, including **0.0**. The τ = 0.0 level, compared
  with Stage 2A (where the line is absent), also tests whether the line itself shifts behaviour.
- A test checks that each question is Stage 2A's wording plus this one line.

## Levels (per model)

| τ | Role |
|---|---|
| 0.0 | baseline |
| 1.5 | the stage-game halfway point. **Not parameter-free in the 10-round game:** for 1 < τ < 2 the stage game is chicken, with two pure equilibria, so round-1 cooperation can be subgame-perfect (Benoît & Krishna, 1985; author's correction). Kept for comparability with the stage-game λ fits; the assumption is stated as a limitation |
| 2.5 | the classical "guess": just above the dominance threshold T − R = 2 |
| τ\* = 1.9 + ln 9 / λ̂ₘ | the derived mechanism: 90% target at model m's fitted λ, rounded to 0.1. Capped at 50 at the floor (λ < 0.046); dropped at the ceiling (λ ≥ 3.66), where it would fall at or below 2.5 (`docs/decision-gate.md`) |

## Size

- **100 per level per model**, normal wording only.
- **Balanced across the three Stage 2A paraphrases (34/33/33)**, so wording is not confounded
  with level.
- New seeds.
- **Maths check:** C against D, including the subsidy (answer S + τ). A misreading of the rule
  gives 0, so the check would catch it.

## Outcome and tests (author's amendment to the headline)

"Cooperation at τ\* exceeds cooperation at 2.5" would almost certainly pass, since τ\* > 2.5
whenever λ < 3.66. So it tests nothing. Instead:

1. **Derived vs guessed theory, at τ = 2.5:** is QRE's prediction (at λ̂ₘ) closer to the
   observed rate than classical theory's 100%? Compare absolute errors.
2. **The derived mechanism, at τ\*:** is the observed rate within 90 ± 15 (75–100 in practice)?
   An observed rate of about 100% is reported as "target exceeded: QRE under-predicts
   responsiveness; the mechanism overpays".
3. **The stage-game halfway point, at τ = 1.5:** an exact binomial test against 0.5, read with
   `docs/interpretation-key.md` (the repeated-game caveat applies).
4. **Calibration:** each level against the QRE curve at λ̂ₘ.

## Two definitions made explicit in the analysis code (Claude, for the author's review)

- **"Target exceeded"** at τ\*: the 95% Wilson interval lies wholly above 90%. That is reported as
  "QRE under-predicts responsiveness; the mechanism overpays".
- **QRE's prediction band** at each level comes from the posterior over λ of the model's
  Stage 2A named-PD fit. The point prediction uses the posterior median (λ̂).
