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

---

## 3. Empty replies are re-asked, not scored as unreadable (2026-09-30)

**Applies to:** both pre-registrations (Stage 2A and Stage 2B).

**What was found.** NVIDIA's Kimi K3 endpoint sometimes returns a reply with **no text
at all**: its reasoning is a burst of "!!!!" and the answer is empty. Re-asking the
identical question three times gave two normal answers and one more empty reply, so it
is random and comes from the serving stack, not from the question.

**Registered rule it touches.** Unreadable answers (PARSE_FAIL) are "a fact about the
model, reported as a rate, never dropped"; server refusals are re-asked.

**Decision.** A reply with no text in it is not an answer, so it is treated like a
server refusal: re-asked, never scored. A reply that has any text but doesn't fit the
answer format is still the model's, and stays PARSE_FAIL exactly as registered. The rule
depends only on whether the reply is empty, never on what the answer would have been.

**Affected rows.** 4 Kimi rows (3 in Stage 2A, 1 in Stage 2B), relabelled with
`analysis/relabel_empty_replies.py`; the original rows stay in the files as the audit
trail. No other model has returned an empty reply. The count of empty replies per model
will be reported in the paper.

## 4. Practical note: gpt-oss daily token cap (2026-09-30)

Not a deviation, recorded for the timeline. Groq's free tier limits gpt-oss-120b to
200,000 tokens a day, about 170 questions. Every planned question is still asked; it
just takes longer (gpt-oss finishes around early November 2026). Its Stage 2B blocks run
in the order B, C, E, D so the traps finish first. Block order does not change any
question or analysis.

## 5. Scoring correction: NVIDIA access outage (2026-09-30 19:22–19:32 UTC)

Not a deviation from either plan; a correction of a scoring error, recorded for the audit.

For about ten minutes NVIDIA refused every request with "403 Authorization failed". The
code did not yet classify 403 as a server refusal, so 4,454 refused requests across Kimi
and Nemotron were scored as unreadable answers in a fraction of a second each, which made
several blocks look complete. The models never saw those questions.

They were relabelled INFRA_FAIL with `analysis/relabel_outage_403.py` and are re-asked
under the registered rule for server refusals. Genuine maths-check format failures from
before the outage (replies taking 5–25 seconds) were left exactly as they were. Since
then, any failure that happens before a reply arrives is classified as infrastructure,
and an access refusal pauses the run instead of racing through the plan.

## 6. Observation and exploratory addition: Nemotron's "fraction slip" (2026-10-02)

Not a deviation: the confirmatory analysis is run and reported exactly as locked. Recorded
because it changes how one number should be read.

**What was seen** (Nemotron's Stage 2A analysis, the first real result): 31 of its 276
counted Cournot answers (11%) are exactly 3× or 6× the equilibrium. In every one, the
written reasoning reaches the correct answer as a fraction ("q = 70/3 ≈ 23.33",
"157/6 ≈ 26.17"), but the answer field holds the numerator (70, 157). The answer field
only accepts a plain number, and the fraction was cut at the "/". No other model shows
this in Stage 2A, and Nemotron does not show it in the Cournot trap.

**What it does to the results.**
- *Main test (share at equilibrium):* scored as registered — the answer field is the
  answer. The slip hits both wordings about equally (normal 90%, disguised 88%), so the
  conclusion of no disguise effect is unaffected.
- *λ for Nemotron's Cournot cells:* the logit model reads a jump to 3× the equilibrium as
  an enormously costly strategic error, so λ is pulled to the bottom of the grid. For this
  cell, λ measures the slip rate, not strategic precision. It is reported with that note.

**Exploratory addition, defined before any other model's Stage 2A analysis.** For every
model, λ will also be reported with answers excluded where the answer field disagrees
with the final number stated in the model's own reasoning. This is labelled exploratory
in the paper; the confirmatory numbers are the locked ones. Stage 3.5's reasoning
checklist gets a matching code (answer–reasoning mismatch).

**Also seen, for Stage 3.5:** in the disguised wording Nemotron often writes "This is a
Cournot duopoly game", i.e. it recognised the disguised game. Recognition rates will be
measured for every model by the Stage 3.5 checklist.

## 7. Block D (reasoning effort) dropped before data collection (2026-10-02)

**Applies to:** pre-registration 2 (osf.io/6hz8d), Block D.

**What changed.** Block D — gpt-oss-120b answering the 1,104 Stage 2A questions again at low
and at high reasoning effort (2,208 questions) — was dropped. **No Block D data was ever
collected**: gpt-oss was still on Stage 2A, and Block D was last in its queue.

**Why.** So that all four models answer exactly the same set of questions (4,140 each),
which the author judged better for the comparison across models. It also shortens
gpt-oss's run by about 13 days under Groq's free-tier cap.

**Consequences.**
- The Block D prediction in pre-registration 2 (high effort cuts the normal-vs-disguised
  gap by half or more) is **not tested**, and the paper will say so.
- No other block, prediction, sample size or analysis changes. The locked Stage 2B analysis
  code for Block D is left in place, unused.
- Stage 2 totals: 16,560 questions (Stage 2A 4,416 + Stage 2B 12,144), down from 18,768.
