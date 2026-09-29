# Power analysis — Stage 1

Source: `results/raw/pilot_n20.csv`, 160 trials. Test: two-sample proportions, two-sided. α = 0.05 Bonferroni-corrected over 4 games → **α = 0.0125 per game**. Power = 80%.

## 1. What the pilot observed

| Game | Named | Disguised | Difference | Cohen's h |
|---|---:|---:|---:|---:|
| Vickrey | 100% | 90% | -10 pts | 0.64 |
| Cournot | 90% | 50% | -40 pts | 0.93 |
| Repeated PD | 0% | 95% | +95 pts | 2.69 |
| Public goods | 95% | 90% | -5 pts | 0.19 |

## 2. What n=20 could actually detect

From a 90% baseline, the pilot could only reliably detect a drop of **46 percentage points** or more.

So Cournot's 40-point shift and the Prisoner's Dilemma's 95-point shift were both inside what the pilot could see. **Vickrey (−10) and public goods (−5) were not.** Their small observed shifts are not evidence of *no* framing effect — an effect of that size was simply undetectable at this sample. Stage 2 has to settle whether those two games are genuinely null.

## 3. Trials per cell for a given smallest effect of interest

Drop from a 90% baseline. **n is per cell** — per game per framing.

| Smallest drop worth detecting | Cohen's h | n per cell |
|---:|---:|---:|
| 30 pts | 0.73 | 43 |
| 25 pts | 0.62 | 58 |
| 20 pts | 0.52 | 84 |
| 15 pts | 0.40 | 137 |
| 10 pts | 0.28 | 277 |

## 4. For context only — n to detect the pilot's own effects

**Do not plan on these.** They inherit the pilot's noise and its tendency to overstate whichever effects happened to come out large.

| Game | n per cell |
|---|---:|
| Vickrey | 54 |
| Cournot | 26 |
| Repeated PD | 4 |
| Public goods | 603 |

## 5. Recommendation

**n = 138 per cell**, split evenly across the three paraphrases (46 each). That detects a 15-point shift from a 90% baseline at 80% power after correction — enough to settle whether Vickrey and public goods are genuinely null, rather than merely undetected.

The paraphrases are spread *within* each cell rather than multiplying it, so they cost nothing extra in trials — and if wording turns out to matter, that shows up as variance rather than being averaged away.

**The smallest effect worth detecting is your decision, not mine** — it goes in `preregistration-1.md` and has to be fixed before Stage 2 runs. 15 points is a defensible default: smaller than any effect that would change what the paper claims, large enough to stay affordable.

## 6. Compute

1104 trials per model (4 games × 2 framings × 138), which is **2208 API calls** — each trial is a play call plus a probe call.

- **gpt-oss-120b and Qwen 3.8 27B (Groq):** measured 3.7 trials/min in the pilot, token-limited → **~5.0 hours each**. If Groq's limits are per model rather than per account, they can run in parallel.
- **Nemotron 3 Ultra (OpenRouter free):** capped by requests per DAY, not speed. At 50/day: **~45 days**. At 1,000/day (after $10 of credit has ever been bought): **~3 days**.
- **Gemini (Google free tier):** limits are not published, only shown in your AI Studio dashboard. Measure in a short pilot first.

**At this n, Nemotron on the free cap does not fit Stage 2's four-week window.** Either buy the $10 of credit, or lower n for Nemotron only and accept less power for that one model.

## 7. Caveats

- Proportions are a proxy; the real analysis compares fitted λ. Conservative for the continuous games. Re-run as a simulation in Stage 3.
- The 90% baseline is the pilot's named-framing rate. The PD's named rate is 0%, so its own planning would differ — but that effect is so large it is detectable at almost any n.
- Assumes trials are independent. Seeds are shared across paraphrases, so within a cell trials are paired by parameter draw — a paired analysis would be slightly more powerful still.
