# PIPELINE CHECK ONLY: made-up Stage 2C answers built from Nemotron's Stage 2A normal answers (no real Stage 2C data)

## Which answers count

| Model | Game | 2C answered | 2C counted | Normal pairs | Disguised pairs |
|---|---|---:|---:|---:|---:|
| nemotron (synthetic 2C) | Vickrey auction | 138 | 138 | 138 | 138 |
| nemotron (synthetic 2C) | Cournot | 138 | 138 | 138 | 138 |
| nemotron (synthetic 2C) | Repeated PD | 138 | 137 | 137 | 136 |
| nemotron (synthetic 2C) | Public goods | 138 | 136 | 136 | 136 |

## Main test: equilibrium play, normal (2A) vs extreme (2C)

### Fraction-slip corrected (registered)

| Model | Game | Pairs | Normal (2A) | Extreme (2C) | Normal − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| nemotron (synthetic 2C) | Vickrey auction | 138 | 100% (138/138) | 100% (138/138) | +0 pts [-1, +1] | 1 | 1 |
| nemotron (synthetic 2C) | Cournot | 138 | 98% (135/138) | 98% (135/138) | +0 pts [-1, +1] | 1 | 1 |
| nemotron (synthetic 2C) | Repeated PD | 137 | 59% (81/137) | 59% (81/137) | +0 pts [-1, +1] | 1 | 1 |
| nemotron (synthetic 2C) | Public goods | 136 | 100% (136/136) | 100% (136/136) | +0 pts [-1, +1] | 1 | 1 |

### Uncorrected (recorded verdicts), for comparison

| Model | Game | Pairs | Normal (2A) | Extreme (2C) | Normal − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| nemotron (synthetic 2C) | Vickrey auction | 138 | 100% (138/138) | 100% (138/138) | +0 pts [-1, +1] | 1 | 1 |
| nemotron (synthetic 2C) | Cournot | 138 | 90% (124/138) | 98% (135/138) | -8 pts [-13, -3] | 0.000977 | 0.00391 |
| nemotron (synthetic 2C) | Repeated PD | 137 | 59% (81/137) | 59% (81/137) | +0 pts [-1, +1] | 1 | 1 |
| nemotron (synthetic 2C) | Public goods | 136 | 100% (136/136) | 100% (136/136) | +0 pts [-1, +1] | 1 | 1 |

### Secondary: conversion slips counted as equilibrium play

| Model | Game | Pairs | Normal (2A) | Extreme (2C) | Normal − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| nemotron (synthetic 2C) | Vickrey auction | 138 | 100% (138/138) | 100% (138/138) | +0 pts [-1, +1] | 1 | 1 |
| nemotron (synthetic 2C) | Cournot | 138 | 98% (135/138) | 98% (135/138) | +0 pts [-1, +1] | 1 | 1 |
| nemotron (synthetic 2C) | Repeated PD | 137 | 59% (81/137) | 59% (81/137) | +0 pts [-1, +1] | 1 | 1 |
| nemotron (synthetic 2C) | Public goods | 136 | 100% (136/136) | 100% (136/136) | +0 pts [-1, +1] | 1 | 1 |

### Sensitivity (not registered): extreme answers judged with the Stage 2A tolerance after decoding (±0.5 on the offer, amount or contribution)

| Model | Game | Pairs | Normal (2A) | Extreme (2C) | Normal − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| nemotron (synthetic 2C) | Vickrey auction | 138 | 100% (138/138) | 100% (138/138) | +0 pts [-1, +1] | 1 | 1 |
| nemotron (synthetic 2C) | Cournot | 138 | 98% (135/138) | 98% (135/138) | +0 pts [-1, +1] | 1 | 1 |
| nemotron (synthetic 2C) | Repeated PD | 137 | 59% (81/137) | 59% (81/137) | +0 pts [-1, +1] | 1 | 1 |
| nemotron (synthetic 2C) | Public goods | 136 | 100% (136/136) | 100% (136/136) | +0 pts [-1, +1] | 1 | 1 |

## Secondary: disguised (2A) vs extreme (2C)

### Fraction-slip corrected

| Model | Game | Pairs | Disguised (2A) | Extreme (2C) | Disguised − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| nemotron (synthetic 2C) | Vickrey auction | 138 | 100% (138/138) | 100% (138/138) | +0 pts [-1, +1] | 1 | 1 |
| nemotron (synthetic 2C) | Cournot | 138 | 98% (135/138) | 98% (135/138) | +0 pts [-4, +4] | 1 | 1 |
| nemotron (synthetic 2C) | Repeated PD | 136 | 59% (80/136) | 60% (81/136) | -1 pts [-12, +11] | 1 | 1 |
| nemotron (synthetic 2C) | Public goods | 136 | 100% (136/136) | 100% (136/136) | +0 pts [-1, +1] | 1 | 1 |

## Recognition: did the model name the game? (`NAMES_GAME`)

| Model | Game | Pairs | Disguised (2A) | Extreme (2C) | McNemar p |
|---|---|---:|---:|---:|---:|
| nemotron (synthetic 2C) | Vickrey auction | 138 | 100% (138/138) | 0% (0/138) | 5.74e-42 |
| nemotron (synthetic 2C) | Cournot | 138 | 96% (133/138) | 0% (0/138) | 1.84e-40 |
| nemotron (synthetic 2C) | Repeated PD | 136 | 81% (110/136) | 87% (118/136) | 0.243 |
| nemotron (synthetic 2C) | Public goods | 136 | 53% (72/136) | 0% (0/136) | 4.24e-22 |

### Exploratory: equilibrium play within the extreme wording, named vs not named

| Model | Game | Named the game | Did not | Fisher p (exploratory) |
|---|---|---:|---:|---:|
| nemotron (synthetic 2C) | Vickrey auction | – | 100% (138/138) | – |
| nemotron (synthetic 2C) | Cournot | – | 98% (135/138) | – |
| nemotron (synthetic 2C) | Repeated PD | 68% (81/119) | 0% (0/18) | 1.51e-08 |
| nemotron (synthetic 2C) | Public goods | – | 100% (136/136) | – |

## Fraction slips corrected (counted answers)

| Model | Game | Normal (2A) | Disguised (2A) | Extreme (2C) |
|---|---|---:|---:|---:|
| nemotron (synthetic 2C) | Vickrey auction | 0% (0/138) | 0% (0/138) | 0% (0/138) |
| nemotron (synthetic 2C) | Cournot | 8% (11/138) | 10% (14/138) | 0% (0/138) |
| nemotron (synthetic 2C) | Public goods | 0% (0/136) | 0% (0/138) | 0% (0/136) |

## Conversion slips (extreme only: right strategy, answer in the wrong unit)

| Model | Game | Counted 2C answers | Conversion slips | Missed answers that are conversion slips |
|---|---|---:|---:|---:|
| nemotron (synthetic 2C) | Vickrey auction | 138 | 0% (0/138) | – |
| nemotron (synthetic 2C) | Cournot | 138 | 0% (0/138) | 0% (0/3) |

## λ on the Stage 2A scale (paired counted answers, slip-corrected)

| Model | Game | λ normal (2A) | λ extreme (2C, decoded) | Δλ = normal − extreme |
|---|---|---|---|---|
| nemotron (synthetic 2C) | Vickrey auction | λ ≥ 944 (ceiling; n=138) | λ ≥ 944 (ceiling; n=138) | both wordings at the ceiling: no difference detectable in λ |
| nemotron (synthetic 2C) | Cournot | λ = 0.00818 [0.00631, 0.0103] (n=138) | λ = 0.00818 [0.00631, 0.0103] (n=138) | Δλ = +0 [-0.00276, +0.00276], P(Δλ > 0) = 0.47 |
| nemotron (synthetic 2C) | Repeated PD | λ = 0.154 [0.00158, 0.473] (n=137) | λ = 0.154 [0.00158, 0.473] (n=137) | Δλ = +0 [-0.377, +0.377], P(Δλ > 0) = 0.50 |
| nemotron (synthetic 2C) | Public goods | λ ≥ 21.8 (ceiling; n=136) | λ ≥ 21.8 (ceiling; n=136) | both wordings at the ceiling: no difference detectable in λ |

## Predictions vs results (THIS MODEL ONLY; the registered check is the pooled report)

| Prediction | Result | Verdict |
|---|---|---|
| Vickrey auction: recognition ~90% (85–95) | 0% (0/138) | ❌ not met |
| Cournot: recognition ~25% (20–35) | 0% (0/138) | ❌ not met |
| Repeated PD: recognition ~55% (45–65) | 87% (118/136) | ❌ not met |
| Public goods: recognition ~95% (90–100) | 0% (0/136) | ❌ not met |
| Vickrey auction: play ~10 points lower than normal | +0 pts | ❌ not met |
| Cournot: play 35–45 points lower than normal | +0 pts | ❌ not met |
| Public goods: play within ±5 points of normal | +0 pts | ✅ met |
| Repeated PD: extreme play 80–90%, above normal, at or above disguised | 59%; normal − extreme +0 pts, disguised − extreme -1 pts | ❌ not met |

_Ranges are read inclusively. Conversion-slip share of each drop: see the conversion-slip table (predicted 5–15 points of the Cournot and Vickrey drops)._

