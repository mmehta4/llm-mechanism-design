# Reasoning codebook — version 2 (Stage 3.5)

**Why a version 2.** Round 1 of the hand check (`results/analysis/hand_check_1.md`)
validated `NAMES_GAME` (κ = 1.00) and `COOPERATION_NORM` (κ = 0.63) but not the error
breakdown (κ = 0.47). Eight of the eleven disagreements were codes used outside the games
they apply to, and the human coder found three patterns the codebook lacked. Version 2
fixes both. Version 1 and its round-1 result stay on record unchanged.

**Disclosure.** Version 2's new codes come from reading round-1 disagreements, which were
real Stage 2 answers. They are validated on a **fresh** sample that excludes every round-1
answer.

**Locked:** 2026-10-01 23:14 UTC, before the round-2 sample was drawn.

**Status.** Exploratory, as version 1. Recognition codes (`NAMES_GAME`, `NAMES_CONCEPT`) and
method codes are unchanged from version 1.

---

## 1. One main error code per missed answer, chosen in a fixed order

Each STRATEGIC_GAP answer gets exactly **one** main error code: the first in its game's
list that fits. The hand coder uses the same list in the same order.

### Cournot (including the trap and the sweep)

| Order | Code | Fits when |
|---|---|---|
| 1 | `MISMATCH` | The **last** number in the reasoning is the equilibrium (within 0.5) but the answer is not: concluded right, wrote something else (e.g. a fraction cut at "/"). |
| 2 | `KNEW_AND_DEVIATED` | The equilibrium appears in the reasoning but is not the last number, and the answer is elsewhere: derived it, then chose otherwise. |
| 3 | `DUOPOLY_FORMULA` | Trap only: answer within 0.5 of (a − c)/3b with three firms. |
| 4 | `COLLUSIVE` | Answer within 0.5 of the joint-profit share (a − c)/(2·n·b): assumed the rival does the same and optimised both together. |
| 5 | `CLAIMED_NASH_WRONG` | *(new)* The reasoning says its answer is the Nash / equilibrium quantity, but the number is wrong and the equilibrium never appears. |
| 6 | `UNCODED` | None of the above. |

### Vickrey (including the trap and the sweep)

| Order | Code | Fits when |
|---|---|---|
| 1 | `TRUTHFUL_DEFAULT` | Trap only: bid within 0.5 of the value, ignoring the doubled payment. |
| 2 | `UNCODED` | None of the above. |

### Prisoner's dilemma (all versions)

| Order | Code | Fits when |
|---|---|---|
| 1 | `LABEL_SWAP` | *(new)* The reasoning says the option it **chose** is the dominant one, when in that question's table it is the cooperative one: it misread which letter is which. |
| 2 | `KNEW_OVERRODE` | *(new)* Chose to cooperate while acknowledging the equilibrium argument: mentions backward induction, or that defecting is dominant / rational. |
| 3 | `COOPERATION_NORM` | Chose to cooperate citing trust, mutual benefit, reciprocity, signalling or establishing cooperation. |
| 4 | `UNCODED` | None of the above. |

### Public goods (all versions)

| Order | Code | Fits when |
|---|---|---|
| 1 | `GROUP_OPTIMUM` | Contributed more than the equilibrium, appealing to the group: everyone, all players, collective, group, total payoff, social. |
| 2 | `UNCODED` | None of the above. |

## 2. Hand check, round 2

- **Fresh sample:** 60 real Stage 2A answers, seed 20261003, **excluding every round-1
  answer**; 15 per model; 10 of each 15 are missed answers (STRATEGIC_GAP) so each code has
  enough cases.
- The sheet lists, under each answer, **only that game's codes in order**.
- Reported: κ on the main error code within each game family, and yes/no κ for every code
  with at least 5 cases in either coding. Same bar as round 1: κ < 0.6 means a code is
  reported as unreliable.
