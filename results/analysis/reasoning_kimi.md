# Stage 3.5 reasoning codes: kimi (exploratory)

## Did the model name the game? (`NAMES_GAME`)

| Game | Normal | Disguised |
|---|---:|---:|
| cournot | 97% (261/269) | 75% (205/273) |
| vickrey | 53% (144/270) | 58% (158/274) |
| repeated_pd | 2% (4/266) | 1% (4/273) |
| public_goods | 16% (43/271) | 6% (16/271) |

## Why the equilibrium was missed (STRATEGIC_GAP answers)

| Game | Wording | Gaps | COLLUSIVE | DUOPOLY_FORMULA | TRUTHFUL_DEFAULT | COOPERATION_NORM | GROUP_OPTIMUM | MISMATCH | KNEW_AND_DEVIATED | UNCODED |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| cournot | disguised | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| cournot | named | 2 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| public_goods | disguised | 8 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 6 |
| public_goods | named | 12 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 7 |
| repeated_pd | disguised | 59 | 0 | 0 | 0 | 58 | 0 | 0 | 0 | 1 |
| repeated_pd | named | 76 | 0 | 0 | 0 | 75 | 0 | 0 | 0 | 1 |
| vickrey | disguised | 6 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 |
| vickrey | named | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |

## How the model reasoned (all counted answers)

| Game | Wording | Names a concept | Dominance | Best response | Backward induction |
|---|---|---:|---:|---:|---:|
| cournot | disguised | 98% (267/273) | 0% (0/273) | 82% (224/273) | 0% (0/273) |
| cournot | named | 99% (266/269) | 0% (0/269) | 78% (211/269) | 0% (0/269) |
| public_goods | disguised | 4% (11/271) | 53% (143/271) | 0% (0/271) | 0% (0/271) |
| public_goods | named | 9% (24/271) | 48% (131/271) | 0% (0/271) | 0% (0/271) |
| repeated_pd | disguised | 6% (17/273) | 62% (168/273) | 1% (3/273) | 26% (70/273) |
| repeated_pd | named | 7% (19/266) | 50% (134/266) | 2% (4/266) | 25% (66/266) |
| vickrey | disguised | 18% (49/274) | 55% (152/274) | 0% (0/274) | 0% (0/274) |
| vickrey | named | 29% (77/270) | 53% (144/270) | 0% (0/270) | 0% (0/270) |
