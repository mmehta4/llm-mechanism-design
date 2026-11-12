# Pre-registration addendum: concurrent controls for the prisoner's dilemma and for drift

Addendum to pre-registrations 1–4 (osf.io/2uqpj, osf.io/6hz8d, osf.io/cqnsy, osf.io/qg43y).
It is filed on OSF before any of the data below exists. Runner: `experiments/addendum.py`.

**Amendment before filing (13 November 2026, no data collected).** Kimi K3 was retired on
NVIDIA's API on 15 October 2026 (the endpoint now returns HTTP 410, "Gone"), so it cannot be
re-asked where Stages 2A–5 ran it. Kimi K3 is therefore dropped. In its place, Block P is run
on Mistral Large 4 (Mistral AI, `mistralai/mistral-large-4-1t-a52b`), on the same NVIDIA API
and free tier. Mistral Large 4 has no earlier data, so for it only the within-addendum contrasts
C1–C3 apply, and it carries no directional prediction. The predictions for Kimi K3 in Section 4
were written before the retirement was found; they are kept for the record and are not scored.
The first version of this file was committed as git commit bb64cba.

## 1. Questions

1. **Loss framing.** The extreme prisoner's dilemma of Stage 2C changes three things at once:
   - it removes the frame and the story;
   - it doubles the payoffs;
   - it shifts them so that two payoffs are losses (mutual defection −2, sucker −4).

   Does the loss framing contribute to the extreme wording's rise in defection?
2. **Stating the rule.** Is the lower cooperation under Stage 5's rule stated at τ = 0, compared
   with Stage 2A's question without the rule, present when both are collected at the same time?
3. **Drift in Stage 2C.** Do gpt-oss's standard → extreme drops in Cournot and Vickrey equilibrium
   play hold when both wordings are collected at the same time?

## 2. Design

Every arm of a model is asked in one shuffled order (seeded), so all arms are collected
concurrently.

**Block P (gpt-oss-120b, Nemotron 3 Ultra, Gemini 3.5 Flash Lite, Mistral Large 4): 100
questions per arm**
- Seeds are `MASTER_SEED + 60000 + k` (k = 0..99), with paraphrase `k mod 3`.
- Round 1 of the 10-round game.
- All arms share the seeds, and the extreme arms share the counterbalanced letters.

| Arm | Question |
|---|---|
| P1 | Stage 2A standard wording, payoffs (5, 3, 1, 0), no subsidy rule |
| P2 | P1 plus Stage 5's subsidy rule stated at τ = 0.0 |
| P3 | Stage 2C extreme wording, payoffs 2u − 4: (6, 2, −2, −4) |
| P4 | The same text as P3, payoffs 2u + 1: (11, 7, 3, 1), so no payoff is negative |

P3 and P4 are positive affine transformations of P1 (scale 2). A deriving model plays them
identically (paper, Proposition 1).

**Block G (gpt-oss only): 69 questions per arm**
- These are the Stage 2A/2C paired seeds `MASTER_SEED + k` (k = 0..68), with paraphrase `k mod 3`.
- Arms: Cournot standard; Cournot extreme; Vickrey standard; Vickrey extreme.

**Unchanged from Stages 2A–5**
- Settings: models, default sampling, answer schemas, competence probes.
- Providers, the same as for every earlier stage:
  - gpt-oss-120b on Groq (model key `gptoss120b`), as in Stages 2A, 2B, 2C and 5;
  - Nemotron 3 Ultra on NVIDIA's API;
  - Gemini on Google AI Studio;
  - Mistral Large 4 on NVIDIA's API (new to this addendum).

  No other provider is used. Every comparison with earlier stages is against data from these
  same providers.
- Scoring:
  - the Stage 2C fraction-slip rule;
  - the registered tolerance, with the matched tolerance of ±0.5 after decoding also reported.
- Rules for non-answers: server refusals and empty replies are re-asked, never scored.

**Sample:** 1,876 questions in total. The counts are fixed and form the stopping rule.

## 3. Analysis

**Outcome**
- Block P: defection among probe-passed answers (`AT_EQUILIBRIUM` or `STRATEGIC_GAP`).
- Block G: equilibrium play among probe-passed answers.

**Block P contrasts, per model**

| Contrast | What it measures |
|---|---|
| C1 = P2 − P1 | Stating the rule |
| C2 = P3 − P4 | Loss framing |
| C3 = P4 − P1 | Frame and story removed, payoffs positive |
| C4 = P3 − P1 | Concurrent replication of the Stage 2C shift |

- Two-sided Fisher exact tests, with Holm correction across the four models within each of
  C1–C3, and across the three models with earlier data (gpt-oss, Nemotron, Gemini) for C4.
- Pooled across models: a Cochran–Mantel–Haenszel test stratified by model.
- Effects are reported with 95% Newcombe intervals.

**Block G**
- Standard vs extreme on pairs with the same seed: exact McNemar test.
- Descriptive comparison with the original Stage 2A/2C answers on the same seeds.

**Power:** 100 per arm gives about 80% power for a 20-point difference near 50% (α = 0.05,
two-sided).

## 4. Predictions (author, written before filing)

Kimi K3's predictions below are not scored, because Kimi K3 is not run (see the amendment).
Mistral Large 4 carries no directional prediction.

Each prediction anchors on earlier results: Stage 2A for P1, Stage 5 at τ = 0 for P2, and
Stage 2C for P3.

**Arm levels:** defection (%) among probe-passed answers, with a predicted range.

| Model | P1 (2A standard) | P2 (+ rule at τ = 0) | P3 (extreme, losses) | P4 (extreme, positive) |
|---|---|---|---|---|
| gpt-oss-120b | 70 [60–80] | 90 [82–97] | 86 [78–94] | 85 [77–93] |
| Nemotron 3 Ultra | 60 [50–70] | 82 [72–90] | 93 [86–98] | 92 [85–98] |
| Kimi K3 | 46 [35–57] | 69 [58–79] | 70 [60–80] | 68 [58–78] |
| Gemini 3.5 Flash Lite | 9 [3–17] | 6 [2–13] | 85 [77–92] | 83 [75–91] |

**C1, stating the rule**
- Predicted: gpt-oss about +20, Nemotron about +22, Kimi about +23 points. Gemini ≈ 0, with
  |C1| < 8.
- Significance:
  - gpt-oss and Nemotron survive Holm correction;
  - Kimi is positive and significant, but is the least safe of the three (power after Holm
    about 0.75);
  - the pooled CMH test is significant.
- Reason: three models moved by 23 points each, in the same direction, across two providers,
  while Gemini did not move. Drift is unlikely to produce that pattern.

**C2, loss framing**
- Predicted: C2 ≈ 0 for every model, with |C2| ≤ 8 and no model significant.
- Pooled: the CMH test is not significant, and the pooled estimate is within ±5 points.
- Reason:
  - once the frame is gone, the models compute dominance, and defection dominates in both payoff
    versions; maximin also picks defection in both (−2 vs −4, and 3 vs 1);
  - gpt-oss and Nemotron are near the ceiling;
  - any nonzero effect is most likely for Kimi, the least ceiling-bound.

**C3, frame removed with positive payoffs**
- Predicted: gpt-oss about +15, Nemotron about +32, Kimi about +22, Gemini about +74. All four
  are positive.
- Significance: Nemotron, Kimi and Gemini are significant after Holm; gpt-oss has about 75%
  power to clear it.
- Reason: if C2 ≈ 0, this is the whole extreme-wording shift.

**C4, replication of the extreme-wording shift**
- Predicted: Stage 2C replicates within ±10 points per model: about +16, +33, +24 and +76.
- Significance: the same pattern as C3, and the pooled CMH test has p < 10⁻¹⁰.

**Block G, gpt-oss's concurrent drops**
- Predicted: the drops hold.
  - Cournot: standard about 95% [88–100] vs extreme about 30% [18–45].
  - Vickrey: standard at least 97% vs extreme about 50% [35–65].
- Significance: the exact McNemar test gives p < 10⁻⁶ for both.
- Both rates fall within ±12 points of the original answers on the same seeds.
- Reason: a 46–66-point drop confined to one wording, with recognition at 1–10% in the extreme
  wording, is a wording effect, while drift would move both wordings together.

## 5. Interpretation key

**Loss framing (C2)**
- **C2 ≈ 0:** the extreme-wording shift is not loss framing. The paper attributes it to removing
  the frame and story (C3).
- **C2 > 0 (more defection with losses):** loss framing contributes. The paper reports C3 as the
  frame effect, and C2 separately.

**Stating the rule (C1)**
- **C1 ≈ 0 for a model:** the Stage 5 vs Stage 2A gap was drift for that model, and the paper
  withdraws the claim for it.
- **C1 > 0 (more defection with the rule):** the effect of stating the rule is confirmed for
  that model.

**Drift in Stage 2C (Block G)**
- **The drops hold:** the Stage 2A → 2C results for gpt-oss are not drift.
- **They do not hold:** the paper reports that, and reads those results as possibly drift.

All results are reported, whatever they show.
