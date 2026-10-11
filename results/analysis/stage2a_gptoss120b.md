# Stage 2A confirmatory analysis: gptoss120b

## Main test: share of equilibrium play, normal vs disguised

| Game | Normal | Disguised | Change | z-test p | Holm p | Fisher p | Excluded (n / d) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Vickrey auction | 100% (138/138) | 98% (129/131) | -2 pts | 0.145 | 0.299 | 0.236 | 0 / 7 |
| Cournot | 96% (130/135) | 80% (110/138) | -17 pts | 2.63e-05 | 0.000105 | 2.36e-05 | 3 / 0 |
| Repeated PD | 69% (95/138) | 73% (101/138) | +4 pts | 0.426 | 0.426 | 0.507 | 0 / 0 |
| Public goods | 97% (134/138) | 93% (128/138) | -4 pts | 0.0998 | 0.299 | 0.168 | 0 / 0 |

## Public goods: equivalence test (the predicted null)

TOST p = 0.000804 against ±13 points: **equivalent within ±13 points**. (Threshold 0.05; the Holm-corrected threshold for this game is applied when the four-game family is reported together.)

## Headline: λ and Δλ (quantal response fits)

| Game | λ normal | λ disguised | Δλ = normal − disguised |
|---|---|---|---|
| Vickrey auction | λ ≥ 944 (ceiling; n=138) | λ = 1.12 [0.866, 1.45] (n=131) | Δλ ≥ +943 (normal at the ceiling, so only a lower bound) |
| Cournot | λ = 0.173 [0.133, 0.218] (n=135) | λ = 0.0274 [0.0218, 0.0345] (n=138) | Δλ = +0.146 [+0.107, +0.193], P(Δλ > 0) = 1.00 |
| Repeated PD | λ = 0.579 [0.274, 0.917] (n=138) | λ = 0.772 [0.447, 1.12] (n=138) | Δλ = -0.193 [-0.668, +0.271], P(Δλ > 0) = 0.20 |
| Public goods | λ = 3.76 [3.07, 4.34] (n=138) | λ = 1.19 [1, 1.37] (n=138) | Δλ = +2.53 [+1.88, +3.24], P(Δλ > 0) = 1.00 |

## Wording check: equilibrium share by wording

| Game | Framing | Wording 1 | Wording 2 | Wording 3 | Spread |
|---|---|---:|---:|---:|---:|
| Vickrey auction | named | 100% | 100% | 100% | 0 pts |
| Vickrey auction | disguised | 95% | 100% | 100% | 5 pts |
| Cournot | named | 91% | 100% | 98% | 9 pts |
| Cournot | disguised | 63% | 87% | 89% | 26 pts |
| Repeated PD | named | 61% | 50% | 96% | 46 pts |
| Repeated PD | disguised | 83% | 59% | 78% | 24 pts |
| Public goods | named | 100% | 91% | 100% | 9 pts |
| Public goods | disguised | 87% | 96% | 96% | 9 pts |

_If the spread between wordings is as large as the normal-vs-disguised change, the disguise effect for that game is not distinguishable from a wording effect._
