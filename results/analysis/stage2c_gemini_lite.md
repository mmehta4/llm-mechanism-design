# Stage 2C confirmatory analysis: gemini_lite

## Which answers count

| Model | Game | 2C answered | 2C counted | Normal pairs | Disguised pairs |
|---|---|---:|---:|---:|---:|
| gemini_lite | Vickrey auction | 138 | 138 | 138 | 11 |
| gemini_lite | Cournot | 138 | 0 | 0 | 0 |
| gemini_lite | Repeated PD | 138 | 138 | 138 | 138 |
| gemini_lite | Public goods | 138 | 22 | 22 | 22 |

## Main test: equilibrium play, normal (2A) vs extreme (2C)

### Fraction-slip corrected (registered)

| Model | Game | Pairs | Normal (2A) | Extreme (2C) | Normal − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| gemini_lite | Vickrey auction | 138 | 100% (138/138) | 45% (62/138) | +55 pts [+46, +63] | 2.65e-23 | 5.29e-23 |
| gemini_lite | Cournot | 0 | – | – | – | – | – |
| gemini_lite | Repeated PD | 138 | 9% (12/138) | 85% (117/138) | -76 pts [-83, -67] | 1.29e-27 | 3.86e-27 |
| gemini_lite | Public goods | 22 | 100% (22/22) | 0% (0/22) | +100 pts [+78, +100] | 4.77e-07 | 4.77e-07 |

### Uncorrected (recorded verdicts), for comparison

| Model | Game | Pairs | Normal (2A) | Extreme (2C) | Normal − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| gemini_lite | Vickrey auction | 138 | 100% (138/138) | 45% (62/138) | +55 pts [+46, +63] | 2.65e-23 | 5.29e-23 |
| gemini_lite | Cournot | 0 | – | – | – | – | – |
| gemini_lite | Repeated PD | 138 | 9% (12/138) | 85% (117/138) | -76 pts [-83, -67] | 1.29e-27 | 3.86e-27 |
| gemini_lite | Public goods | 22 | 100% (22/22) | 0% (0/22) | +100 pts [+78, +100] | 4.77e-07 | 4.77e-07 |

### Secondary: conversion slips counted as equilibrium play

| Model | Game | Pairs | Normal (2A) | Extreme (2C) | Normal − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| gemini_lite | Vickrey auction | 138 | 100% (138/138) | 45% (62/138) | +55 pts [+46, +63] | 2.65e-23 | 5.29e-23 |
| gemini_lite | Cournot | 0 | – | – | – | – | – |
| gemini_lite | Repeated PD | 138 | 9% (12/138) | 85% (117/138) | -76 pts [-83, -67] | 1.29e-27 | 3.86e-27 |
| gemini_lite | Public goods | 22 | 100% (22/22) | 0% (0/22) | +100 pts [+78, +100] | 4.77e-07 | 4.77e-07 |

### Sensitivity (not registered): extreme answers judged with the Stage 2A tolerance after decoding (±0.5 on the offer, amount or contribution)

| Model | Game | Pairs | Normal (2A) | Extreme (2C) | Normal − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| gemini_lite | Vickrey auction | 138 | 100% (138/138) | 44% (61/138) | +56 pts [+47, +63] | 1.32e-23 | 2.65e-23 |
| gemini_lite | Cournot | 0 | – | – | – | – | – |
| gemini_lite | Repeated PD | 138 | 9% (12/138) | 85% (117/138) | -76 pts [-83, -67] | 1.29e-27 | 3.86e-27 |
| gemini_lite | Public goods | 22 | 100% (22/22) | 0% (0/22) | +100 pts [+78, +100] | 4.77e-07 | 4.77e-07 |

## Secondary: disguised (2A) vs extreme (2C)

### Fraction-slip corrected

| Model | Game | Pairs | Disguised (2A) | Extreme (2C) | Disguised − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| gemini_lite | Vickrey auction | 11 | 91% (10/11) | 27% (3/11) | +64 pts [+23, +85] | 0.0156 | 0.0303 |
| gemini_lite | Cournot | 0 | – | – | – | – | – |
| gemini_lite | Repeated PD | 138 | 70% (97/138) | 85% (117/138) | -14 pts [-25, -3] | 0.0151 | 0.0303 |
| gemini_lite | Public goods | 22 | 77% (17/22) | 0% (0/22) | +77 pts [+51, +91] | 1.53e-05 | 4.58e-05 |

## Recognition: did the model name the game? (`NAMES_GAME`)

| Model | Game | Pairs | Disguised (2A) | Extreme (2C) | McNemar p |
|---|---|---:|---:|---:|---:|
| gemini_lite | Vickrey auction | 11 | 73% (8/11) | 27% (3/11) | 0.0625 |
| gemini_lite | Cournot | 0 | – | – | – |
| gemini_lite | Repeated PD | 138 | 33% (46/138) | 0% (0/138) | 2.84e-14 |
| gemini_lite | Public goods | 22 | 50% (11/22) | 100% (22/22) | 0.000977 |

### Exploratory: equilibrium play within the extreme wording, named vs not named

| Model | Game | Named the game | Did not | Fisher p (exploratory) |
|---|---|---:|---:|---:|
| gemini_lite | Vickrey auction | 24% (6/25) | 50% (56/113) | 0.0258 |
| gemini_lite | Cournot | – | – | – |
| gemini_lite | Repeated PD | – | 85% (117/138) | – |
| gemini_lite | Public goods | 0% (0/22) | – | – |

## Fraction slips corrected (counted answers)

| Model | Game | Normal (2A) | Disguised (2A) | Extreme (2C) |
|---|---|---:|---:|---:|
| gemini_lite | Vickrey auction | 0% (0/138) | 0% (0/11) | 0% (0/138) |
| gemini_lite | Cournot | 0% (0/137) | 0% (0/138) | – |
| gemini_lite | Public goods | 0% (0/138) | 0% (0/138) | 0% (0/22) |

## Conversion slips (extreme only: right strategy, answer in the wrong unit)

| Model | Game | Counted 2C answers | Conversion slips | Missed answers that are conversion slips |
|---|---|---:|---:|---:|
| gemini_lite | Vickrey auction | 138 | 0% (0/138) | 0% (0/76) |
| gemini_lite | Cournot | 0 | – | – |

## λ on the Stage 2A scale (paired counted answers, slip-corrected)

| Model | Game | λ normal (2A) | λ extreme (2C, decoded) | Δλ = normal − extreme |
|---|---|---|---|---|
| gemini_lite | Vickrey auction | λ ≥ 944 (ceiling; n=138) | λ = 0.282 [0.211, 0.365] (n=138) | Δλ ≥ +944 (normal at the ceiling, so only a lower bound) |
| gemini_lite | Cournot | – | – | not enough answers |
| gemini_lite | Repeated PD | λ = 0.00316 [0.00103, 0.023] (n=138) | λ = 1.45 [1.03, 2] (n=138) | Δλ = -1.45 [-1.99, -1.02], P(Δλ > 0) = 0.00 |
| gemini_lite | Public goods | λ ≥ 13.3 (ceiling; n=22) | λ = 0.00282 [0.00103, 0.0183] (n=22) | Δλ ≥ +13.3 (normal at the ceiling, so only a lower bound) |

## Predictions vs results (THIS MODEL ONLY; the registered check is the pooled report)

| Prediction | Result | Verdict |
|---|---|---|
| Vickrey auction: recognition ~90% (85–95) | 27% (3/11) | ❌ not met |
| Cournot: recognition ~25% (20–35) | – | – |
| Repeated PD: recognition ~55% (45–65) | 0% (0/138) | ❌ not met |
| Public goods: recognition ~95% (90–100) | 100% (22/22) | ✅ met |
| Vickrey auction: play ~10 points lower than normal | +55 pts | ❌ not met |
| Cournot: play 35–45 points lower than normal | +nan pts | – |
| Public goods: play within ±5 points of normal | +100 pts | ❌ not met |
| Repeated PD: extreme play 80–90%, above normal, at or above disguised | 85%; normal − extreme -76 pts, disguised − extreme -14 pts | ✅ met |
| Cournot drop, gemini_lite: 20–35 points | +nan pts | – |

_Ranges are read inclusively. Conversion-slip share of each drop: see the conversion-slip table (predicted 5–15 points of the Cournot and Vickrey drops)._

