# PRACTICE ONLY: decision gate on the Stage 1 practice run

Criteria: `docs/decision-gate.md` (held-out calibration ±10 points; a game is calibrated in ≥ 2 of 3 rotations; a model's fits are good in ≥ 3 of 4 games).

## gptoss120b (practice)

| Game | Held out | λ (trained on the other two) | Predicted | Observed | Within ±10 |
|---|---:|---:|---:|---:|:---:|
| **vickrey** | | | | **100%** | **not calibrated**  |
| **cournot** | | | | **95%** | **not calibrated**  |
| **repeated_pd** | | | | **75%** | **not calibrated**  |
| **public_goods** | | | | **95%** | **not calibrated**  |

**Fits: POOR** (0/4 games calibrated). Stage 5 λ̂ (named PD, posterior median): **0.546**.

## Gate

λ is not compared across games, so option 1 is untestable (decision-gate.md).

**Option 3: fits are poor for every model; Stage 4 studies why.**
