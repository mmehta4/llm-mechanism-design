# Reasoning codebook — Stage 3.5

**Purpose.** Stage 2 records *what* each model played. This codebook classifies *why*,
from the short reasoning each answer comes with, using fixed rules a computer applies
identically to every answer (`analysis/reasoning.py`). The rules are fingerprinted before
they are applied to any real Stage 2 reasoning, and a random sample is checked by hand
(Section 4) to show the automatic coding agrees with a human reader.

**Locked:** 2026-10-01 23:02 UTC, before the rules were applied to any real Stage 2 reasoning.

**Status.** Exploratory. Neither pre-registration makes predictions about reasoning, so
nothing here is a confirmatory test. Rates are reported as description.

**How the rules were built.** From the practice runs only (Stage 1 pilot, 160 answers;
Stage 2B practice round, 47; the per-model pilot checks): 235 answers with reasoning.
**Disclosure:** two real Stage 2 observations were seen before the rules were finalised,
while inspecting Nemotron's first analysis: its fraction slip (code `MISMATCH`), and its
naming of the disguised Cournot game (code `NAMES_GAME`). Both codes would have been
included anyway, but they were not designed blind to real data.

---

## 1. Recognition codes (every answer)

| Code | Rule | Why it matters |
|---|---|---|
| `NAMES_GAME` | The reasoning uses a name for the game's textbook form **that is not in the question itself**: Cournot / duopoly / oligopoly / triopoly; Vickrey / second-price / auction; prisoner's dilemma; public good(s) / free-ride / commons. | Direct evidence the model recognised the game. In the **disguised** wording this means the disguise failed to hide it. |
| `NAMES_CONCEPT` | The reasoning uses an equilibrium concept: "Nash", "equilibrium", "dominant strategy", "best response". | The model frames the problem as a game-theory exercise. |

`NAMES_GAME` checks against the question text, so naming "auction" in the normal Vickrey
question (where the question says "auction") does **not** count; naming it in the
disguised question does.

## 2. Method codes (every answer)

| Code | Rule |
|---|---|
| `DOMINANCE` | Argues from dominance: "dominant", "dominates", "regardless of what the other…", "whatever the other…". |
| `BEST_RESPONSE` | Derives a best response: "best response", "reaction function", or solves a first-order condition ("derivative", "maximiz… with respect to"). |
| `BACKWARD_INDUCTION` | "backward induction", "last round", "final round", "unravel". |

## 3. Error codes (answers that missed the equilibrium: STRATEGIC_GAP)

| Code | Game | Rule | The mistake |
|---|---|---|---|
| `COLLUSIVE` | Cournot | Answer within 0.5 of the joint-profit-maximising share, (a − c) / (2·n·b), where n = number of firms. | Optimised what is best for **both together**, assuming the rival does the same, instead of best-responding. |
| `DUOPOLY_FORMULA` | Cournot trap | Answer within 0.5 of (a − c) / 3b with three firms. | Reused the memorised two-firm formula. |
| `TRUTHFUL_DEFAULT` | Vickrey trap | Answer within 0.5 of the item's value. | Bid the value, the textbook rule, ignoring the doubled payment. |
| `COOPERATION_NORM` | PD | Chose the cooperative action **and** the reasoning mentions trust, mutual benefit, reciprocity, signalling, or establishing cooperation. | A social script overriding the payoff table. |
| `GROUP_OPTIMUM` | Public goods | Contributed more than the equilibrium **and** the reasoning appeals to the group: "everyone", "all players", "collective", "group", "total payoff", "social". | Optimised for the group, not for itself. |
| `MISMATCH` | Cournot | The **last** number in the reasoning is the equilibrium (within 0.5), but the answer field is more than 0.5 away. | Concluded at the right answer but wrote a different number (e.g. a fraction cut at "/"). |
| `KNEW_AND_DEVIATED` | Cournot | The equilibrium appears in the reasoning (within 0.5) but is **not** the last number, and the answer is elsewhere. | Derived the equilibrium, then deliberately chose something else. |
| `UNCODED` | any | A STRATEGIC_GAP matching none of the above. | Reported as a share; read by hand in the write-up. |

An answer can carry several codes (e.g. `NAMES_GAME` and `COLLUSIVE`).

*Why only Cournot for the last two:* in Vickrey and public goods the equilibrium is a number
already given in the question (the value; 0 or the endowment), so the reasoning mentioning
it shows nothing. The first practice draft applied the rule to every numeric game and got
three false alarms of exactly that kind; it was narrowed before the lock.

## 4. Hand check (inter-rater agreement)

After the rules are locked, a random sample of **60 real answers** (seed 20261002,
stratified: 15 per model, half normal and half disguised, gaps over-sampled so error codes
appear) is printed **without** the automatic codes. The author codes each by reading it,
using the definitions above. Agreement with the automatic codes is reported as Cohen's κ
for `NAMES_GAME` and for the error code, plus the raw percentage agreement. If κ < 0.6 for
a code, that code is reported as unreliable rather than interpreted.

## 5. What is reported

- `NAMES_GAME` rate by model × game × wording. The key number: how often each model names
  the disguised game.
- Among STRATEGIC_GAP answers: the share of each error code, by model × game × wording.
- `MISMATCH` rate per model (feeds the exploratory λ in deviation 6).
- Method code rates, normal vs disguised.
