# Pre-registration 3 — Equilibrium or Retrieval: the extreme disguise

**Status:** DRAFT. Not locked.
**Scope:** the Stage 2C experiment — the four Stage 2A games in an extreme disguise, four
models, 138 questions per game per model: **2,208 questions**.
**Relation to earlier registrations:** pre-registration 1 (osf.io/2uqpj) and pre-registration 2
(osf.io/6hz8d) and their experiments are unchanged by this document.

---

## 0. Why a third study

Stage 2A's disguise did not hide the games from at least one model: Nemotron named the
disguised game in 96% (Cournot), 100% (Vickrey), 81% (PD) and 54% (public goods) of its
Stage 2A answers (validated code, κ = 1.00). Two reasons were found:

1. **The answer box leaked the game** in three of the four disguised questions ("bid: The
   sealed bid to submit"; "quantity to produce"; "contribution"), recorded as deviation 8.
2. **Strong models recognise the mathematics**, not only the words.

A pilot on Nemotron (practice questions only, 8 per game) tested an extreme disguise. It cut
naming of Cournot from 96% to 14% and of the PD from 81% to 50%, with maths checks still
passed, but did not hide Vickrey or public goods, whose rules are their fingerprint. (The
pilot's Vickrey prize was mistakenly worded as common knowledge; corrected here.)

Stage 2C asks: **when a game is genuinely hidden, does a model's play change?** A model that
recalls should play differently on the same question once the game is hidden; a model that
derives should not.

---

## 1. Design

**Materials** (`games/extreme.py`, three wordings per game):

| Game | Extreme disguise | Correct answer |
|---|---|---|
| Vickrey | No story. Each participant writes x; offer = 3x + 5; prize private ("known only to them"); the largest offer receives its owner's prize minus the largest other offer. | x = (prize − 5) / 3 |
| Cournot | No story. A = 2 × (your number) + 4, B likewise; score = K·A − A·A − A·B, with K = a − c of the Stage 2A question. | number = (K/3 − 4) / 2 |
| Prisoner's dilemma | No story; payoffs 2u − 4 of the Stage 2A table (+6, +2, −2, −4) shown as balance changes; 10 rounds known to both; round 1. | defect |
| Public goods | No story; asks how many points to KEEP; points not kept are pooled, multiplied by M and shared equally. | keep everything |

**Answer box:** neutral throughout. `number`, "The number you choose, as a decimal (12.25) or a
fraction (49/4)", converted to a decimal in code. A number-only box cut Nemotron's fractions at the
"/" (deviation 6), and asking for a decimal did not stop it in practice; accepting the fraction
removes the cut-off while keeping Stage 2A's order (answer first, then reasoning). **Reading rule,
fixed now:** if the box holds an equation, the number after the last "=" is read; otherwise a
plain decimal or fraction; otherwise exactly one number found in it; anything else is an
unreadable answer (PARSE_FAIL). The PD keeps its already-neutral `action` box.

**Questions:** 138 per game per model, all four Stage 2A models (gpt-oss-120b, Nemotron 3 Ultra,
Kimi K3, Gemini 3.5 Flash Lite). **Question k uses the same seed and the same wording index as
Stage 2A question k**, so every Stage 2A question now exists in three versions with identical
numbers: normal (2A), disguised (2A) and extreme (2C).

**Same rules as before:** fixed shuffled order; exactly the planned count, never more; server
refusals and empty replies re-asked; every answer saved as it arrives; maths checks in the
extreme question's own terms.

---

## 2. Predictions

Written by the project author before any Stage 2C data existed. ✏️ marks wording corrected
in review for factual accuracy; no number was changed.

**Vickrey.**
(a) Recognition ~90% (range 85–95). The rule is the fingerprint: "largest offer receives prize
minus largest offer by anyone else" is the second-price auction, and the 3x + 5 coding obscures
the surface, not the structure.
(b) Play slightly lower than in normal wording: ~80–90% vs ~95–100%, about −10 points.
(c) A model that recognises the game still has to convert (set 3x + 5 = prize), and one that
doesn't must derive winner-pays-second from scratch; both are doable, so play survives, but
conversion slips (answering the prize, or prize − 5, instead of x) cost a few points that have
nothing to do with strategy.

**Cournot.**
(a) Recognition ~25% (range 20–35). "K × A minus A × A minus A × B" has no economic word to
anchor a name to.
(b) Play clearly lower than in normal wording: ~40–50% vs ~85%, i.e. −35 to −45 points.
(c) With the game hidden, the recalled anchor "(a − c)/3b" is unavailable; the model must
optimise in A and convert back to the number. Models that derived all along lose almost
nothing; models that recalled lose the answer and must survive two algebraic steps that
✏️ *some models failed at even in Stage 2A's disguised wording*.

**Prisoner's dilemma.**
(a) Recognition ~55% (range 45–65): no moral vocabulary remains, but a known 10-round game with a
temptation/sucker table still pattern-matches for about half.
(b) ✏️ *Play: ~80–90% equilibrium (defect) in the extreme wording, above the same questions'
normal-wording rate and at or above the disguised rate.*
(c) The cooperation pull lived in the framing (C/D, "score"); the extreme wording strips it,
leaving a dominance calculation on balance changes. Models that still name the PD will defect
anyway, as in Stage 2A's disguised wording: naming is not what drives play.

**Public goods.**
(a) Recognition ~95% (range 90–100): with no story, the bare structure (shared pile, multiplied,
split equally) is the textbook public goods game.
(b) Play the same as in normal wording: ~90–95% in both, within ±5 points.
(c) The control case: the disguise fails, the game is named, nothing should move.

**Headline (Cournot, by model).** The models that play clearly worse than in normal wording will
be Nemotron and Gemini. Nemotron because it named the Stage 2A disguised game in 96% of Cournot
answers, and the extreme wording finally hides it (pilot: 14%). Gemini because ✏️ *it gives many
genuinely wrong Cournot numbers in Stage 2A (124 misses, against 11 for gpt-oss)*. gpt-oss and
Kimi should be nearly stable: their Stage 2A reasoning already contained real derivations.
**Committed drops, normal minus extreme: Nemotron ≥ 35 points, Gemini 20–35, Kimi ≤ 15,
gpt-oss ≤ 15.** Each model's gap measures how much of its normal-wording play was recall. If
Nemotron's play does not drop, it was deriving all along or re-derives faster than the disguise
hides the game; the reasoning will say which. **5–15 points of each model's Cournot and Vickrey
drop will be conversion slips** (right strategy, wrong unit), counted separately.

---

## 3. How the results will be judged

**Which answers count.** As in pre-registrations 1 and 2: maths check passed (AT_EQUILIBRIUM or
STRATEGIC_GAP). Server refusals and empty replies are re-asked, never counted.

**Pairs.** Each Stage 2C question is paired with the Stage 2A question that has the same game,
seed and wording index. A pair is used when both of its answers count.

**Main test.** For each model and game: equilibrium play, extreme (2C) vs normal (2A), on paired
questions — exact McNemar test, Holm-corrected across the four games within each model. Reported
as the paired difference (normal − extreme) with a 95% interval. Pooled across models: the
stratified McNemar (Mantel–Haenszel for matched pairs), Holm across the four games.

**Secondary.** The same comparison, extreme vs disguised (2A).

**Recognition.** `NAMES_GAME` (validated, κ = 1.00) rate, extreme vs Stage 2A disguised, on the
same paired questions — exact McNemar per model and game. Exploratory: within the extreme
wording, equilibrium play when the model named the game vs when it did not.

**Conversion slips** (counted separately, from the author's prompt review). Vickrey: answer within
0.5 of the prize, or of prize − 5 (the offer, or the offer without dividing by 3). Cournot: answer
within 0.5 of K/3 (the amount A) or of K/3 − 4 (A without dividing by 2). The main test uses the
answer as given; a secondary version treats conversion slips as their decoded answer.

**λ.** Fitted in the original action space after decoding (offer = 3x + 5; A = 2x + 4;
contribution = endowment − keep), so Vickrey, Cournot and public goods λ are on the Stage 2A
scale. The PD payoffs are doubled (2u − 4), so a Stage 2C PD λ is multiplied by 2 before any
comparison with Stage 2A (the shift does not matter; the doubling does). The decoding code is
added to the analysis lock before any Stage 2C answer is analysed.

**Limitations stated in advance.** (1) Stage 2C is asked weeks after Stage 2A, so a provider
updating a model in between would show up as a difference. (2) The PD's "balance changes"
framing (gains and losses) is a new surface, strategically inert but named here. (3) The coded
answers add a conversion step; conversion slips are counted separately for that reason.

---

## 4. The rules I can't change later

**Stopping rule.** Exactly 138 per game per model, 2,208 in total. Nothing added after results
are seen.

**Earlier registrations are not touched.** Nothing here changes pre-registrations 1 or 2.

---

## 5. What I'm disclosing

The predictions were written after seeing:
- the live board of Stage 2A and 2B results while they ran, and Nemotron's complete Stage 2A
  analysis, including its game-naming rates;
- the answer-box leak (deviation 8);
- the Nemotron pilot of the extreme disguise (8 practice questions per game), reported above;
- ✏️ *that Nemotron answered all of its early Cournot trap questions correctly (Stage 2B, before
  that block was analysed);*
- ✏️ *two hand-check sheets of 60 real Stage 2A answers each, in which the model behind each
  answer could be identified.*

No Stage 2C data had been collected. The per-model headline is written so that it can be wrong
for each model independently.

---

## 6. Materials

Code, prompts and seeds: repository commit **[SET AT LOCK]**. This file's SHA-256 is recorded in
`experiments/stage2c.py`, which refuses to collect real Stage 2C data unless this file matches it.
