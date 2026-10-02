# PIPELINE CHECK ONLY: simulated QRE players (no real Stage 5 data)

## synthetic QRE player, λ = 0.154  (λ̂ = 0.154)

| τ | Cooperation [95% CI] | QRE at λ̂ [band] | Classical | Within ±10 of QRE |
|---:|---:|---:|---:|:---:|
| 0 | 39% (39/100) [30%, 49%] | 44% [44%, 45%] | 0% | ✅ |
| 1.5 | 44% (44/100) [35%, 54%] | 50% [50%, 50%] | 50% (mixed) | ✅ |
| 2.5 | 49% (49/100) [39%, 59%] | 54% [53%, 54%] | 100% | ✅ |
| 16.2 | 92% (92/100) [85%, 96%] | 90% [88%, 92%] | 100% | ✅ |

**Test 1 (τ = 2.5): QRE vs classical.** |obs − 100%| − |obs − QRE| = +46 pts [+36, +46]: **QRE is closer**.
**Test 2 (τ* = 16.2): the derived mechanism.** 92% (92/100) [85%, 96%]: within 90 ± 15.
**Test 3 (τ = 1.5): stage-game halfway point.** 44% (44/100) [35%, 54%], exact binomial p = 0.271 against 50%.
**Rule line at τ = 0.0 vs Stage 2A (no line):** 39% (39/100) vs 39% (53/137), p = 0.961.

**Reading (docs/interpretation-key.md):** QRE describes this model.

