# Stage 2C confirmatory analysis: kimi

## Which answers count

| Model | Game | 2C answered | 2C counted | Normal pairs | Disguised pairs |
|---|---|---:|---:|---:|---:|
| kimi | Vickrey auction | 138 | 137 | 137 | 137 |
| kimi | Cournot | 138 | 138 | 138 | 138 |
| kimi | Repeated PD | 138 | 138 | 138 | 138 |
| kimi | Public goods | 138 | 138 | 138 | 138 |

## Main test: equilibrium play, normal (2A) vs extreme (2C)

### Fraction-slip corrected (registered)

| Model | Game | Pairs | Normal (2A) | Extreme (2C) | Normal − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| kimi | Vickrey auction | 137 | 100% (137/137) | 99% (135/137) | +1 pts [-1, +4] | 0.5 | 1 |
| kimi | Cournot | 138 | 100% (138/138) | 100% (138/138) | +0 pts [-1, +1] | 1 | 1 |
| kimi | Repeated PD | 138 | 46% (63/138) | 70% (96/138) | -24 pts [-34, -13] | 6.74e-05 | 0.00027 |
| kimi | Public goods | 138 | 96% (132/138) | 96% (133/138) | -1 pts [-5, +4] | 1 | 1 |

### Uncorrected (recorded verdicts), for comparison

| Model | Game | Pairs | Normal (2A) | Extreme (2C) | Normal − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| kimi | Vickrey auction | 137 | 100% (137/137) | 99% (135/137) | +1 pts [-1, +4] | 0.5 | 1 |
| kimi | Cournot | 138 | 100% (138/138) | 100% (138/138) | +0 pts [-1, +1] | 1 | 1 |
| kimi | Repeated PD | 138 | 46% (63/138) | 70% (96/138) | -24 pts [-34, -13] | 6.74e-05 | 0.00027 |
| kimi | Public goods | 138 | 96% (132/138) | 96% (133/138) | -1 pts [-5, +4] | 1 | 1 |

### Secondary: conversion slips counted as equilibrium play

| Model | Game | Pairs | Normal (2A) | Extreme (2C) | Normal − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| kimi | Vickrey auction | 137 | 100% (137/137) | 99% (135/137) | +1 pts [-1, +4] | 0.5 | 1 |
| kimi | Cournot | 138 | 100% (138/138) | 100% (138/138) | +0 pts [-1, +1] | 1 | 1 |
| kimi | Repeated PD | 138 | 46% (63/138) | 70% (96/138) | -24 pts [-34, -13] | 6.74e-05 | 0.00027 |
| kimi | Public goods | 138 | 96% (132/138) | 96% (133/138) | -1 pts [-5, +4] | 1 | 1 |

### Sensitivity (not registered): extreme answers judged with the Stage 2A tolerance after decoding (±0.5 on the offer, amount or contribution)

| Model | Game | Pairs | Normal (2A) | Extreme (2C) | Normal − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| kimi | Vickrey auction | 137 | 100% (137/137) | 99% (135/137) | +1 pts [-1, +4] | 0.5 | 1 |
| kimi | Cournot | 138 | 100% (138/138) | 100% (138/138) | +0 pts [-1, +1] | 1 | 1 |
| kimi | Repeated PD | 138 | 46% (63/138) | 70% (96/138) | -24 pts [-34, -13] | 6.74e-05 | 0.00027 |
| kimi | Public goods | 138 | 96% (132/138) | 96% (133/138) | -1 pts [-5, +4] | 1 | 1 |

## Secondary: disguised (2A) vs extreme (2C)

### Fraction-slip corrected

| Model | Game | Pairs | Disguised (2A) | Extreme (2C) | Disguised − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| kimi | Vickrey auction | 137 | 100% (137/137) | 99% (135/137) | +1 pts [-1, +4] | 0.5 | 1 |
| kimi | Cournot | 138 | 100% (138/138) | 100% (138/138) | +0 pts [-1, +1] | 1 | 1 |
| kimi | Repeated PD | 138 | 57% (79/138) | 70% (96/138) | -12 pts [-23, -1] | 0.0464 | 0.185 |
| kimi | Public goods | 138 | 99% (136/138) | 96% (133/138) | +2 pts [-2, +6] | 0.453 | 1 |

## Recognition: did the model name the game? (`NAMES_GAME`)

| Model | Game | Pairs | Disguised (2A) | Extreme (2C) | McNemar p |
|---|---|---:|---:|---:|---:|
| kimi | Vickrey auction | 137 | 100% (137/137) | 93% (127/137) | 0.00195 |
| kimi | Cournot | 138 | 72% (99/138) | 20% (27/138) | 4.6e-16 |
| kimi | Repeated PD | 138 | 3% (4/138) | 1% (2/138) | 0.625 |
| kimi | Public goods | 138 | 11% (15/138) | 4% (5/138) | 0.0309 |

### Exploratory: equilibrium play within the extreme wording, named vs not named

| Model | Game | Named the game | Did not | Fisher p (exploratory) |
|---|---|---:|---:|---:|
| kimi | Vickrey auction | 100% (127/127) | 80% (8/10) | 0.00483 |
| kimi | Cournot | 100% (27/27) | 100% (111/111) | 1 |
| kimi | Repeated PD | 50% (1/2) | 70% (95/136) | 0.518 |
| kimi | Public goods | 60% (3/5) | 98% (130/133) | 0.0101 |

## Fraction slips corrected (counted answers)

| Model | Game | Normal (2A) | Disguised (2A) | Extreme (2C) |
|---|---|---:|---:|---:|
| kimi | Vickrey auction | 0% (0/138) | 0% (0/138) | 0% (0/137) |
| kimi | Cournot | 0% (0/138) | 0% (0/138) | 0% (0/138) |
| kimi | Public goods | 0% (0/138) | 0% (0/138) | 0% (0/138) |

## Conversion slips (extreme only: right strategy, answer in the wrong unit)

| Model | Game | Counted 2C answers | Conversion slips | Missed answers that are conversion slips |
|---|---|---:|---:|---:|
| kimi | Vickrey auction | 137 | 0% (0/137) | 0% (0/2) |
| kimi | Cournot | 138 | 0% (0/138) | – |

## λ on the Stage 2A scale (paired counted answers, slip-corrected)

| Model | Game | λ normal (2A) | λ extreme (2C, decoded) | Δλ = normal − extreme |
|---|---|---|---|---|
| kimi | Vickrey auction | λ ≥ 944 (ceiling; n=137) | λ = 47.3 [36.5, 59.6] (n=137) | Δλ ≥ +884 (normal at the ceiling, so only a lower bound) |
| kimi | Cournot | λ ≥ 299 (ceiling; n=138) | λ ≥ 631 (ceiling; n=138) | both wordings at the ceiling: no difference detectable in λ |
| kimi | Repeated PD | λ = 0.0075 [0.00109, 0.106] (n=138) | λ = 0.596 [0.299, 0.944] (n=138) | Δλ = -0.584 [-0.932, -0.275], P(Δλ > 0) = 0.00 |
| kimi | Public goods | λ = 2.51 [2.11, 2.9] (n=138) | λ = 2.74 [2.3, 3.25] (n=138) | Δλ = -0.247 [-0.887, +0.378], P(Δλ > 0) = 0.18 |

## Predictions vs results (THIS MODEL ONLY; the registered check is the pooled report)

| Prediction | Result | Verdict |
|---|---|---|
| Vickrey auction: recognition ~90% (85–95) | 93% (127/137) | ✅ met |
| Cournot: recognition ~25% (20–35) | 20% (27/138) | ❌ not met |
| Repeated PD: recognition ~55% (45–65) | 1% (2/138) | ❌ not met |
| Public goods: recognition ~95% (90–100) | 4% (5/138) | ❌ not met |
| Vickrey auction: play ~10 points lower than normal | +1 pts | ❌ not met |
| Cournot: play 35–45 points lower than normal | +0 pts | ❌ not met |
| Public goods: play within ±5 points of normal | -1 pts | ✅ met |
| Repeated PD: extreme play 80–90%, above normal, at or above disguised | 70%; normal − extreme -24 pts, disguised − extreme -12 pts | ❌ not met |
| Cournot drop, kimi: ≤ 15 points | +0 pts | ✅ met |

_Ranges are read inclusively. Conversion-slip share of each drop: see the conversion-slip table (predicted 5–15 points of the Cournot and Vickrey drops)._

