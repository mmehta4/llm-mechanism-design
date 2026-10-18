# Stage 5 confirmatory analysis: all models

## gptoss120b  (λ̂ = 0.579)

| τ | Cooperation [95% CI] | QRE at λ̂ [band] | Classical | Within ±10 of QRE |
|---:|---:|---:|---:|:---:|
| 0 | 8% (8/100) [4%, 15%] | 32% [24%, 40%] | 0% | ❌ |
| 1.5 | 57% (57/100) [47%, 66%] | 50% [50%, 50%] | 50% (mixed) | ✅ |
| 2.5 | 84% (84/100) [76%, 90%] | 62% [56%, 68%] | 100% | ❌ |
| 5.7 | 98% (98/100) [93%, 99%] | 90% [75%, 97%] | 100% | ✅ |

**Test 1 (τ = 2.5): QRE vs classical.** |obs − 100%| − |obs − QRE| = -6 pts [-20, +8]: **classical is closer** (interval includes 0).
**Test 2 (τ* = 5.7): the derived mechanism.** 98% (98/100) [93%, 99%]: target exceeded: QRE under-predicts responsiveness; the mechanism overpays.
**Test 3 (τ = 1.5): stage-game halfway point.** 57% (57/100) [47%, 66%], exact binomial p = 0.193 against 50%.
**Rule line at τ = 0.0 vs Stage 2A (no line):** 8% (8/100) vs 31% (43/138), p = 1.72e-05.

**Reading (docs/interpretation-key.md):** about 50% at τ = 1.5, but not close to QRE at every other level.

## nemotron  (λ̂ = 0.154)

| τ | Cooperation [95% CI] | QRE at λ̂ [band] | Classical | Within ±10 of QRE |
|---:|---:|---:|---:|:---:|
| 0 | 18% (18/100) [12%, 27%] | 44% [35%, 50%] | 0% | ❌ |
| 1.5 | 96% (96/100) [90%, 98%] | 50% [50%, 50%] | 50% (mixed) | ❌ |
| 2.5 | 100% (100/100) [96%, 100%] | 54% [50%, 60%] | 100% | ❌ |
| 16.2 | 100% (100/100) [96%, 100%] | 90% [51%, 100%] | 100% | ✅ |

**Test 1 (τ = 2.5): QRE vs classical.** |obs − 100%| − |obs − QRE| = -46 pts [-46, -46]: **classical is closer**.
**Test 2 (τ* = 16.2): the derived mechanism.** 100% (100/100) [96%, 100%]: target exceeded: QRE under-predicts responsiveness; the mechanism overpays.
**Test 3 (τ = 1.5): stage-game halfway point.** 96% (96/100) [90%, 98%], exact binomial p = 6.45e-24 against 50%.
**Rule line at τ = 0.0 vs Stage 2A (no line):** 18% (18/100) vs 41% (56/137), p = 0.000175.

**Reading (docs/interpretation-key.md):** well above 50% at τ = 1.5: cooperation norm or repeated-game reasoning (the reasoning codes decide which); the mechanism worked but overpaid.

## kimi  (λ̂ = 0.0075)

| τ | Cooperation [95% CI] | QRE at λ̂ [band] | Classical | Within ±10 of QRE |
|---:|---:|---:|---:|:---:|
| 0 | 31% (31/100) [23%, 41%] | 50% [46%, 50%] | 0% | ❌ |
| 1.5 | 95% (95/100) [89%, 98%] | 50% [50%, 50%] | 50% (mixed) | ❌ |
| 2.5 | 99% (99/100) [95%, 100%] | 50% [50%, 53%] | 100% | ❌ |
| 50 | 99% (99/100) [95%, 100%] | 59% [51%, 99%] | 100% | ❌ |

**Test 1 (τ = 2.5): QRE vs classical.** |obs − 100%| − |obs − QRE| = -48 pts [-50, -44]: **classical is closer**.
**Test 2 (τ* = 50): the derived mechanism.** 99% (99/100) [95%, 100%]: target exceeded: QRE under-predicts responsiveness; the mechanism overpays.
**Test 3 (τ = 1.5): stage-game halfway point.** 95% (95/100) [89%, 98%], exact binomial p = 1.25e-22 against 50%.
**Rule line at τ = 0.0 vs Stage 2A (no line):** 31% (31/100) vs 54% (75/138), p = 0.000347.

**Reading (docs/interpretation-key.md):** well above 50% at τ = 1.5: cooperation norm or repeated-game reasoning (the reasoning codes decide which); the mechanism worked but overpaid.

## gemini_lite  (λ̂ = 0.00316)

| τ | Cooperation [95% CI] | QRE at λ̂ [band] | Classical | Within ±10 of QRE |
|---:|---:|---:|---:|:---:|
| 0 | 94% (94/100) [88%, 97%] | 50% [49%, 50%] | 0% | ❌ |
| 1.5 | 100% (100/100) [96%, 100%] | 50% [50%, 50%] | 50% (mixed) | ❌ |
| 2.5 | 100% (100/100) [96%, 100%] | 50% [50%, 51%] | 100% | ❌ |
| 50 | 100% (100/100) [96%, 100%] | 54% [51%, 75%] | 100% | ❌ |

**Test 1 (τ = 2.5): QRE vs classical.** |obs − 100%| − |obs − QRE| = -50 pts [-50, -50]: **classical is closer**.
**Test 2 (τ* = 50): the derived mechanism.** 100% (100/100) [96%, 100%]: target exceeded: QRE under-predicts responsiveness; the mechanism overpays.
**Test 3 (τ = 1.5): stage-game halfway point.** 100% (100/100) [96%, 100%], exact binomial p = 1.58e-30 against 50%.
**Rule line at τ = 0.0 vs Stage 2A (no line):** 94% (94/100) vs 91% (126/138), p = 0.438.

**Reading (docs/interpretation-key.md):** well above 50% at τ = 1.5: cooperation norm or repeated-game reasoning (the reasoning codes decide which); the mechanism worked but overpaid.

## Test 3 across models (Holm)

| Model | p | Holm p |
|---|---:|---:|
| gptoss120b | 0.193 | 0.193 |
| nemotron | 6.45e-24 | 1.93e-23 |
| kimi | 1.25e-22 | 2.5e-22 |
| gemini_lite | 1.58e-30 | 6.31e-30 |
