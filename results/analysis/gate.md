# Decision gate (all four models)

Criteria: `docs/decision-gate.md` (held-out calibration ±10 points; a game is calibrated in ≥ 2 of 3 rotations; a model's fits are good in ≥ 3 of 4 games).

## gptoss120b

| Game | Held out | λ (trained on the other two) | Predicted | Observed | Within ±10 |
|---|---:|---:|---:|---:|:---:|
| vickrey | wording 1 | 1e+03 | 82% | 100% | ❌ |
| vickrey | wording 2 | 1e+03 | 90% | 100% | ✅ |
| vickrey | wording 3 | 1e+03 | 87% | 100% | ❌ |
| **vickrey** | | | | **100%** | **not calibrated**  |
| cournot | wording 1 | 0.546 | 51% | 91% | ❌ |
| cournot | wording 2 | 0.119 | 27% | 100% | ❌ |
| cournot | wording 3 | 0.145 | 29% | 98% | ❌ |
| **cournot** | | | | **96%** | **not calibrated**  |
| repeated_pd | wording 1 | 0.729 | 72% | 61% | ❌ |
| repeated_pd | wording 2 | 1.03 | 78% | 50% | ❌ |
| repeated_pd | wording 3 | 0.0316 | 51% | 96% | ❌ |
| **repeated_pd** | | | | **69%** | **not calibrated**  |
| public_goods | wording 1 | 2.82 | 76% | 100% | ❌ |
| public_goods | wording 2 | 141 | 100% | 91% | ✅ |
| public_goods | wording 3 | 2.82 | 76% | 100% | ❌ |
| **public_goods** | | | | **97%** | **not calibrated**  |

**Fits: POOR** (0/4 games calibrated). Stage 5 λ̂ (named PD, posterior median): **0.579**.

## nemotron

| Game | Held out | λ (trained on the other two) | Predicted | Observed | Within ±10 |
|---|---:|---:|---:|---:|:---:|
| vickrey | wording 1 | 1e+03 | 82% | 100% | ❌ |
| vickrey | wording 2 | 1e+03 | 90% | 100% | ✅ |
| vickrey | wording 3 | 1e+03 | 87% | 100% | ❌ |
| **vickrey** | | | | **100%** | **not calibrated**  |
| cournot | wording 1 | 0.00109 | 3% | 93% | ❌ |
| cournot | wording 2 | 0.00237 | 4% | 83% | ❌ |
| cournot | wording 3 | 0.00109 | 3% | 93% | ❌ |
| **cournot** | | | | **90%** | **not calibrated**  |
| repeated_pd | wording 1 | 0.075 | 53% | 61% | ✅ |
| repeated_pd | wording 2 | 0.0282 | 51% | 67% | ❌ |
| repeated_pd | wording 3 | 0.335 | 61% | 49% | ❌ |
| **repeated_pd** | | | | **59%** | **not calibrated**  |
| public_goods | wording 1 | 141 | 100% | 100% | ✅ |
| public_goods | wording 2 | 141 | 100% | 100% | ✅ |
| public_goods | wording 3 | 141 | 100% | 100% | ✅ |
| **public_goods** | | | | **100%** | **calibrated**  |

**Fits: POOR** (1/4 games calibrated). Stage 5 λ̂ (named PD, posterior median): **0.154**.

## kimi

| Game | Held out | λ (trained on the other two) | Predicted | Observed | Within ±10 |
|---|---:|---:|---:|---:|:---:|
| vickrey | wording 1 | 1e+03 | 82% | 100% | ❌ |
| vickrey | wording 2 | 1e+03 | 90% | 100% | ✅ |
| vickrey | wording 3 | 1e+03 | 87% | 100% | ❌ |
| **vickrey** | | | | **100%** | **not calibrated**  |
| cournot | wording 1 | 387 | 100% | 100% | ✅ |
| cournot | wording 2 | 866 | 100% | 100% | ✅ |
| cournot | wording 3 | 398 | 100% | 100% | ✅ |
| **cournot** | | | | **100%** | **calibrated**  |
| repeated_pd | wording 1 | 0.0141 | 51% | 35% | ❌ |
| repeated_pd | wording 2 | 0.00818 | 50% | 48% | ✅ |
| repeated_pd | wording 3 | 0.00688 | 50% | 54% | ✅ |
| **repeated_pd** | | | | **46%** | **not calibrated** hard fail: below what any λ ≥ 0 produces |
| public_goods | wording 1 | 2 | 63% | 98% | ❌ |
| public_goods | wording 2 | 6.88 | 97% | 89% | ✅ |
| public_goods | wording 3 | 1.83 | 60% | 100% | ❌ |
| **public_goods** | | | | **96%** | **not calibrated**  |

**Fits: POOR** (1/4 games calibrated). Stage 5 λ̂ (named PD, posterior median): **0.0075**.

## gemini_lite

| Game | Held out | λ (trained on the other two) | Predicted | Observed | Within ±10 |
|---|---:|---:|---:|---:|:---:|
| vickrey | wording 1 | 1e+03 | 82% | 100% | ❌ |
| vickrey | wording 2 | 1e+03 | 90% | 100% | ✅ |
| vickrey | wording 3 | 1e+03 | 87% | 100% | ❌ |
| **vickrey** | | | | **100%** | **not calibrated**  |
| cournot | wording 1 | 0.688 | 55% | 93% | ❌ |
| cournot | wording 2 | 0.818 | 59% | 98% | ❌ |
| cournot | wording 3 | 0.501 | 49% | 98% | ❌ |
| **cournot** | | | | **96%** | **not calibrated**  |
| repeated_pd | wording 1 | 0.00345 | 50% | 22% | ❌ |
| repeated_pd | wording 2 | 0.00387 | 50% | 0% | ❌ |
| repeated_pd | wording 3 | 0.00376 | 50% | 4% | ❌ |
| **repeated_pd** | | | | **9%** | **not calibrated** hard fail: below what any λ ≥ 0 produces |
| public_goods | wording 1 | 141 | 100% | 100% | ✅ |
| public_goods | wording 2 | 141 | 100% | 100% | ✅ |
| public_goods | wording 3 | 141 | 100% | 100% | ✅ |
| **public_goods** | | | | **100%** | **calibrated**  |

**Fits: POOR** (1/4 games calibrated). Stage 5 λ̂ (named PD, posterior median): **0.00316**.

## Gate

λ is not compared across games, so option 1 is untestable (decision-gate.md).

**Option 3: fits are poor for every model; Stage 4 studies why.**
