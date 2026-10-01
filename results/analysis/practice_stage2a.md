# PRACTICE RUN ONLY: Stage 1, gpt-oss-120b, 20 per cell (not confirmatory)

## Main test: share of equilibrium play, normal vs disguised

| Game | Normal | Disguised | Change | z-test p | Holm p | Fisher p | Excluded (n / d) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Vickrey auction | 100% (20/20) | 95% (18/19) | -5 pts | 0.299 | 0.597 | 0.487 | 0 / 1 |
| Cournot | 95% (18/19) | 50% (10/20) | -45 pts | 0.00191 | 0.00766 | 0.00334 | 1 / 0 |
| Repeated PD | 75% (15/20) | 95% (19/20) | +20 pts | 0.0765 | 0.23 | 0.182 | 0 / 0 |
| Public goods | 95% (19/20) | 90% (18/20) | -5 pts | 0.548 | 0.597 | 1 | 0 / 0 |

## Public goods: equivalence test (the predicted null)

TOST p = 0.188 against ±13 points: **equivalence NOT shown (the null is not supported)**. (Threshold 0.05; the Holm-corrected threshold for this game is applied when the four-game family is reported together.)

## Headline: λ and Δλ (quantal response fits)

| Game | λ normal | λ disguised | Δλ = normal − disguised |
|---|---|---|---|
| Vickrey auction | λ ≥ 631 (ceiling; n=20) | λ ≥ 596 (ceiling; n=19) | both wordings at the ceiling: no difference detectable in λ |
| Cournot | λ = 0.15 [0.0708, 0.274] (n=19) | λ = 0.0075 [0.00355, 0.0133] (n=20) | Δλ = +0.141 [+0.0631, +0.264], P(Δλ > 0) = 1.00 |
| Repeated PD | λ = 0.546 [0.00194, 1.78] (n=20) | λ = 2.66 [1, 5.62] (n=20) | Δλ = -2.1 [-5.2, -0.0437], P(Δλ > 0) = 0.02 |
| Public goods | λ = 1.58 [1, 2.44] (n=20) | λ = 0.866 [0.531, 1.33] (n=20) | Δλ = +0.719 [-0.0347, +1.6], P(Δλ > 0) = 0.97 |

## Wording check: equilibrium share by wording

| Game | Framing | Wording 1 | Wording 2 | Wording 3 | Spread |
|---|---|---:|---:|---:|---:|
| Vickrey auction | named | 100% | – | – | – |
| Vickrey auction | disguised | 95% | – | – | – |
| Cournot | named | 95% | – | – | – |
| Cournot | disguised | 50% | – | – | – |
| Repeated PD | named | 75% | – | – | – |
| Repeated PD | disguised | 95% | – | – | – |
| Public goods | named | 95% | – | – | – |
| Public goods | disguised | 90% | – | – | – |

_If the spread between wordings is as large as the normal-vs-disguised change, the disguise effect for that game is not distinguishable from a wording effect._
