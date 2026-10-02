# PRACTICE ONLY: reasoning codes (not real Stage 2 data)

## Did the model name the game? (`NAMES_GAME`)

| Game | Normal | Disguised |
|---|---:|---:|
| cournot | 96% (24/25) | 12% (3/26) |
| vickrey | 96% (25/26) | 52% (13/25) |
| repeated_pd | 3% (1/29) | 7% (2/29) |
| public_goods | 4% (1/26) | 0% (0/26) |

## Why the equilibrium was missed (STRATEGIC_GAP answers)

| Game | Wording | Gaps | COLLUSIVE | DUOPOLY_FORMULA | TRUTHFUL_DEFAULT | COOPERATION_NORM | GROUP_OPTIMUM | MISMATCH | KNEW_AND_DEVIATED | UNCODED |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| cournot | disguised | 14 | 11 | 0 | 0 | 0 | 0 | 0 | 1 | 3 |
| cournot | named | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| public_goods | disguised | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 |
| public_goods | named | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| repeated_pd | disguised | 4 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 |
| repeated_pd | named | 7 | 0 | 0 | 0 | 7 | 0 | 0 | 0 | 0 |
| vickrey | disguised | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| vickrey | named | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |

## How the model reasoned (all counted answers)

| Game | Wording | Names a concept | Dominance | Best response | Backward induction |
|---|---|---:|---:|---:|---:|
| cournot | disguised | 81% (21/26) | 0% (0/26) | 38% (10/26) | 0% (0/26) |
| cournot | named | 92% (23/25) | 0% (0/25) | 60% (15/25) | 0% (0/25) |
| public_goods | disguised | 15% (4/26) | 0% (0/26) | 15% (4/26) | 0% (0/26) |
| public_goods | named | 23% (6/26) | 19% (5/26) | 4% (1/26) | 0% (0/26) |
| repeated_pd | disguised | 21% (6/29) | 52% (15/29) | 3% (1/29) | 31% (9/29) |
| repeated_pd | named | 14% (4/29) | 41% (12/29) | 0% (0/29) | 28% (8/29) |
| vickrey | disguised | 40% (10/25) | 40% (10/25) | 0% (0/25) | 0% (0/25) |
| vickrey | named | 77% (20/26) | 81% (21/26) | 0% (0/26) | 0% (0/26) |
