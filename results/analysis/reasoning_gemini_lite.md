# Stage 3.5 reasoning codes: gemini_lite (exploratory)

## Did the model name the game? (`NAMES_GAME`)

| Game | Normal | Disguised |
|---|---:|---:|
| cournot | 100% (137/137) | 69% (95/138) |
| vickrey | 100% (138/138) | 85% (17/20) |
| repeated_pd | 89% (123/138) | 32% (47/146) |
| public_goods | 81% (128/159) | 54% (84/156) |

## Why the equilibrium was missed (STRATEGIC_GAP answers)

| Game | Wording | Gaps | COLLUSIVE | DUOPOLY_FORMULA | TRUTHFUL_DEFAULT | COOPERATION_NORM | GROUP_OPTIMUM | MISMATCH | KNEW_AND_DEVIATED | UNCODED |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| cournot | disguised | 132 | 37 | 0 | 0 | 0 | 0 | 3 | 12 | 86 |
| cournot | named | 5 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 4 |
| public_goods | disguised | 33 | 0 | 0 | 0 | 0 | 20 | 0 | 0 | 13 |
| public_goods | named | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 |
| repeated_pd | disguised | 41 | 0 | 0 | 0 | 37 | 0 | 0 | 0 | 4 |
| repeated_pd | named | 126 | 0 | 0 | 0 | 126 | 0 | 0 | 0 | 0 |
| vickrey | disguised | 4 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 1 |

## How the model reasoned (all counted answers)

| Game | Wording | Names a concept | Dominance | Best response | Backward induction |
|---|---|---:|---:|---:|---:|
| cournot | disguised | 55% (76/138) | 0% (0/138) | 34% (47/138) | 0% (0/138) |
| cournot | named | 91% (125/137) | 0% (0/137) | 50% (69/137) | 0% (0/137) |
| public_goods | disguised | 64% (100/156) | 65% (101/156) | 0% (0/156) | 0% (0/156) |
| public_goods | named | 92% (146/159) | 92% (147/159) | 0% (0/159) | 0% (0/159) |
| repeated_pd | disguised | 4% (6/146) | 3% (4/146) | 0% (0/146) | 0% (0/146) |
| repeated_pd | named | 0% (0/138) | 1% (1/138) | 0% (0/138) | 0% (0/138) |
| vickrey | disguised | 40% (8/20) | 30% (6/20) | 0% (0/20) | 0% (0/20) |
| vickrey | named | 75% (103/138) | 75% (104/138) | 0% (0/138) | 0% (0/138) |
