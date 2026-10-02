# The decision gate: how "good" and "stable" are judged

Written by the author on 2026-10-03 (final workbook, Task 4), **before** the Stage 2A fits of
gpt-oss-120b, Kimi K3 and Gemini 3.5 Flash Lite existed (only Nemotron's was complete).
Pre-registration 1 defines the three gate options but not the criteria; these make them operational.

## When a fit is "good" (held-out calibration)

For each model and game:
- fit λ on two of the three normal-wording paraphrases;
- predict the equilibrium-play rate of the third, held-out paraphrase;
- count the fit as calibrated if the prediction is within **±10 points** of the observed rate.

Rotate the held-out paraphrase through all three, and call the game calibrated if at least 2 of
the 3 rotations are. A model's fits are **good** if this holds in **at least 3 of its 4 games**.

*Why held out:* in a two-action game one free λ can match one observed rate almost exactly, so
in-sample calibration would be nearly a tautology.

*Hard fail:* if the observed rate is one QRE cannot produce for any λ ≥ 0, that game's fit is
**poor**, whatever the ±10 rule says. Example: stage-game PD cooperation above 50%, because QRE
cooperation at τ = 0 is at most ½.

## Whether λ is "stable across games"

Raw λ is not comparable across games: it scales with the size of the payoffs. **λ is declared
not comparable across games without normalisation, and the gate goes game by game.** This makes
option 1 ("λ stable") untestable as written, so the gate chooses between option 2 (good fits,
game by game) and option 3 (poor fits).

Normalising by a "typical deviation" was rejected: that choice is a free parameter which could be
tuned to manufacture stability.

## The derived subsidy at the extremes of λ

τ\*(0.9, λ) = 1.9 + ln 9 / λ.
- **Floor**, λ < 0.046 (so τ\* > 50): cap τ\* at 50; report the cap, and QRE's own prediction at
  50, which is below 90%.
- **Ceiling**, λ ≥ 3.66 (so τ\* ≤ 2.5): QRE already predicts at least 90% at τ = 2.5, so derived
  and guessed coincide. Drop that model's separate derived level and report why; its τ = 2.5
  cell serves both.
