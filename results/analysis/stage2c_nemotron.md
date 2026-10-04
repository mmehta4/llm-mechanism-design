# Stage 2C confirmatory analysis: nemotron

## Which answers count

| Model | Game | 2C answered | 2C counted | Normal pairs | Disguised pairs |
|---|---|---:|---:|---:|---:|
| nemotron | Vickrey auction | 138 | 138 | 138 | 138 |
| nemotron | Cournot | 138 | 138 | 138 | 138 |
| nemotron | Repeated PD | 138 | 138 | 137 | 137 |
| nemotron | Public goods | 138 | 138 | 136 | 138 |

## Main test: equilibrium play, normal (2A) vs extreme (2C)

### Fraction-slip corrected (registered)

| Model | Game | Pairs | Normal (2A) | Extreme (2C) | Normal − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| nemotron | Vickrey auction | 138 | 100% (138/138) | 99% (136/138) | +1 pts [-1, +4] | 0.5 | 1 |
| nemotron | Cournot | 138 | 98% (135/138) | 99% (137/138) | -1 pts [-5, +2] | 0.625 | 1 |
| nemotron | Repeated PD | 137 | 59% (81/137) | 93% (128/137) | -34 pts [-43, -25] | 6.4e-11 | 2.56e-10 |
| nemotron | Public goods | 136 | 100% (136/136) | 99% (135/136) | +1 pts [-1, +3] | 1 | 1 |

### Uncorrected (recorded verdicts), for comparison

| Model | Game | Pairs | Normal (2A) | Extreme (2C) | Normal − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| nemotron | Vickrey auction | 138 | 100% (138/138) | 49% (67/138) | +51 pts [+42, +59] | 8.47e-22 | 3.39e-21 |
| nemotron | Cournot | 138 | 90% (124/138) | 44% (61/138) | +46 pts [+37, +53] | 2.17e-19 | 6.51e-19 |
| nemotron | Repeated PD | 137 | 59% (81/137) | 93% (128/137) | -34 pts [-43, -25] | 6.4e-11 | 1.28e-10 |
| nemotron | Public goods | 136 | 100% (136/136) | 99% (135/136) | +1 pts [-1, +3] | 1 | 1 |

### Secondary: conversion slips counted as equilibrium play

| Model | Game | Pairs | Normal (2A) | Extreme (2C) | Normal − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| nemotron | Vickrey auction | 138 | 100% (138/138) | 99% (137/138) | +1 pts [-1, +3] | 1 | 1 |
| nemotron | Cournot | 138 | 98% (135/138) | 99% (137/138) | -1 pts [-5, +2] | 0.625 | 1 |
| nemotron | Repeated PD | 137 | 59% (81/137) | 93% (128/137) | -34 pts [-43, -25] | 6.4e-11 | 2.56e-10 |
| nemotron | Public goods | 136 | 100% (136/136) | 99% (135/136) | +1 pts [-1, +3] | 1 | 1 |

### Sensitivity (not registered): extreme answers judged with the Stage 2A tolerance after decoding (±0.5 on the offer, amount or contribution)

| Model | Game | Pairs | Normal (2A) | Extreme (2C) | Normal − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| nemotron | Vickrey auction | 138 | 100% (138/138) | 99% (136/138) | +1 pts [-1, +4] | 0.5 | 1 |
| nemotron | Cournot | 138 | 98% (135/138) | 99% (137/138) | -1 pts [-5, +2] | 0.625 | 1 |
| nemotron | Repeated PD | 137 | 59% (81/137) | 93% (128/137) | -34 pts [-43, -25] | 6.4e-11 | 2.56e-10 |
| nemotron | Public goods | 136 | 100% (136/136) | 99% (135/136) | +1 pts [-1, +3] | 1 | 1 |

## Secondary: disguised (2A) vs extreme (2C)

### Fraction-slip corrected

| Model | Game | Pairs | Disguised (2A) | Extreme (2C) | Disguised − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| nemotron | Vickrey auction | 138 | 100% (138/138) | 99% (136/138) | +1 pts [-1, +4] | 0.5 | 1 |
| nemotron | Cournot | 138 | 98% (135/138) | 99% (137/138) | -1 pts [-5, +2] | 0.625 | 1 |
| nemotron | Repeated PD | 137 | 59% (81/137) | 93% (128/137) | -34 pts [-43, -25] | 2.05e-11 | 8.19e-11 |
| nemotron | Public goods | 138 | 100% (138/138) | 99% (137/138) | +1 pts [-1, +3] | 1 | 1 |

## Recognition: did the model name the game? (`NAMES_GAME`)

| Model | Game | Pairs | Disguised (2A) | Extreme (2C) | McNemar p |
|---|---|---:|---:|---:|---:|
| nemotron | Vickrey auction | 138 | 100% (138/138) | 100% (138/138) | 1 |
| nemotron | Cournot | 138 | 96% (133/138) | 10% (14/138) | 3.01e-36 |
| nemotron | Repeated PD | 137 | 81% (111/137) | 65% (89/137) | 0.00815 |
| nemotron | Public goods | 138 | 54% (74/138) | 99% (136/138) | 6e-17 |

### Exploratory: equilibrium play within the extreme wording, named vs not named

| Model | Game | Named the game | Did not | Fisher p (exploratory) |
|---|---|---:|---:|---:|
| nemotron | Vickrey auction | 99% (136/138) | – | – |
| nemotron | Cournot | 100% (14/14) | 99% (123/124) | 1 |
| nemotron | Repeated PD | 90% (80/89) | 100% (49/49) | 0.0265 |
| nemotron | Public goods | 99% (135/136) | 100% (2/2) | 1 |

## Fraction slips corrected (counted answers)

| Model | Game | Normal (2A) | Disguised (2A) | Extreme (2C) |
|---|---|---:|---:|---:|
| nemotron | Vickrey auction | 0% (0/138) | 0% (0/138) | 50% (69/138) |
| nemotron | Cournot | 8% (11/138) | 10% (14/138) | 55% (76/138) |
| nemotron | Public goods | 0% (0/136) | 0% (0/138) | 0% (0/138) |

## Conversion slips (extreme only: right strategy, answer in the wrong unit)

| Model | Game | Counted 2C answers | Conversion slips | Missed answers that are conversion slips |
|---|---|---:|---:|---:|
| nemotron | Vickrey auction | 138 | 1% (1/138) | 50% (1/2) |
| nemotron | Cournot | 138 | 0% (0/138) | 0% (0/1) |

## λ on the Stage 2A scale (paired counted answers, slip-corrected)

| Model | Game | λ normal (2A) | λ extreme (2C, decoded) | Δλ = normal − extreme |
|---|---|---|---|---|
| nemotron | Vickrey auction | λ ≥ 944 (ceiling; n=138) | λ = 5.62 [4.47, 7.08] (n=138) | Δλ ≥ +937 (normal at the ceiling, so only a lower bound) |
| nemotron | Cournot | λ = 0.00818 [0.00631, 0.0103] (n=138) | λ = 0.0237 [0.0183, 0.0299] (n=138) | Δλ = -0.0154 [-0.0217, -0.00989], P(Δλ > 0) = 0.00 |
| nemotron | Repeated PD | λ = 0.154 [0.00158, 0.473] (n=137) | λ = 2.59 [1.94, 3.45] (n=137) | Δλ = -2.44 [-3.34, -1.68], P(Δλ > 0) = 0.00 |
| nemotron | Public goods | λ ≥ 21.8 (ceiling; n=136) | λ = 6.13 [5.01, 7.29] (n=136) | Δλ ≥ +14.5 (normal at the ceiling, so only a lower bound) |

## Predictions vs results (THIS MODEL ONLY; the registered check is the pooled report)

| Prediction | Result | Verdict |
|---|---|---|
| Vickrey auction: recognition ~90% (85–95) | 100% (138/138) | ❌ not met |
| Cournot: recognition ~25% (20–35) | 10% (14/138) | ❌ not met |
| Repeated PD: recognition ~55% (45–65) | 65% (89/137) | ✅ met |
| Public goods: recognition ~95% (90–100) | 99% (136/138) | ✅ met |
| Vickrey auction: play ~10 points lower than normal | +1 pts | ❌ not met |
| Cournot: play 35–45 points lower than normal | -1 pts | ❌ not met |
| Public goods: play within ±5 points of normal | +1 pts | ✅ met |
| Repeated PD: extreme play 80–90%, above normal, at or above disguised | 93%; normal − extreme -34 pts, disguised − extreme -34 pts | ❌ not met |
| Cournot drop, nemotron: ≥ 35 points | -1 pts | ❌ not met |

_Ranges are read inclusively. Conversion-slip share of each drop: see the conversion-slip table (predicted 5–15 points of the Cournot and Vickrey drops)._

