# Stage 3.5 hand check, round 2 (codebook v2)

Fresh sample: 60 real Stage 2A answers (seed 20261003), none from round 1; 40 missed answers
coded by the author with the automatic codes hidden, choosing the first fitting code from
each game's own ordered list. Bar fixed in advance: κ < 0.6 means unreliable.

| Code | You | Computer | κ | Verdict |
|---|---:|---:|---:|---|
| Main error code, all games | 40 | 40 | **0.61** (72%) | **passes** (round 1: 0.47) |
| `COOPERATION_NORM` | 22 | 19 | **0.75** | **reliable** |
| `MISMATCH` (fraction slip) | 5 | 3 | **0.72** | **reliable** |
| `KNEW_OVERRODE` | 3 | 8 | 0.49 | **unreliable**: the rule over-counts |
| `LABEL_SWAP`, `GROUP_OPTIMUM`, `CLAIMED_NASH_WRONG`, `COLLUSIVE` | <5 | <5 | — | too few cases to judge |

By game: PD 76% agreement (n = 29), public goods 75% (n = 4), Cournot 57% (n = 7).

## Reading the 11 disagreements

- **The rule over-counts `KNEW_OVERRODE` (3):** it fires on any mention of "final round" or
  of one outcome "dominating" another (e.g. "(3,3) dominates (1,1)"), not only on answers that
  acknowledge the equilibrium argument and override it. The human coding is right here.
- **The rule under-counts `LABEL_SWAP` (3):** it catches "X dominates" and "X is dominant" but
  not "X is a strictly dominant strategy" (2), and cannot see a swap stated without any
  dominance claim ("choosing X signals a competitive stance", where X was the cooperative
  letter) (1). The human coding is right here.
- **The computer fits the definitions better in 2** (#12: the collusive quantity comes before a
  Nash claim in the fixed order; #26: no equilibrium number, so not a mismatch).
- **3 are judgement calls** (#10, #40, #59).

## Decision

No round 3. Reported in the write-up:
- `NAMES_GAME` (round 1 κ = 1.00), `COOPERATION_NORM` (κ = 0.75) and `MISMATCH` (κ = 0.72) are
  used quantitatively.
- `KNEW_OVERRODE` and `LABEL_SWAP` are reported as patterns seen in hand reading, with the
  automatic counts given only as descriptive and labelled unreliable, with the reasons above.
- The other codes are reported descriptively.
