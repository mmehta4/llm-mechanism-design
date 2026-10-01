# OSF registration — paste-ready text

Everything you need to fill in on OSF. Copy each block into the matching box.

---

## Project title

```
Equilibrium or Retrieval: Do LLM Agents Derive or Recall Game-Theoretic Equilibria?
```

## Project description

```
Tests whether large language models play games with known equilibria because they
derive the answer or because they recognise a familiar game. Four games (Vickrey
auction, Cournot duopoly, finitely repeated Prisoner's Dilemma, public goods) are
posed in two framings with identical payoff mathematics -- standard vocabulary and
disguised vocabulary -- to four models from four companies.
```

## Registration template to choose

**Open-Ended Registration** — the simplest template: one summary box plus the attached file.

## Summary box (the one question the template asks)

```
Pre-registration for the Stage 2 confirmatory experiment, written before any Stage 2
data existed.

Design: 4 games x 2 framings (standard / disguised) x 3 paraphrases x 4 models
(gpt-oss-120b, Nemotron 3 Ultra, Kimi K3, Gemini). 138 questions per game per framing
per model, fixed in advance by a power analysis for a 15-percentage-point effect
(80% power, Holm-corrected across four games).

Primary test: two-proportion comparison of equilibrium play, standard vs disguised.
Headline measure: delta-lambda = lambda(standard) - lambda(disguised), from quantal
response equilibrium fits. The one predicted null (public goods) is tested by an
equivalence test at +/-13 points.

Predictions per game and across models, exclusion rules, stopping rule and decision
gate are in the attached file. Predictions were informed by a 160-question practice
run on gpt-oss-120b only, and this is disclosed in Section 7 of the file.

Attached file: preregistration-1.md
SHA-256: a70cf95ace715646b5ef000845ab56cc2289d00c267878c2c1943f4643a78a40
Matches git commit 54cdfe6 in the project repository.
```

## Embargo

Choose **embargo** and pick a date about a year out. You can make it public early at any
time — for example, the day the paper goes on arXiv. While embargoed, nobody can read it,
but the registration date is fixed and counts.

---

## Why the SHA-256 line matters

It's a fingerprint of the exact file. Anyone can later check that the file in your repo is
byte-for-byte the one you registered — change one character and the fingerprint changes.
That ties the OSF record to the code.

## Registered

- **OSF registration:** https://osf.io/2uqpj
- **Submitted:** 2026-09-29 (UTC)
- **Status at submission:** embargoed (private) until **2027-09-30**, then public automatically.
  OSF asks project admins to approve the embargo by email; if nobody acts, it is approved automatically after 48 hours.
- **Registered file:** `docs/preregistration-1.md`, SHA-256
  `a70cf95ace715646b5ef000845ab56cc2289d00c267878c2c1943f4643a78a40` (commit 54cdfe6).
  Do not edit that file: the fingerprint is the proof that the plan came before the data.

---

# Registration 2 — Stage 2B stress tests

## Title

```
Equilibrium or Retrieval 2: Trap Games, Number Sweeps, Reasoning Effort and the Prisoner's Dilemma Endgame
```

## Description

```
Second pre-registered study in the Equilibrium or Retrieval project (first: osf.io/2uqpj).
Tests whether large language models derive game-theoretic equilibria or recall them,
using "trap" versions of four classic games in which the textbook answer is wrong, plus
a sweep of game sizes, a reasoning-effort manipulation and late rounds of a finitely
repeated Prisoner's Dilemma. Each game is posed in standard and disguised wording with
identical payoff mathematics, to four models from four companies.
```

## Summary box

```
Pre-registration 2 (Stage 2B), written before any Stage 2B data existed. A separate,
second study; pre-registration 1 (osf.io/2uqpj) and its experiment are unchanged.

Design, 14,352 questions:
B. Traps (4 models x 4 traps x 2 wordings x 138): Vickrey where the winner pays twice the
   second-highest bid; Cournot with three firms; a harmony-game PD (R=5, T=3, S=2, P=1);
   public goods with multiplier 5 and 4 players. The textbook answer is wrong in each.
C. Number sweep (4 models x 4 games x 3 sizes x 2 wordings x 46).
D. Reasoning effort (gpt-oss-120b at low and high effort on the 1,104 Stage 2A questions).
E. PD endgame (4 models x rounds 5, 9, 10 of 10 after mutual cooperation x 2 wordings x 138).
Models: gpt-oss-120b, Nemotron 3 Ultra, Kimi K3, Gemini 3.5 Flash Lite.

Key prediction: in the traps, models fall for the textbook answer more often in standard
wording than in disguised wording. Tests: Cochran-Mantel-Haenszel across models per trap,
Holm-corrected; interactions by logistic regression for Blocks C and D; per-round
comparisons for Block E. All predictions, exclusion rules and the stopping rule are in
the attached file, with disclosures in Section 5.

Attached file: preregistration-2.md
SHA-256: ad378d9158fca7872babc3f024783d98e645c5dd2bb8eb4e26095a4705a9dfc0
Locked in git commit 2a71eda; materials at commit d3ef924.
```

## Registered (registration 2)

- **OSF registration:** https://osf.io/6hz8d
- **Submitted:** 2026-09-30 08:44:43 UTC, before any Stage 2B data existed.
- **Status at submission:** embargoed (private) until **2027-09-30**, then public automatically.
- **Registered file:** `docs/preregistration-2.md`, SHA-256
  `ad378d9158fca7872babc3f024783d98e645c5dd2bb8eb4e26095a4705a9dfc0` (lock commit 2a71eda).
  OSF's own hash of the uploaded file matches.
