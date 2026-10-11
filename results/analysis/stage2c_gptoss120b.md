# Stage 2C confirmatory analysis: gptoss120b

## Which answers count

| Model | Game | 2C answered | 2C counted | Normal pairs | Disguised pairs |
|---|---|---:|---:|---:|---:|
| gptoss120b | Vickrey auction | 138 | 138 | 138 | 131 |
| gptoss120b | Cournot | 138 | 137 | 134 | 137 |
| gptoss120b | Repeated PD | 138 | 138 | 138 | 138 |
| gptoss120b | Public goods | 138 | 138 | 138 | 138 |

## Main test: equilibrium play, normal (2A) vs extreme (2C)

### Fraction-slip corrected (registered)

| Model | Game | Pairs | Normal (2A) | Extreme (2C) | Normal − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| gptoss120b | Vickrey auction | 138 | 100% (138/138) | 54% (74/138) | +46 pts [+37, +54] | 1.08e-19 | 3.25e-19 |
| gptoss120b | Cournot | 134 | 96% (129/134) | 30% (40/134) | +66 pts [+57, +74] | 8.83e-25 | 3.53e-24 |
| gptoss120b | Repeated PD | 138 | 69% (95/138) | 86% (119/138) | -17 pts [-28, -7] | 0.00223 | 0.00309 |
| gptoss120b | Public goods | 138 | 97% (134/138) | 86% (118/138) | +12 pts [+5, +18] | 0.00154 | 0.00309 |

### Uncorrected (recorded verdicts), for comparison

| Model | Game | Pairs | Normal (2A) | Extreme (2C) | Normal − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| gptoss120b | Vickrey auction | 138 | 100% (138/138) | 54% (74/138) | +46 pts [+37, +54] | 1.08e-19 | 3.25e-19 |
| gptoss120b | Cournot | 134 | 96% (129/134) | 30% (40/134) | +66 pts [+57, +74] | 8.83e-25 | 3.53e-24 |
| gptoss120b | Repeated PD | 138 | 69% (95/138) | 86% (119/138) | -17 pts [-28, -7] | 0.00223 | 0.00309 |
| gptoss120b | Public goods | 138 | 97% (134/138) | 86% (118/138) | +12 pts [+5, +18] | 0.00154 | 0.00309 |

### Secondary: conversion slips counted as equilibrium play

| Model | Game | Pairs | Normal (2A) | Extreme (2C) | Normal − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| gptoss120b | Vickrey auction | 138 | 100% (138/138) | 54% (74/138) | +46 pts [+37, +54] | 1.08e-19 | 3.25e-19 |
| gptoss120b | Cournot | 134 | 96% (129/134) | 30% (40/134) | +66 pts [+57, +74] | 8.83e-25 | 3.53e-24 |
| gptoss120b | Repeated PD | 138 | 69% (95/138) | 86% (119/138) | -17 pts [-28, -7] | 0.00223 | 0.00309 |
| gptoss120b | Public goods | 138 | 97% (134/138) | 86% (118/138) | +12 pts [+5, +18] | 0.00154 | 0.00309 |

### Sensitivity (not registered): extreme answers judged with the Stage 2A tolerance after decoding (±0.5 on the offer, amount or contribution)

| Model | Game | Pairs | Normal (2A) | Extreme (2C) | Normal − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| gptoss120b | Vickrey auction | 138 | 100% (138/138) | 53% (73/138) | +47 pts [+38, +55] | 5.42e-20 | 1.63e-19 |
| gptoss120b | Cournot | 134 | 96% (129/134) | 30% (40/134) | +66 pts [+57, +74] | 8.83e-25 | 3.53e-24 |
| gptoss120b | Repeated PD | 138 | 69% (95/138) | 86% (119/138) | -17 pts [-28, -7] | 0.00223 | 0.00309 |
| gptoss120b | Public goods | 138 | 97% (134/138) | 86% (118/138) | +12 pts [+5, +18] | 0.00154 | 0.00309 |

## Secondary: disguised (2A) vs extreme (2C)

### Fraction-slip corrected

| Model | Game | Pairs | Disguised (2A) | Extreme (2C) | Disguised − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| gptoss120b | Vickrey auction | 131 | 98% (129/131) | 53% (70/131) | +45 pts [+35, +53] | 4.37e-16 | 1.75e-15 |
| gptoss120b | Cournot | 137 | 80% (109/137) | 29% (40/137) | +50 pts [+39, +60] | 2.77e-15 | 8.3e-15 |
| gptoss120b | Repeated PD | 138 | 73% (101/138) | 86% (119/138) | -13 pts [-22, -4] | 0.00792 | 0.0158 |
| gptoss120b | Public goods | 138 | 93% (128/138) | 86% (118/138) | +7 pts [-1, +15] | 0.0987 | 0.0987 |

## Recognition: did the model name the game? (`NAMES_GAME`)

| Model | Game | Pairs | Disguised (2A) | Extreme (2C) | McNemar p |
|---|---|---:|---:|---:|---:|
| gptoss120b | Vickrey auction | 131 | 89% (116/131) | 10% (13/131) | 1.97e-31 |
| gptoss120b | Cournot | 137 | 9% (13/137) | 1% (2/137) | 0.00739 |
| gptoss120b | Repeated PD | 138 | 1% (2/138) | 2% (3/138) | 1 |
| gptoss120b | Public goods | 138 | 0% (0/138) | 0% (0/138) | 1 |

### Exploratory: equilibrium play within the extreme wording, named vs not named

| Model | Game | Named the game | Did not | Fisher p (exploratory) |
|---|---|---:|---:|---:|
| gptoss120b | Vickrey auction | 100% (14/14) | 48% (60/124) | 9.56e-05 |
| gptoss120b | Cournot | 100% (2/2) | 28% (38/135) | 0.0837 |
| gptoss120b | Repeated PD | 100% (3/3) | 86% (116/135) | 1 |
| gptoss120b | Public goods | – | 86% (118/138) | – |

## Fraction slips corrected (counted answers)

| Model | Game | Normal (2A) | Disguised (2A) | Extreme (2C) |
|---|---|---:|---:|---:|
| gptoss120b | Vickrey auction | 0% (0/138) | 0% (0/131) | 0% (0/138) |
| gptoss120b | Cournot | 0% (0/135) | 0% (0/138) | 0% (0/137) |
| gptoss120b | Public goods | 0% (0/138) | 0% (0/138) | 0% (0/138) |

## Conversion slips (extreme only: right strategy, answer in the wrong unit)

| Model | Game | Counted 2C answers | Conversion slips | Missed answers that are conversion slips |
|---|---|---:|---:|---:|
| gptoss120b | Vickrey auction | 138 | 0% (0/138) | 0% (0/64) |
| gptoss120b | Cournot | 137 | 0% (0/137) | 0% (0/97) |

## λ on the Stage 2A scale (paired counted answers, slip-corrected)

| Model | Game | λ normal (2A) | λ extreme (2C, decoded) | Δλ = normal − extreme |
|---|---|---|---|---|
| gptoss120b | Vickrey auction | λ ≥ 944 (ceiling; n=138) | λ = 0.0501 [0.0325, 0.0708] (n=138) | Δλ ≥ +944 (normal at the ceiling, so only a lower bound) |
| gptoss120b | Cournot | λ = 0.173 [0.133, 0.218] (n=134) | λ = 0.00168 [0.00119, 0.00224] (n=134) | Δλ = +0.171 [+0.132, +0.216], P(Δλ > 0) = 1.00 |
| gptoss120b | Repeated PD | λ = 0.579 [0.274, 0.917] (n=138) | λ = 1.58 [1.12, 2.11] (n=138) | Δλ = -1.02 [-1.64, -0.442], P(Δλ > 0) = 0.00 |
| gptoss120b | Public goods | λ = 3.76 [3.07, 4.34] (n=138) | λ = 0.631 [0.531, 0.75] (n=138) | Δλ = +3.09 [+2.47, +3.78], P(Δλ > 0) = 1.00 |

## Predictions vs results (THIS MODEL ONLY; the registered check is the pooled report)

| Prediction | Result | Verdict |
|---|---|---|
| Vickrey auction: recognition ~90% (85–95) | 10% (13/131) | ❌ not met |
| Cournot: recognition ~25% (20–35) | 1% (2/137) | ❌ not met |
| Repeated PD: recognition ~55% (45–65) | 2% (3/138) | ❌ not met |
| Public goods: recognition ~95% (90–100) | 0% (0/138) | ❌ not met |
| Vickrey auction: play ~10 points lower than normal | +46 pts | ❌ not met |
| Cournot: play 35–45 points lower than normal | +66 pts | ❌ not met |
| Public goods: play within ±5 points of normal | +12 pts | ❌ not met |
| Repeated PD: extreme play 80–90%, above normal, at or above disguised | 86%; normal − extreme -17 pts, disguised − extreme -13 pts | ✅ met |
| Cournot drop, gptoss120b: ≤ 15 points | +66 pts | ❌ not met |

_Ranges are read inclusively. Conversion-slip share of each drop: see the conversion-slip table (predicted 5–15 points of the Cournot and Vickrey drops)._

