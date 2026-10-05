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

## 8. Limitation found: the answer box carried the named game's words (2026-10-02)

Not a change to either plan; a flaw in the materials, recorded so results are read
correctly.

**What was found.** Each answer is returned through a form whose field names and
descriptions the model sees, and writes, as it answers. For three games the same form was
used for both wordings, and it uses the **named** game's vocabulary:

| Game | Field the model sees in the DISGUISED question |
|---|---|
| Vickrey (and its trap and sweep) | `bid` — "The sealed bid to submit." |
| Cournot (and its trap and sweep) | `quantity` — "The quantity to produce." |
| Public goods (and its trap and sweep) | `contribution` — "How much of your endowment to contribute." |
| Prisoner's dilemma | `action` — "The option chosen" (neutral: not affected) |

So in Stage 2A and Stage 2B the disguised Vickrey, Cournot and public goods questions were
less disguised than intended. Found while designing the Stage 2C pilot; not caught by the
Stage 0 isomorphism checks, which compared prompt texts only.

**What it means.**
- Registered results are reported exactly as collected; nothing is rescored.
- The disguise comparison for Vickrey, Cournot and public goods is a comparison between the
  named wording and a *partly* disguised one. The prisoner's dilemma disguise is clean.
- Recognition rates in disguised questions (Stage 3.5 `NAMES_GAME`) may be inflated for those
  three games. Nemotron still named the clean PD disguise in 81% of answers, so the box is
  not the whole story.
- The Stage 2C pilot measures the box's effect directly: the Stage 2A disguised wording,
  word for word, asked with a neutral `number` box. Stage 2C itself uses neutral boxes
  throughout.

## 9. Ten answers re-asked that should have been scored (2026-10-03)

Not a change to either plan; a classification error, recorded for the audit.

After the NVIDIA outage (item 5), any failure before a usable reply was classified as
infrastructure and re-asked. That rule was too broad: a reply that **arrives but fails the
answer-format check** is the model's own unreadable answer, which the registrations score
(PARSE_FAIL for the move, PROBE_FORMAT_FAIL for the maths check) rather than re-ask.

**Affected:** 1 Kimi Stage 2A answer (a format-check failure, re-asked and then answered),
and 9 Nemotron questions (2 in Stage 2A, 7 in Stage 2B traps) where the maths-check call
failed without its error being recorded, so it cannot be told whether they were format
failures or genuine server errors. About 10 of roughly 10,000 questions; no result can
change. The answers obtained on re-asking stand, and these cases are listed in the paper.

**Fixed:** a format-check failure is now always the model's answer (`agents/llm.py`), with a
test. Found while practising Stage 2C's new answer box, which made such replies common.

## 10. Limitation: explanatory text sent with two answer forms (2026-10-03)

Not a change to either plan; recorded so results are read correctly.

The answer forms are sent to the model as a schema, and a code comment written as a
class docstring is sent with it as the schema's description. Two Stage 2A/2B forms had one:

- **PD answer form** (both wordings): "Labels are counterbalanced per trial, so this cannot be
  a static Literal. Validate the returned string against the trial's own two labels."
- **Maths-check form for the PD** (both wordings): a note that mentions "setting Y would give
  you more" and answer formatting.

Both reveal that the question is part of an experiment, and the second contains a phrase from
the disguised PD's vocabulary. Both are **identical in the named and disguised wordings**, so
they cannot create a difference between wordings, and neither names the game. The other forms
(Vickrey, Cournot, public goods, numeric maths checks) send no such text.

**Also affected: the Stage 2C pilot.** The first neutral answer box used in the pilot had a
docstring quoting the Stage 2A field texts ("bid: The sealed bid to submit", "quantity to
produce", "contribution"), so every pilot deep-disguise question carried those words. The
pilot's recognition rates (e.g. 100% for the extreme Vickrey and public goods) are therefore
likely overstated; Cournot's fall from 96% to 14% happened despite the leak. Found by a test
written before Stage 2C's registration; the Stage 2C box sends no description at all.

## 11. gpt-oss-120b's Stage 2B blocks served by a second provider (recorded 2026-10-06, before any affected data)

**A change to where one model is served, not to the design.** Pre-registration 2 lists
gpt-oss-120b "via Groq". Groq's free tier allows about 155 gpt-oss questions a day, which would
push the end of collection to about 1 November. gpt-oss-120b is an open-weights model, and
Cerebras serves the same weights, with a free tier of about 1 million tokens a day.

**What moves:** only gpt-oss-120b's Stage 2B blocks (B traps, C sweep, E endgame).

**What stays on Groq:** gpt-oss-120b's Stage 2A, Stage 2C and Stage 5. Stage 2C and Stage 5
are compared question by question with Stage 2A, so they must share a provider.

**Why the 2B comparisons are unaffected:** every Stage 2B test compares named with disguised
wording *within* a block, and each block is served entirely by one provider.

**Settings:** `reasoning_effort` is pinned to `medium` on Cerebras (Groq's default, used for
everything else).

**Record:** every row records `model_api_id`. Groq rows read `openai/gpt-oss-120b`; Cerebras
rows read `gpt-oss-120b`.

**Not yet done when this was written:** no gpt-oss Stage 2B question had been asked on either
provider. A practice check on non-registered seeds confirms that answers fit Cerebras's
free-tier context cap before any registered question is sent.

**Limitation:** two providers may serve the same weights with different numerical precision or
inference stacks. The paper reports gpt-oss's Stage 2B results with this caveat.

**Not done:** additional accounts on any provider to multiply free quotas. This was considered
and rejected, because it breaks the providers' terms.
