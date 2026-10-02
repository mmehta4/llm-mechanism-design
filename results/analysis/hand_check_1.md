# Stage 3.5 hand check, round 1 (2026-10-02)

Sample: 60 real Stage 2A answers (seed 20261002; 15 per model, half each wording, gaps
over-sampled), coded by the author from the reasoning text with the automatic codes hidden.
Rule fixed in advance (docs/reasoning-codebook.md §4): a code with κ < 0.6 is reported as
unreliable rather than interpreted.

| Code | n | Agreement | Cohen's κ | Verdict |
|---|---:|---:|---:|---|
| `NAMES_GAME` (all 60 answers) | 60 | 100% | 1.00 | **reliable** |
| Error code, all categories (strategic gaps) | 32 | 66% | 0.47 | below 0.6: **not reliable as a breakdown** |
| `COOPERATION_NORM` present / absent | 32 | 81% | 0.63 | **reliable** |
| Other error codes (COLLUSIVE, MISMATCH, KNEW_AND_DEVIATED, GROUP_OPTIMUM, UNCODED) | — | — | — | too few cases, disagreements: **not reliable** |

## Where the 11 disagreements came from

- **8 were codes applied outside the games they are defined for** (the codebook restricts
  COLLUSIVE, MISMATCH and KNEW_AND_DEVIATED to Cournot): KNEW_AND_DEVIATED ×4, COLLUSIVE ×2
  and MISMATCH ×2 given to prisoner's dilemma answers. The guide did not state the
  restriction prominently enough.
- **They nonetheless point at real patterns the codebook lacks:**
  - *PD, knew and overrode:* answers that cite backward induction or dominance and then
    cooperate anyway (#1, #14, #25, #33). Partly visible already as COOPERATION_NORM together
    with the BACKWARD_INDUCTION method code.
  - *PD, swapped labels:* answers claiming the chosen letter "dominates" when, in that
    question's counterbalanced table, it is the cooperative one (#9, #42) — the model misread
    which letter was which.
  - *Cournot, claimed Nash with the wrong number:* answers stating they give the Cournot–Nash
    quantity while giving a different number, with no equilibrium value written (#26, #36).
- **1 case the automatic code fits the definition better** (#57: symmetric substitution
  before differentiating, coded COLLUSIVE).

## Consequence

- `NAMES_GAME` and `COOPERATION_NORM` are used in the write-up.
- The other error codes are reported only as a descriptive table, labelled unreliable.
- A round-2 check is possible with a clarified codebook (version 2: game restrictions stated
  per code; new codes for swapped labels and wrong-number Nash claims), locked before a
  **fresh** sample that excludes these 60 answers. Round 1 stays reported as it is.
