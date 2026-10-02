# How each result will be read, fixed in advance

Written by the author on 2026-10-03 (final workbook, Task 5), before the results it covers
existed: the other models' Stage 2A, Stage 2B, Stage 2C and Stage 5. The paper's conclusions follow these
rows. Any departure is reported as such.

## Definitions

- **"More":** a two-proportion test, p < 0.05.
- **"About 50%":** the 95% interval includes 50.
- **"Close":** within ±10 points.
- **Recognition:** `NAMES_GAME`; "high" means more than 50%.

## Stage 2A (each model)

| Pattern | Reading |
|---|---|
| No change between wordings, **and** the game is named in > 50% of disguised answers | inconclusive for that game: the disguise didn't hide it |
| Otherwise | as registered in pre-registration 1 |

## Stage 2B traps (pooled across models, per trap)

| Pattern | Reading |
|---|---|
| More textbook (wrong) answers in the named wording | recall |
| Textbook answer equally common in both wordings, **and** recognition low in the disguised wording | a reading or reasoning failure, not recall |
| Equally common, but the disguised wording is still recognised | inconclusive |
| Correct in both wordings | derivation |

## Stage 2C (each model and game, normal vs extreme)

| Pattern | Reading |
|---|---|
| Play drops, recognition drops, and the maths-check pass rate holds up in the extreme wording | recall |
| Play drops, recognition drops, but the maths-check pass rate falls | inconclusive: a comprehension cost, not recall |
| Play unchanged, recognition drops | consistent with derivation. Recognition is coded from what the model *writes*, so silent recognition can't be ruled out |
| Play unchanged, recognition still high | inconclusive: the disguise failed |
| Play drops, recognition still high, and conversion slips account for the drop | a conversion problem |
| Play drops, recognition still high, and slips do not account for the drop | inconclusive: recognised but misapplied |

## Stage 5 (each model)

| Pattern | Reading |
|---|---|
| About 50% at τ = 1.5, and close to QRE at the other levels | QRE describes the model |
| Well above 50% at τ = 1.5 | cooperation norm **or** repeated-game reasoning: round-1 cooperation is subgame-perfect at τ = 1.5 (Benoît & Krishna, 1985). The reasoning codes decide which: future rounds, reciprocity or "establishing cooperation" means repeated-game; fairness or "the right thing" means norm |
| Well below 50% at τ = 1.5, **and** below 50% at τ = 2.5 (where cooperating is dominant) | ignores the subsidy |
| Well below 50% at τ = 1.5, but cooperates at τ = 2.5 | a defection bias near indifference: rejects QRE, not a sign of recall |
| τ\* gives < 75% | the derived mechanism failed (registered failure criterion) |
| τ\* gives about 100% while τ = 2.5 is already ≥ 90% | the mechanism worked but overpaid: QRE under-predicts this model's responsiveness |
