# Stage 2C confirmatory analysis: all models

## Which answers count

| Model | Game | 2C answered | 2C counted | Normal pairs | Disguised pairs |
|---|---|---:|---:|---:|---:|
| gptoss120b | Vickrey auction | 138 | 138 | 138 | 131 |
| gptoss120b | Cournot | 138 | 137 | 134 | 137 |
| gptoss120b | Repeated PD | 138 | 138 | 138 | 138 |
| gptoss120b | Public goods | 138 | 138 | 138 | 138 |
| nemotron | Vickrey auction | 138 | 138 | 138 | 138 |
| nemotron | Cournot | 138 | 138 | 138 | 138 |
| nemotron | Repeated PD | 138 | 138 | 137 | 137 |
| nemotron | Public goods | 138 | 138 | 136 | 138 |
| kimi | Vickrey auction | 138 | 137 | 137 | 137 |
| kimi | Cournot | 138 | 138 | 138 | 138 |
| kimi | Repeated PD | 138 | 138 | 138 | 138 |
| kimi | Public goods | 138 | 138 | 138 | 138 |
| gemini_lite | Vickrey auction | 138 | 138 | 138 | 11 |
| gemini_lite | Cournot | 138 | 0 | 0 | 0 |
| gemini_lite | Repeated PD | 138 | 138 | 138 | 138 |
| gemini_lite | Public goods | 138 | 22 | 22 | 22 |

## Main test: equilibrium play, normal (2A) vs extreme (2C)

### Fraction-slip corrected (registered)

| Model | Game | Pairs | Normal (2A) | Extreme (2C) | Normal − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| gptoss120b | Vickrey auction | 138 | 100% (138/138) | 54% (74/138) | +46 pts [+37, +54] | 1.08e-19 | 3.25e-19 |
| gptoss120b | Cournot | 134 | 96% (129/134) | 30% (40/134) | +66 pts [+57, +74] | 8.83e-25 | 3.53e-24 |
| gptoss120b | Repeated PD | 138 | 69% (95/138) | 86% (119/138) | -17 pts [-28, -7] | 0.00223 | 0.00309 |
| gptoss120b | Public goods | 138 | 97% (134/138) | 86% (118/138) | +12 pts [+5, +18] | 0.00154 | 0.00309 |
| nemotron | Vickrey auction | 138 | 100% (138/138) | 99% (136/138) | +1 pts [-1, +4] | 0.5 | 1 |
| nemotron | Cournot | 138 | 98% (135/138) | 99% (137/138) | -1 pts [-5, +2] | 0.625 | 1 |
| nemotron | Repeated PD | 137 | 59% (81/137) | 93% (128/137) | -34 pts [-43, -25] | 6.4e-11 | 2.56e-10 |
| nemotron | Public goods | 136 | 100% (136/136) | 99% (135/136) | +1 pts [-1, +3] | 1 | 1 |
| kimi | Vickrey auction | 137 | 100% (137/137) | 99% (135/137) | +1 pts [-1, +4] | 0.5 | 1 |
| kimi | Cournot | 138 | 100% (138/138) | 100% (138/138) | +0 pts [-1, +1] | 1 | 1 |
| kimi | Repeated PD | 138 | 46% (63/138) | 70% (96/138) | -24 pts [-34, -13] | 6.74e-05 | 0.00027 |
| kimi | Public goods | 138 | 96% (132/138) | 96% (133/138) | -1 pts [-5, +4] | 1 | 1 |
| gemini_lite | Vickrey auction | 138 | 100% (138/138) | 45% (62/138) | +55 pts [+46, +63] | 2.65e-23 | 5.29e-23 |
| gemini_lite | Cournot | 0 | – | – | – | – | – |
| gemini_lite | Repeated PD | 138 | 9% (12/138) | 85% (117/138) | -76 pts [-83, -67] | 1.29e-27 | 3.86e-27 |
| gemini_lite | Public goods | 22 | 100% (22/22) | 0% (0/22) | +100 pts [+78, +100] | 4.77e-07 | 4.77e-07 |
| **all models** | Vickrey auction | 551 | 100% (551/551) | 74% (407/551) | +26 pts [+22, +30] | 8.97e-44 | 3.59e-43 |
| **all models** | Cournot | 410 | 98% (402/410) | 77% (315/410) | +21 pts [+17, +25] | 8.59e-22 | 1.72e-21 |
| **all models** | Repeated PD | 551 | 46% (251/551) | 83% (460/551) | -38 pts [-43, -33] | 3.99e-37 | 1.2e-36 |
| **all models** | Public goods | 434 | 98% (424/434) | 89% (386/434) | +9 pts [+5, +12] | 2.57e-07 | 2.57e-07 |

### Uncorrected (recorded verdicts), for comparison

| Model | Game | Pairs | Normal (2A) | Extreme (2C) | Normal − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| gptoss120b | Vickrey auction | 138 | 100% (138/138) | 54% (74/138) | +46 pts [+37, +54] | 1.08e-19 | 3.25e-19 |
| gptoss120b | Cournot | 134 | 96% (129/134) | 30% (40/134) | +66 pts [+57, +74] | 8.83e-25 | 3.53e-24 |
| gptoss120b | Repeated PD | 138 | 69% (95/138) | 86% (119/138) | -17 pts [-28, -7] | 0.00223 | 0.00309 |
| gptoss120b | Public goods | 138 | 97% (134/138) | 86% (118/138) | +12 pts [+5, +18] | 0.00154 | 0.00309 |
| nemotron | Vickrey auction | 138 | 100% (138/138) | 49% (67/138) | +51 pts [+42, +59] | 8.47e-22 | 3.39e-21 |
| nemotron | Cournot | 138 | 90% (124/138) | 44% (61/138) | +46 pts [+37, +53] | 2.17e-19 | 6.51e-19 |
| nemotron | Repeated PD | 137 | 59% (81/137) | 93% (128/137) | -34 pts [-43, -25] | 6.4e-11 | 1.28e-10 |
| nemotron | Public goods | 136 | 100% (136/136) | 99% (135/136) | +1 pts [-1, +3] | 1 | 1 |
| kimi | Vickrey auction | 137 | 100% (137/137) | 99% (135/137) | +1 pts [-1, +4] | 0.5 | 1 |
| kimi | Cournot | 138 | 100% (138/138) | 100% (138/138) | +0 pts [-1, +1] | 1 | 1 |
| kimi | Repeated PD | 138 | 46% (63/138) | 70% (96/138) | -24 pts [-34, -13] | 6.74e-05 | 0.00027 |
| kimi | Public goods | 138 | 96% (132/138) | 96% (133/138) | -1 pts [-5, +4] | 1 | 1 |
| gemini_lite | Vickrey auction | 138 | 100% (138/138) | 45% (62/138) | +55 pts [+46, +63] | 2.65e-23 | 5.29e-23 |
| gemini_lite | Cournot | 0 | – | – | – | – | – |
| gemini_lite | Repeated PD | 138 | 9% (12/138) | 85% (117/138) | -76 pts [-83, -67] | 1.29e-27 | 3.86e-27 |
| gemini_lite | Public goods | 22 | 100% (22/22) | 0% (0/22) | +100 pts [+78, +100] | 4.77e-07 | 4.77e-07 |
| **all models** | Vickrey auction | 551 | 100% (551/551) | 61% (338/551) | +39 pts [+34, +43] | 1.52e-64 | 6.08e-64 |
| **all models** | Cournot | 410 | 95% (391/410) | 58% (239/410) | +37 pts [+32, +42] | 2.68e-43 | 8.04e-43 |
| **all models** | Repeated PD | 551 | 46% (251/551) | 83% (460/551) | -38 pts [-43, -33] | 3.99e-37 | 7.97e-37 |
| **all models** | Public goods | 434 | 98% (424/434) | 89% (386/434) | +9 pts [+5, +12] | 2.57e-07 | 2.57e-07 |

### Secondary: conversion slips counted as equilibrium play

| Model | Game | Pairs | Normal (2A) | Extreme (2C) | Normal − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| gptoss120b | Vickrey auction | 138 | 100% (138/138) | 54% (74/138) | +46 pts [+37, +54] | 1.08e-19 | 3.25e-19 |
| gptoss120b | Cournot | 134 | 96% (129/134) | 30% (40/134) | +66 pts [+57, +74] | 8.83e-25 | 3.53e-24 |
| gptoss120b | Repeated PD | 138 | 69% (95/138) | 86% (119/138) | -17 pts [-28, -7] | 0.00223 | 0.00309 |
| gptoss120b | Public goods | 138 | 97% (134/138) | 86% (118/138) | +12 pts [+5, +18] | 0.00154 | 0.00309 |
| nemotron | Vickrey auction | 138 | 100% (138/138) | 99% (137/138) | +1 pts [-1, +3] | 1 | 1 |
| nemotron | Cournot | 138 | 98% (135/138) | 99% (137/138) | -1 pts [-5, +2] | 0.625 | 1 |
| nemotron | Repeated PD | 137 | 59% (81/137) | 93% (128/137) | -34 pts [-43, -25] | 6.4e-11 | 2.56e-10 |
| nemotron | Public goods | 136 | 100% (136/136) | 99% (135/136) | +1 pts [-1, +3] | 1 | 1 |
| kimi | Vickrey auction | 137 | 100% (137/137) | 99% (135/137) | +1 pts [-1, +4] | 0.5 | 1 |
| kimi | Cournot | 138 | 100% (138/138) | 100% (138/138) | +0 pts [-1, +1] | 1 | 1 |
| kimi | Repeated PD | 138 | 46% (63/138) | 70% (96/138) | -24 pts [-34, -13] | 6.74e-05 | 0.00027 |
| kimi | Public goods | 138 | 96% (132/138) | 96% (133/138) | -1 pts [-5, +4] | 1 | 1 |
| gemini_lite | Vickrey auction | 138 | 100% (138/138) | 45% (62/138) | +55 pts [+46, +63] | 2.65e-23 | 5.29e-23 |
| gemini_lite | Cournot | 0 | – | – | – | – | – |
| gemini_lite | Repeated PD | 138 | 9% (12/138) | 85% (117/138) | -76 pts [-83, -67] | 1.29e-27 | 3.86e-27 |
| gemini_lite | Public goods | 22 | 100% (22/22) | 0% (0/22) | +100 pts [+78, +100] | 4.77e-07 | 4.77e-07 |
| **all models** | Vickrey auction | 551 | 100% (551/551) | 74% (408/551) | +26 pts [+22, +30] | 1.79e-43 | 7.17e-43 |
| **all models** | Cournot | 410 | 98% (402/410) | 77% (315/410) | +21 pts [+17, +25] | 8.59e-22 | 1.72e-21 |
| **all models** | Repeated PD | 551 | 46% (251/551) | 83% (460/551) | -38 pts [-43, -33] | 3.99e-37 | 1.2e-36 |
| **all models** | Public goods | 434 | 98% (424/434) | 89% (386/434) | +9 pts [+5, +12] | 2.57e-07 | 2.57e-07 |

### Sensitivity (not registered): extreme answers judged with the Stage 2A tolerance after decoding (±0.5 on the offer, amount or contribution)

| Model | Game | Pairs | Normal (2A) | Extreme (2C) | Normal − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| gptoss120b | Vickrey auction | 138 | 100% (138/138) | 53% (73/138) | +47 pts [+38, +55] | 5.42e-20 | 1.63e-19 |
| gptoss120b | Cournot | 134 | 96% (129/134) | 30% (40/134) | +66 pts [+57, +74] | 8.83e-25 | 3.53e-24 |
| gptoss120b | Repeated PD | 138 | 69% (95/138) | 86% (119/138) | -17 pts [-28, -7] | 0.00223 | 0.00309 |
| gptoss120b | Public goods | 138 | 97% (134/138) | 86% (118/138) | +12 pts [+5, +18] | 0.00154 | 0.00309 |
| nemotron | Vickrey auction | 138 | 100% (138/138) | 99% (136/138) | +1 pts [-1, +4] | 0.5 | 1 |
| nemotron | Cournot | 138 | 98% (135/138) | 99% (137/138) | -1 pts [-5, +2] | 0.625 | 1 |
| nemotron | Repeated PD | 137 | 59% (81/137) | 93% (128/137) | -34 pts [-43, -25] | 6.4e-11 | 2.56e-10 |
| nemotron | Public goods | 136 | 100% (136/136) | 99% (135/136) | +1 pts [-1, +3] | 1 | 1 |
| kimi | Vickrey auction | 137 | 100% (137/137) | 99% (135/137) | +1 pts [-1, +4] | 0.5 | 1 |
| kimi | Cournot | 138 | 100% (138/138) | 100% (138/138) | +0 pts [-1, +1] | 1 | 1 |
| kimi | Repeated PD | 138 | 46% (63/138) | 70% (96/138) | -24 pts [-34, -13] | 6.74e-05 | 0.00027 |
| kimi | Public goods | 138 | 96% (132/138) | 96% (133/138) | -1 pts [-5, +4] | 1 | 1 |
| gemini_lite | Vickrey auction | 138 | 100% (138/138) | 44% (61/138) | +56 pts [+47, +63] | 1.32e-23 | 2.65e-23 |
| gemini_lite | Cournot | 0 | – | – | – | – | – |
| gemini_lite | Repeated PD | 138 | 9% (12/138) | 85% (117/138) | -76 pts [-83, -67] | 1.29e-27 | 3.86e-27 |
| gemini_lite | Public goods | 22 | 100% (22/22) | 0% (0/22) | +100 pts [+78, +100] | 4.77e-07 | 4.77e-07 |
| **all models** | Vickrey auction | 551 | 100% (551/551) | 74% (405/551) | +26 pts [+23, +30] | 2.24e-44 | 8.97e-44 |
| **all models** | Cournot | 410 | 98% (402/410) | 77% (315/410) | +21 pts [+17, +25] | 8.59e-22 | 1.72e-21 |
| **all models** | Repeated PD | 551 | 46% (251/551) | 83% (460/551) | -38 pts [-43, -33] | 3.99e-37 | 1.2e-36 |
| **all models** | Public goods | 434 | 98% (424/434) | 89% (386/434) | +9 pts [+5, +12] | 2.57e-07 | 2.57e-07 |

## Secondary: disguised (2A) vs extreme (2C)

### Fraction-slip corrected

| Model | Game | Pairs | Disguised (2A) | Extreme (2C) | Disguised − extreme [95% CI] | McNemar p | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|
| gptoss120b | Vickrey auction | 131 | 98% (129/131) | 53% (70/131) | +45 pts [+35, +53] | 4.37e-16 | 1.75e-15 |
| gptoss120b | Cournot | 137 | 80% (109/137) | 29% (40/137) | +50 pts [+39, +60] | 2.77e-15 | 8.3e-15 |
| gptoss120b | Repeated PD | 138 | 73% (101/138) | 86% (119/138) | -13 pts [-22, -4] | 0.00792 | 0.0158 |
| gptoss120b | Public goods | 138 | 93% (128/138) | 86% (118/138) | +7 pts [-1, +15] | 0.0987 | 0.0987 |
| nemotron | Vickrey auction | 138 | 100% (138/138) | 99% (136/138) | +1 pts [-1, +4] | 0.5 | 1 |
| nemotron | Cournot | 138 | 98% (135/138) | 99% (137/138) | -1 pts [-5, +2] | 0.625 | 1 |
| nemotron | Repeated PD | 137 | 59% (81/137) | 93% (128/137) | -34 pts [-43, -25] | 2.05e-11 | 8.19e-11 |
| nemotron | Public goods | 138 | 100% (138/138) | 99% (137/138) | +1 pts [-1, +3] | 1 | 1 |
| kimi | Vickrey auction | 137 | 100% (137/137) | 99% (135/137) | +1 pts [-1, +4] | 0.5 | 1 |
| kimi | Cournot | 138 | 100% (138/138) | 100% (138/138) | +0 pts [-1, +1] | 1 | 1 |
| kimi | Repeated PD | 138 | 57% (79/138) | 70% (96/138) | -12 pts [-23, -1] | 0.0464 | 0.185 |
| kimi | Public goods | 138 | 99% (136/138) | 96% (133/138) | +2 pts [-2, +6] | 0.453 | 1 |
| gemini_lite | Vickrey auction | 11 | 91% (10/11) | 27% (3/11) | +64 pts [+23, +85] | 0.0156 | 0.0303 |
| gemini_lite | Cournot | 0 | – | – | – | – | – |
| gemini_lite | Repeated PD | 138 | 70% (97/138) | 85% (117/138) | -14 pts [-25, -3] | 0.0151 | 0.0303 |
| gemini_lite | Public goods | 22 | 77% (17/22) | 0% (0/22) | +77 pts [+51, +91] | 1.53e-05 | 4.58e-05 |
| **all models** | Vickrey auction | 417 | 99% (414/417) | 82% (344/417) | +17 pts [+13, +20] | 2.94e-19 | 1.18e-18 |
| **all models** | Cournot | 413 | 92% (382/413) | 76% (315/413) | +16 pts [+12, +20] | 1.37e-13 | 4.1e-13 |
| **all models** | Repeated PD | 551 | 65% (358/551) | 83% (460/551) | -19 pts [-24, -13] | 6.45e-12 | 1.29e-11 |
| **all models** | Public goods | 436 | 96% (419/436) | 89% (388/436) | +7 pts [+4, +10] | 3.31e-05 | 3.31e-05 |

## Recognition: did the model name the game? (`NAMES_GAME`)

| Model | Game | Pairs | Disguised (2A) | Extreme (2C) | McNemar p |
|---|---|---:|---:|---:|---:|
| gptoss120b | Vickrey auction | 131 | 89% (116/131) | 10% (13/131) | 1.97e-31 |
| gptoss120b | Cournot | 137 | 9% (13/137) | 1% (2/137) | 0.00739 |
| gptoss120b | Repeated PD | 138 | 1% (2/138) | 2% (3/138) | 1 |
| gptoss120b | Public goods | 138 | 0% (0/138) | 0% (0/138) | 1 |
| nemotron | Vickrey auction | 138 | 100% (138/138) | 100% (138/138) | 1 |
| nemotron | Cournot | 138 | 96% (133/138) | 10% (14/138) | 3.01e-36 |
| nemotron | Repeated PD | 137 | 81% (111/137) | 65% (89/137) | 0.00815 |
| nemotron | Public goods | 138 | 54% (74/138) | 99% (136/138) | 6e-17 |
| kimi | Vickrey auction | 137 | 100% (137/137) | 93% (127/137) | 0.00195 |
| kimi | Cournot | 138 | 72% (99/138) | 20% (27/138) | 4.6e-16 |
| kimi | Repeated PD | 138 | 3% (4/138) | 1% (2/138) | 0.625 |
| kimi | Public goods | 138 | 11% (15/138) | 4% (5/138) | 0.0309 |
| gemini_lite | Vickrey auction | 11 | 73% (8/11) | 27% (3/11) | 0.0625 |
| gemini_lite | Cournot | 0 | – | – | – |
| gemini_lite | Repeated PD | 138 | 33% (46/138) | 0% (0/138) | 2.84e-14 |
| gemini_lite | Public goods | 22 | 50% (11/22) | 100% (22/22) | 0.000977 |
| **all models** | Vickrey auction | 417 | 96% (399/417) | 67% (281/417) | 6.02e-36 |
| **all models** | Cournot | 413 | 59% (245/413) | 10% (43/413) | 2.03e-50 |
| **all models** | Repeated PD | 551 | 30% (163/551) | 17% (94/551) | 1.34e-10 |
| **all models** | Public goods | 436 | 23% (100/436) | 37% (163/436) | 3.47e-11 |

### Exploratory: equilibrium play within the extreme wording, named vs not named

| Model | Game | Named the game | Did not | Fisher p (exploratory) |
|---|---|---:|---:|---:|
| gptoss120b | Vickrey auction | 100% (14/14) | 48% (60/124) | 9.56e-05 |
| gptoss120b | Cournot | 100% (2/2) | 28% (38/135) | 0.0837 |
| gptoss120b | Repeated PD | 100% (3/3) | 86% (116/135) | 1 |
| gptoss120b | Public goods | – | 86% (118/138) | – |
| nemotron | Vickrey auction | 99% (136/138) | – | – |
| nemotron | Cournot | 100% (14/14) | 99% (123/124) | 1 |
| nemotron | Repeated PD | 90% (80/89) | 100% (49/49) | 0.0265 |
| nemotron | Public goods | 99% (135/136) | 100% (2/2) | 1 |
| kimi | Vickrey auction | 100% (127/127) | 80% (8/10) | 0.00483 |
| kimi | Cournot | 100% (27/27) | 100% (111/111) | 1 |
| kimi | Repeated PD | 50% (1/2) | 70% (95/136) | 0.518 |
| kimi | Public goods | 60% (3/5) | 98% (130/133) | 0.0101 |
| gemini_lite | Vickrey auction | 24% (6/25) | 50% (56/113) | 0.0258 |
| gemini_lite | Cournot | – | – | – |
| gemini_lite | Repeated PD | – | 85% (117/138) | – |
| gemini_lite | Public goods | 0% (0/22) | – | – |

## Fraction slips corrected (counted answers)

| Model | Game | Normal (2A) | Disguised (2A) | Extreme (2C) |
|---|---|---:|---:|---:|
| gptoss120b | Vickrey auction | 0% (0/138) | 0% (0/131) | 0% (0/138) |
| gptoss120b | Cournot | 0% (0/135) | 0% (0/138) | 0% (0/137) |
| gptoss120b | Public goods | 0% (0/138) | 0% (0/138) | 0% (0/138) |
| nemotron | Vickrey auction | 0% (0/138) | 0% (0/138) | 50% (69/138) |
| nemotron | Cournot | 8% (11/138) | 10% (14/138) | 55% (76/138) |
| nemotron | Public goods | 0% (0/136) | 0% (0/138) | 0% (0/138) |
| kimi | Vickrey auction | 0% (0/138) | 0% (0/138) | 0% (0/137) |
| kimi | Cournot | 0% (0/138) | 0% (0/138) | 0% (0/138) |
| kimi | Public goods | 0% (0/138) | 0% (0/138) | 0% (0/138) |
| gemini_lite | Vickrey auction | 0% (0/138) | 0% (0/11) | 0% (0/138) |
| gemini_lite | Cournot | 0% (0/137) | 0% (0/138) | – |
| gemini_lite | Public goods | 0% (0/138) | 0% (0/138) | 0% (0/22) |

## Conversion slips (extreme only: right strategy, answer in the wrong unit)

| Model | Game | Counted 2C answers | Conversion slips | Missed answers that are conversion slips |
|---|---|---:|---:|---:|
| gptoss120b | Vickrey auction | 138 | 0% (0/138) | 0% (0/64) |
| gptoss120b | Cournot | 137 | 0% (0/137) | 0% (0/97) |
| nemotron | Vickrey auction | 138 | 1% (1/138) | 50% (1/2) |
| nemotron | Cournot | 138 | 0% (0/138) | 0% (0/1) |
| kimi | Vickrey auction | 137 | 0% (0/137) | 0% (0/2) |
| kimi | Cournot | 138 | 0% (0/138) | – |
| gemini_lite | Vickrey auction | 138 | 0% (0/138) | 0% (0/76) |
| gemini_lite | Cournot | 0 | – | – |

## λ on the Stage 2A scale (paired counted answers, slip-corrected)

| Model | Game | λ normal (2A) | λ extreme (2C, decoded) | Δλ = normal − extreme |
|---|---|---|---|---|
| gptoss120b | Vickrey auction | λ ≥ 944 (ceiling; n=138) | λ = 0.0501 [0.0325, 0.0708] (n=138) | Δλ ≥ +944 (normal at the ceiling, so only a lower bound) |
| gptoss120b | Cournot | λ = 0.173 [0.133, 0.218] (n=134) | λ = 0.00168 [0.00119, 0.00224] (n=134) | Δλ = +0.171 [+0.132, +0.216], P(Δλ > 0) = 1.00 |
| gptoss120b | Repeated PD | λ = 0.579 [0.274, 0.917] (n=138) | λ = 1.58 [1.12, 2.11] (n=138) | Δλ = -1.02 [-1.64, -0.442], P(Δλ > 0) = 0.00 |
| gptoss120b | Public goods | λ = 3.76 [3.07, 4.34] (n=138) | λ = 0.631 [0.531, 0.75] (n=138) | Δλ = +3.09 [+2.47, +3.78], P(Δλ > 0) = 1.00 |
| nemotron | Vickrey auction | λ ≥ 944 (ceiling; n=138) | λ = 5.62 [4.47, 7.08] (n=138) | Δλ ≥ +937 (normal at the ceiling, so only a lower bound) |
| nemotron | Cournot | λ = 0.00818 [0.00631, 0.0103] (n=138) | λ = 0.0237 [0.0183, 0.0299] (n=138) | Δλ = -0.0154 [-0.0217, -0.00989], P(Δλ > 0) = 0.00 |
| nemotron | Repeated PD | λ = 0.154 [0.00158, 0.473] (n=137) | λ = 2.59 [1.94, 3.45] (n=137) | Δλ = -2.44 [-3.34, -1.68], P(Δλ > 0) = 0.00 |
| nemotron | Public goods | λ ≥ 21.8 (ceiling; n=136) | λ = 6.13 [5.01, 7.29] (n=136) | Δλ ≥ +14.5 (normal at the ceiling, so only a lower bound) |
| kimi | Vickrey auction | λ ≥ 944 (ceiling; n=137) | λ = 47.3 [36.5, 59.6] (n=137) | Δλ ≥ +884 (normal at the ceiling, so only a lower bound) |
| kimi | Cournot | λ ≥ 299 (ceiling; n=138) | λ ≥ 631 (ceiling; n=138) | both wordings at the ceiling: no difference detectable in λ |
| kimi | Repeated PD | λ = 0.0075 [0.00109, 0.106] (n=138) | λ = 0.596 [0.299, 0.944] (n=138) | Δλ = -0.584 [-0.932, -0.275], P(Δλ > 0) = 0.00 |
| kimi | Public goods | λ = 2.51 [2.11, 2.9] (n=138) | λ = 2.74 [2.3, 3.25] (n=138) | Δλ = -0.247 [-0.887, +0.378], P(Δλ > 0) = 0.18 |
| gemini_lite | Vickrey auction | λ ≥ 944 (ceiling; n=138) | λ = 0.282 [0.211, 0.365] (n=138) | Δλ ≥ +944 (normal at the ceiling, so only a lower bound) |
| gemini_lite | Cournot | – | – | not enough answers |
| gemini_lite | Repeated PD | λ = 0.00316 [0.00103, 0.023] (n=138) | λ = 1.45 [1.03, 2] (n=138) | Δλ = -1.45 [-1.99, -1.02], P(Δλ > 0) = 0.00 |
| gemini_lite | Public goods | λ ≥ 13.3 (ceiling; n=22) | λ = 0.00282 [0.00103, 0.0183] (n=22) | Δλ ≥ +13.3 (normal at the ceiling, so only a lower bound) |

## Predictions vs results (all models pooled unless stated)

| Prediction | Result | Verdict |
|---|---|---|
| Vickrey auction: recognition ~90% (85–95) | 67% (281/417) | ❌ not met |
| Cournot: recognition ~25% (20–35) | 10% (43/413) | ❌ not met |
| Repeated PD: recognition ~55% (45–65) | 17% (94/551) | ❌ not met |
| Public goods: recognition ~95% (90–100) | 37% (163/436) | ❌ not met |
| Vickrey auction: play ~10 points lower than normal | +26 pts | ❌ not met |
| Cournot: play 35–45 points lower than normal | +21 pts | ❌ not met |
| Public goods: play within ±5 points of normal | +9 pts | ❌ not met |
| Repeated PD: extreme play 80–90%, above normal, at or above disguised | 83%; normal − extreme -38 pts, disguised − extreme -19 pts | ✅ met |
| Cournot drop, nemotron: ≥ 35 points | -1 pts | ❌ not met |
| Cournot drop, gemini_lite: 20–35 points | +nan pts | – |
| Cournot drop, kimi: ≤ 15 points | +0 pts | ✅ met |
| Cournot drop, gptoss120b: ≤ 15 points | +66 pts | ❌ not met |

_Ranges are read inclusively. Conversion-slip share of each drop: see the conversion-slip table (predicted 5–15 points of the Cournot and Vickrey drops)._

