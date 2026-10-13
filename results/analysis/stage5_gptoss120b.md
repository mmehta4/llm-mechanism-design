# Stage 5 confirmatory analysis: gptoss120b

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

