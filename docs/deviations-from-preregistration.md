# Deviations from pre-registration 1

The registered document (`docs/preregistration-1.md`, OSF https://osf.io/2uqpj,
SHA-256 `a70cf95a…4a78a40`) is left exactly as registered. Everything that turned out to
differ from it is recorded here, dated, and will be reported in the paper's
"Deviations from pre-registration" section.

---

## 1. Practice-run scoring error in the prisoner's dilemma (found 2026-09-30)

**What was wrong.** In the named (C/D) prisoner's dilemma, the scoring code compared the
model's answer with the *disguised* framing's label (X or Y) instead of with D. No
named-PD answer could ever be scored as the equilibrium.

**What it affected.** Only the derived columns `equilibrium`, `deviation` and `verdict`
of named-PD rows. The models' answers, probe answers and full transcripts were recorded
correctly. All affected rows were rescored with `analysis/rescore_named_pd.py`, using
the same verdict code that live trials use.

**Corrected practice-run table** (gpt-oss-120b, 20 questions per cell). This replaces
the table at the top of the registered document:

| Game | Normal words | Disguised | Change | Registered as |
|---|---:|---:|---:|---|
| Vickrey auction | 100% | 90% | −10 | same |
| Cournot | 90% | 50% | −40 | same |
| **Repeated PD** | **75%** | **95%** | **+20** | 0% → 95% (+95) |
| Public goods | 95% | 90% | −5 | same |

**Consequences.**
- The registered PD prediction was written after seeing the wrong +95 figure. It stands
  as registered and will be tested as registered. The paper will say it was informed by
  an incorrect practice number.
- At 20 per cell a +20 shift is below the ~46-point detection threshold, so the
  corrected practice run no longer gives a clear PD signal either way.
- The confirmatory design (games, prompts, sample size, tests, stopping rule) is
  unchanged. The fix changes how the named-PD answer is scored, not what is asked.
- Three named-PD Stage 2 trials (gpt-oss-120b) were logged before the fix. They were
  rescored in the same way. No Stage 2 results had been analysed when this was found.

---

## 2. Gemini 3.8 Flash replaced by Gemini 3.5 Flash Lite (2026-09-30)

**Why.** Google AI Studio's free tier allows Gemini 3.8 Flash **20 requests per day**
(Rate Limit page, checked 2026-09-30). One model needs ~2,208 requests, which is ~110
days. Gemini 3.5 Flash Lite allows **500 per day** (~5 days).

**What stays the same.** The fourth model is still Google's closed model, reached the
same way. Same prompts, questions, seeds, sample size and analysis.

**What changes.** Flash Lite is a lighter tier than 3.8 Flash, so the capability spread
across the four models is somewhat different from the registered one. Predictions that
name Gemini (Section 2) are tested against Flash Lite.

**Timing.** The swap was made before any Gemini Stage 2 data existed. An 8-question
practice check confirmed Flash Lite returns usable answers (8/8 parsed).
