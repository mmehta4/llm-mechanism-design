# Stage 2A confirmatory analysis: gemini_lite

## Main test: share of equilibrium play, normal vs disguised

| Game | Normal | Disguised | Change | z-test p | Holm p | Fisher p | Excluded (n / d) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Vickrey auction | 100% (138/138) | 91% (10/11) | -9 pts | 0.00038 | 0.00038 | 0.0738 | 0 / 127 |
| Cournot | 96% (132/137) | 4% (6/138) | -92 pts | 1.48e-52 | 5.93e-52 | 1.15e-63 | 1 / 0 |
| Repeated PD | 9% (12/138) | 70% (97/138) | +62 pts | 1.23e-25 | 3.69e-25 | 2.12e-27 | 0 / 0 |
| Public goods | 100% (138/138) | 80% (110/138) | -20 pts | 2.37e-08 | 4.75e-08 | 1.62e-09 | 0 / 0 |

## Public goods: equivalence test (the predicted null)

TOST p = 0.977 against ±13 points: **equivalence NOT shown (the null is not supported)**. (Threshold 0.05; the Holm-corrected threshold for this game is applied when the four-game family is reported together.)

## Headline: λ and Δλ (quantal response fits)

| Game | λ normal | λ disguised | Δλ = normal − disguised |
|---|---|---|---|
| Vickrey auction | λ ≥ 944 (ceiling; n=138) | λ = 3.98 [1.54, 7.72] (n=11) | Δλ ≥ +936 (normal at the ceiling, so only a lower bound) |
| Cournot | λ = 0.649 [0.501, 0.818] (n=137) | λ = 0.00473 [0.00355, 0.00596] (n=138) | Δλ = +0.645 [+0.496, +0.813], P(Δλ > 0) = 1.00 |
| Repeated PD | λ = 0.00316 [0.00103, 0.023] (n=138) | λ = 0.631 [0.325, 0.972] (n=138) | Δλ = -0.629 [-0.97, -0.323], P(Δλ > 0) = 0.00 |
| Public goods | λ ≥ 21.8 (ceiling; n=138) | λ = 0.434 [0.355, 0.531] (n=138) | Δλ ≥ +21.2 (normal at the ceiling, so only a lower bound) |

## Wording check: equilibrium share by wording

| Game | Framing | Wording 1 | Wording 2 | Wording 3 | Spread |
|---|---|---:|---:|---:|---:|
| Vickrey auction | named | 100% | 100% | 100% | 0 pts |
| Vickrey auction | disguised | 100% | 100% | 75% | 25 pts |
| Cournot | named | 93% | 98% | 98% | 4 pts |
| Cournot | disguised | 0% | 4% | 9% | 9 pts |
| Repeated PD | named | 22% | 0% | 4% | 22 pts |
| Repeated PD | disguised | 100% | 13% | 98% | 87 pts |
| Public goods | named | 100% | 100% | 100% | 0 pts |
| Public goods | disguised | 39% | 100% | 100% | 61 pts |

_If the spread between wordings is as large as the normal-vs-disguised change, the disguise effect for that game is not distinguishable from a wording effect._
