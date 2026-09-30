# Pre-registration 2 — Equilibrium or Retrieval: stress tests

**Status:** DRAFT. Not locked. Waiting on the round-9 prediction and the prompt check.
**Scope:** the Stage 2B experiment: Blocks B (traps), C (number sweep), D (reasoning
effort) and E (PD endgame). 14,352 new questions across four models.
**Relation to pre-registration 1** (https://osf.io/2uqpj): a separate, second study.
Pre-registration 1 and its experiment (Block A, 4,416 questions) are unchanged by this
document.

---

## 0. Why a second study

Block A asks whether disguising a game's wording changes equilibrium play. A model that
recalls the textbook answer and one that derives it can look identical there, because in
Block A the textbook answer is also the right one.

Stage 2B asks questions Block A cannot:

- **B. Traps.** The numbers or one rule make the textbook answer **wrong**. A model that
  derives gets it right in both wordings. A model that recalls falls in more often when
  the familiar wording calls up the memorised answer.
- **C. Number sweep.** Does the framing effect survive different sizes of the same game?
- **D. Reasoning effort.** Does more thinking close the gap between wordings?
- **E. PD endgame.** Late in a finite repeated PD, after mutual cooperation, does the model
  defect as backward induction says?

---

## 1. Design

| Block | Games | Per model | Models | Total |
|---|---|---:|---|---:|
| B | 4 traps × 2 wordings × 138 | 1,104 | 4 | 4,416 |
| C | 4 games × 3 sizes × 2 wordings × 46 | 1,104 | 4 | 4,416 |
| D | Block A's 1,104 questions at low and at high effort | 2,208 | gpt-oss | 2,208 |
| E | PD rounds 5, 9, 10 × 2 wordings × 138 | 828 | 4 | 3,312 |
| | | | | **14,352** |

**Models:** gpt-oss-120b (OpenAI, via Groq), Nemotron 3 Ultra (NVIDIA), Kimi K3 (Moonshot
AI, via NVIDIA), Gemini 3.5 Flash Lite (Google). Block D uses gpt-oss-120b only, with the
provider's `reasoning_effort` set to `low` and to `high`. Block A's gpt-oss questions ran
at the provider default, `medium`, and serve as the middle level.

**The traps (Block B):**

| Trap | Change from the Block A game | Textbook answer (wrong) | Correct answer |
|---|---|---|---|
| Vickrey | Winner pays **twice** the second-highest bid | bid your value | bid half your value |
| Cournot | **Three** firms instead of two | (a − c) / 3b | (a − c) / 4b |
| Prisoner's dilemma | Payoffs R=5, T=3, S=2, P=1 (R > T and S > P) | defect | cooperate, every round |
| Public goods | Multiplier 5 with 4 players (M > n) | contribute 0 | contribute everything |

The PD and public goods traps use Block A's exact wording with new numbers. The Vickrey
trap is Block A's wording with one phrase changed ("pays TWICE the SECOND-highest"). The
Cournot trap is Block A's wording changed from one rival to two. Every trap has its own
maths check that tests the trap rule, not the ordinary one.

**Number sweep (Block C):** Vickrey with 2, 4 or 8 bidders; Cournot with demand intercept
around 60, 100 or 200; public goods with 3, 4 or 8 players (M = 2, still a dilemma);
repeated PD lasting 2, 10 or 50 rounds.

**PD endgame (Block E):** Block A's PD wording at round 5, 9 or 10 of 10, with the history
"in rounds 1 to r−1, you both chose C every time" (or the disguised label). Theory: defect
in every round, including these.

**Same rules as Block A:** fresh seeds never used before; named and disguised questions
paired on identical numbers; three wordings rotated evenly; a fixed shuffled order; every
answer saved as it arrives. Materials are fixed by the code at the commit named in
Section 7, and `tests/test_stage2a_frozen.py` proves Block A's questions were not changed
by building Stage 2B.

---

## 2. Predictions

Written by the project author before any Stage 2B data existed.

### Block B — traps

**Public goods (M > n).** More falls in normal words, but the smallest gap of the four
traps. Named recalls "public goods equilibrium = contribute nothing" and answers 0
(wrong); the warm framing pushes toward giving (right), which partially rescues it.
Disguised has no recall cue and the arithmetic is one line (5/4 = 1.25 > 1, so give
everything). **Committed: named ≈ 25–40% correct, disguised ≈ 70–85%.**

**Prisoner's dilemma (R > T and S > P).** More falls in normal words, and the named number
should be shockingly low. "Always defect" is one of the most over-learned heuristics in the
training data, and the named version lights it directly, even though the numbers now make
cooperation dominant. Disguised, X and Y carry no history; the model either compares the
columns or it doesn't. **Committed: named ≈ 15–30% correct, disguised ≈ 60–75%.**

**Cournot (3 firms).** More falls in normal words. The memorised formula (a − c)/3b happens
to contain the duopoly "3", so three firms hands the recall model a plausible, confident,
wrong answer. Disguised requires the triopoly first-order condition, one step harder than
the duopoly derivation the practice run showed models fail half the time, so disguised
stays middling. **Committed: named ≈ 15–30%, disguised ≈ 40–55%.**

**Vickrey (pay double).** More falls in normal words. "Bid your true value" is the most
famous prescription in auction theory, and the doubling is a one-word change that pattern-
matching never sees. Correct is half your value. Even disguised, this is the subtlest of
the four: the dominance argument has to be re-run against a changed rule. **Committed:
named ≈ 20–35%, disguised ≈ 50–65%.**

**Most-caught trap:** Vickrey pay-double, across both wordings. Recall fails it in the
normal wording and pure reading fails it in the disguised one.

**Design notes from the author.** (1) The public goods trap is the weakest by design: in
the named wording the recalled answer (give nothing, wrong) conflicts with the warm framing
(giving is good, right), so its gap should be attenuated. (2) The cleanest traps are
Cournot and Vickrey, where nothing opposes the recall.

### Block C — number sweep

The gap between wordings stays roughly constant across sizes for Vickrey, Cournot and
public goods: the recall cue lives in the words, not the numbers. The exception is the
repeated PD: a long named game starts to feel like the indefinite-horizon case where
cooperation is legitimate, so named cooperation rises with length and **the PD gap is
clearly larger at 50 rounds than at 10.**

### Block D — reasoning effort

The gap shrinks steadily as effort rises: widest at low, narrowest at high. At low effort
the model leans on pattern-matching, so normal words keep scoring by recall while
disguised collapses. At high effort it can carry out the derivation without lexical cues,
most of all for Cournot, the only game whose disguised failure is genuinely algebraic.
**Committed: high effort does not fully close the gap, but cuts it by half or more
compared with low effort.** If the gap is identical at all three settings, extra thinking
isn't reaching the derivation, which would refute the "lazy recaller" account.

### Block E — PD endgame

Disguised models mostly defect, as at round 1: dominance reasoning doesn't change with
history. Named models show a weak human-style endgame effect.

| Round | Named, % defect | Disguised, % defect |
|---|---|---|
| 5 | 30–40 | 80–85 |
| 9 | **[TO BE FILLED]** | **[TO BE FILLED]** |
| 10 | 55–65 | 85–90 |

If named models defect in round 10 at near-theory rates, their named-version cooperation
was strategic calculation after all, not warmth. The author considers that the most
surprising single result Stage 2B could produce.

---

## 3. How the results will be judged

**Which answers count.** As in pre-registration 1: an answer is kept only if the model
passed that question's maths check, its answer was readable, and the check was answered
as a number or a single label. Server refusals (the model never saw the question) are
re-asked, never counted.

**Block B, main test.** For each trap: share of correct answers, normal vs disguised,
pooled over the four models with a Cochran–Mantel–Haenszel test stratified by model.
Holm correction across the four traps. Per-model two-proportion tests are reported as
secondary.

**Block B, recall signature.** For each trap, the share of answers equal to the textbook
answer (Vickrey: within 0.5 of the value; Cournot: within 0.5 of (a − c)/3b; PD: defect;
public goods: 0), normal vs disguised. Recall predicts more textbook answers in normal
words.

**Block C.** For each game: logistic regression of correct ~ wording × size, with model
as a fixed effect. The test is the wording × size interaction, Holm-corrected across the
four games. Prediction: no interaction for Vickrey, Cournot and public goods; a positive
one for the PD (named cooperation rising with length).

**Block D.** Logistic regression of correct ~ wording × effort (low, medium, high as an
ordered variable), gpt-oss only, using Block A's gpt-oss answers as the medium level. The
test is the interaction. Following the author's note, maths-check pass rates are reported
for each effort level beside every comparison, so a collapse in usable answers at low
effort cannot pass for a narrowing gap.

**Block E.** Defection rate by round and wording. Normal vs disguised at each round,
Holm-corrected across the three rounds; within each wording, the trend across rounds 5,
9 and 10.

**Wording check.** As in pre-registration 1: if results move as much between the three
wordings as between normal and disguised, the disguise effect isn't real.

---

## 4. The rules I can't change later

**Stopping rule.** Exactly the numbers in Section 1. Nothing added after results are seen.

**Block A is not touched.** Nothing in Stage 2B changes pre-registration 1, its questions
or its analysis.

---

## 5. What I'm disclosing

- These predictions were written after the Stage 1 practice run (gpt-oss, 160 questions)
  and while Block A was running. A live dashboard showed Block A's early answers (a few
  hundred questions per model at most) when the predictions were written. No Block A
  analysis had been done.
- A Stage 2B practice round (gpt-oss, 47 questions, separate seeds, never analysed) ran
  **after** the Block B–E predictions above were written, to catch bugs. Its results were
  shown to the author after the predictions were final.
- One design error was corrected before registration: the PD trap first specified
  "R > T" alone, which does not make cooperation dominant. Built and registered as R > T
  and S > P.
- The fourth model is Gemini 3.5 Flash Lite, not Gemini 3.8 Flash, for the free-tier
  reason recorded in `docs/deviations-from-preregistration.md`.

---

## 6. Timeline

Free-tier limits set the pace: Groq 1,000 requests a day, Google 500 a day, NVIDIA's
models about 3–6 minutes a question. Expected completion about three weeks after
registration.

---

## 7. Materials

Code, prompts and seeds: repository commit **[SET AT LOCK]**.
This file's SHA-256 is recorded in `experiments/stage2b.py`, which refuses to collect real
Stage 2B data unless this file matches it.
