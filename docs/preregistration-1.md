# Pre-registration 1 — Equilibrium or Retrieval

**Locked:** 2026-09-29 20:39 UTC, before any Stage 2 data existed.
**Scope:** the Stage 2 confirmatory experiment — four models, four games, two framings,
three paraphrases, 138 questions per game per framing per model.

The predictions below were written after a 160-question practice run on one model
(gpt-oss-120b), disclosed in Section 7. The confirmatory test uses fresh questions for all
four models, three of which had not been run at scale when this was written.

---

## What the practice run showed (gpt-oss only, 20 questions per cell)

| Game | Normal words | Disguised | Change |
|---|---:|---:|---:|
| Vickrey auction | 100% | 90% | −10 |
| Cournot | 90% | 50% | **−40** |
| Repeated PD | 0% | 95% | **+95** |
| Public goods | 95% | 90% | −5 |

*"%" = share of questions where the AI played the perfect move.*

Remember: 20 questions could only reliably spot changes of about 46 points or more. So the
Cournot and PD changes were real signals; the Vickrey and public goods ones were too small
to tell either way.

---

## 1. Your predictions — per game

For each game: when we switch to disguised words, will the AI play the perfect move
**more, less, or about the same?** Roughly how much? And — most important — **why?**
One or two sentences of reasoning each.

**Vickrey auction:**
```
Less, by a small amount — roughly −5 to −10 points (named ≈ 95%+, disguised ≈ 85–90%).

Reason: in the named version, "second-price sealed-bid" is a memorised trigger. "Bid
your true value" is the most famous fact about that format, so a model that merely
recognises the words scores without deriving anything. Disguised, the shortcut is gone
and the model must work the stated rule: overbidding never lowers the price, underbidding
can forfeit a win worth having. Most models will manage that short case analysis, but
some will fall back on the human heuristic "bid a bit above my value to be safe." The
named version is at ceiling, so the only possible direction is down — and the corrected
privacy wording should shrink the small drop the practice run hinted at.

Detectability: a drop this small is at the edge of what 138 questions per cell can see,
and is likely detected only if the named rate sits near 100%. A non-significant Vickrey
result is therefore consistent with this prediction, not a confirmation of it.
```

**Cournot:**
```
Less, by a large amount — roughly −25 to −40 points (named ≈ 85%, disguised ≈ 50–60%).

Reason: this is the most-worked example in all of economics. The numbers change every
question — the intercept is drawn between 80 and 120 — so the model cannot retrieve a
memorised answer. What it can retrieve is the method: the textbook formula
q* = (a − c)/3b. Named, the familiar words cue that formula and it is applied, not
derived. Disguised, retrieval fails and the model must differentiate (V − 10)·q, solve
the first-order condition, and impose symmetry — three algebraic steps where models
commonly slip.

Direction of mistakes: disguised deviations will be negative — under-production. The
practice run showed the failure mode: the model optimises the two players' joint
outcome, which gives the collusive quantity, instead of best-responding to a fixed
rival. This is the cleanest retrieval-vs-derivation test in the battery, and I expect
it to produce the headline positive Δλ.
```

**Repeated Prisoner's Dilemma:**
```
More, by a large amount — roughly +50 to +80 points (named ≈ 10–20% perfect moves,
disguised ≈ 85–95%).

Reason: this is the one game where the familiar words don't hand over the answer — they
pull away from it. "Cooperate" is a loaded label, and a named 10-round PD triggers folk
wisdom (tit-for-tat, be nice first) plus an aversion to choosing "defect"; the
backward-induction answer feels hostile, so models deviate from it. Disguised, the moral
frame is gone: the model reads four numbers, sees that the defecting option beats the
other whatever the opponent does, and chooses it in round 1 — which is exactly the
perfect move. The disguise doesn't hide the answer here; it removes the temptation to be
nice. If any game produces a negative Δλ, it is this one.
```

**Public goods:**
```
About the same — within ±13 points, both wordings near 90% perfect moves.

Reason: here the familiar framing and the arithmetic point the same way. "Contribute to
a common pot" is warm, but the stated rule makes the marginal return visible at a
glance (each unit routed in comes back as M/n = 0.5 < 1), and giving nothing is also
the classic free-rider answer — so both wordings land on zero contribution for any model
that reads the numbers at all. Stripping the warm words removes framing the practice
run showed gpt-oss wasn't responding to anyway.

This is my committed null, tested with an equivalence test: it is confirmed only if the
change is shown to lie within ±13 points — not merely by failing to find a difference.
```

---

## 2. Your predictions — across the four models

The real test runs four AIs from four companies. Will they all show the same pattern as
gpt-oss? Or will some behave differently — and if so, which, and why?

```
The signs replicate across all four: every model shows Cournot down, PD up, Vickrey
slightly down, public goods flat. The mechanism — training-data reminders either handing
over the answer or the method (Vickrey, Cournot), conflicting with the answer (PD), or
pointing the same way as the arithmetic (public goods) — is a property of what these
models were trained on, and all four were trained on the same famous games. If a model
reverses the Cournot sign or the PD sign, my theory is wrong, not just my magnitudes.

Three commitments on size. First, gpt-oss's −40 Cournot drop was the biggest signal in a
small sample and partly why it drew my attention, so regression toward the mean says
fresh data — including gpt-oss's own fresh run — lands closer to −15 to −25; I still
expect all four clearly negative. Second, the PD swing is largest for the most
helpfulness-tuned model: I expect Gemini to show the biggest PD swing, because its
named-version cooperate-pull should be strongest, with gpt-oss close behind and Nemotron
and Kimi intermediate. Third, a ranking: the model with the highest maths-probe pass
rate shows the smallest Cournot drop — the better it is at algebra, the less the
disguise costs it. With four models this is a ranking, not a correlation test.

Public goods stays flat for all four. One hedge: if any model over-contributes in the
named version it will be Gemini or Kimi (helpfulness framing meeting the word
"contribute"), showing up as a small negative Δλ — but I predict it stays under
13 points.
```

---

## 3. The smallest change worth detecting

This sets how many questions each AI answers. Smaller = more sensitive, but longer to run.

| Pick | Smallest change | Questions per game per wording | Total per model |
|:-:|---:|---:|---:|
| ☐ | 30 points | 43 | ~344 |
| ☐ | 20 points | 84 | ~672 |
| ☑ | **15 points — recommended** | **138** | **~1,104** |
| ☐ | 10 points | 277 | ~2,216 |

I recommend **15 points**: small enough to settle whether Vickrey and public goods really
don't move, large enough that the slowest model (Kimi, ~2¾ minutes per question) finishes
in a few days of background running.

**My pick:** `15 points`

---

## 4. The models

| Model | Company | Via |
|---|---|---|
| gpt-oss-120b | OpenAI | Groq |
| Nemotron 3 Ultra | NVIDIA | NVIDIA |
| Kimi K3 | Moonshot AI | NVIDIA |
| Gemini 3.8 Flash | Google | Google |

Qwen 3.8 27B was trialled and dropped (only 5 of 8 answers usable). Claude was
considered and dropped (requires paid API credit).

---

## 5. How the results will be judged

**Which answers count.** Every question is paired with a separate maths check (the
"probe"). An answer is **thrown out** if the AI failed the maths check, if its answer
couldn't be read, or if it answered the maths check in a sentence instead of a number.
Only answers where the AI *could* do the maths are kept — because an AI that can't do
the maths isn't making a strategic choice at all.

**The main test.** For each game and each model: compare the share of perfect moves in
normal words versus disguised words. Two-sided test. Because four games are tested, the
threshold is tightened to stay fair — Holm correction across the four games.

**The main number.** Fit the behavioural model (quantal response equilibrium) to each
game, model and wording, and compute **Δλ = λ(normal) − λ(disguised)** with a confidence
interval. This is the headline result.

**Proving a null.** Where a prediction is "no change" (public goods), a non-significant
difference is **not** accepted as evidence. The claim is tested with an equivalence test
(two one-sided tests, TOST) against a margin of ±13 points, at the same corrected threshold.
At 138 questions per cell this is the tightest margin the design can support.

**Wording check.** Each question comes in three wordings. If results move as much between
wordings as between normal-and-disguised, the disguise effect isn't real and I'll say so.

---

## 6. The rules I can't change later

**Stopping rule.** Exactly the number of questions picked in Section 3. No adding more
after looking at the results to push something over the line.

**Decision gate** (end of Stage 3). Pick one, based on the fits:
- **Fits are good and λ is stable across games** → go on to derive the mechanism.
- **Fits are good but λ varies by game** → derive the mechanism game by game.
- **Fits are poor** → the behavioural model doesn't describe AIs well; that becomes the
  finding, and Stage 4 is about why.

---

## 7. What I'm disclosing

- Predictions in Sections 1–2 were informed by a 160-question practice run on **gpt-oss-120b
  only**, results shown above. They were written after seeing those results.
- The confirmatory test uses **fresh questions** for all four models, including three
  models whose results had not been seen when these predictions were written.
- Predictions were revised once after review — Δλ signs corrected to match the definition
  in Section 5, the public goods null widened from ±10 to ±13 points to match what the
  design can prove, and the Cournot under-production direction added. All revisions were
  made before any Stage 2 data existed.
- The Vickrey disguised prompt was corrected after the practice run (it had failed to say
  that requests are private). Practice-run answers used the old wording.

---
