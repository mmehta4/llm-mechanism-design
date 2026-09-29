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
