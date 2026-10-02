# nemotron · Stage 2A · reasoning codes (exploratory)

## Did the model name the game? (`NAMES_GAME`)

| Game | Normal | Disguised |
|---|---:|---:|
| cournot | 100% (138/138) | 96% (133/138) |
| vickrey | 100% (138/138) | 100% (138/138) |
| repeated_pd | 87% (119/137) | 81% (111/137) |
| public_goods | 98% (133/136) | 54% (74/138) |

## Why the equilibrium was missed (STRATEGIC_GAP answers)

| Game | Wording | Gaps | COLLUSIVE | DUOPOLY_FORMULA | TRUTHFUL_DEFAULT | COOPERATION_NORM | GROUP_OPTIMUM | MISMATCH | KNEW_AND_DEVIATED | UNCODED |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| cournot | disguised | 17 | 0 | 0 | 0 | 0 | 0 | 14 | 3 | 0 |
| cournot | named | 14 | 0 | 0 | 0 | 0 | 0 | 14 | 0 | 0 |
| repeated_pd | disguised | 56 | 0 | 0 | 0 | 49 | 0 | 0 | 0 | 7 |
| repeated_pd | named | 56 | 0 | 0 | 0 | 56 | 0 | 0 | 0 | 0 |

## How the model reasoned (all counted answers)

| Game | Wording | Names a concept | Dominance | Best response | Backward induction |
|---|---|---:|---:|---:|---:|
| cournot | disguised | 99% (137/138) | 1% (2/138) | 99% (136/138) | 0% (0/138) |
| cournot | named | 94% (130/138) | 0% (0/138) | 85% (117/138) | 0% (0/138) |
| public_goods | disguised | 99% (137/138) | 100% (138/138) | 9% (13/138) | 0% (0/138) |
| public_goods | named | 97% (132/136) | 99% (135/136) | 1% (1/136) | 0% (0/136) |
| repeated_pd | disguised | 68% (93/137) | 58% (80/137) | 0% (0/137) | 84% (115/137) |
| repeated_pd | named | 63% (86/137) | 45% (61/137) | 0% (0/137) | 91% (125/137) |
| vickrey | disguised | 100% (138/138) | 100% (138/138) | 0% (0/138) | 0% (0/138) |
| vickrey | named | 100% (138/138) | 100% (138/138) | 0% (0/138) | 0% (0/138) |

---

# nemotron · Stage 2B-B · reasoning codes (exploratory)

## Did the model name the game? (`NAMES_GAME`)

| Game | Normal | Disguised |
|---|---:|---:|
| cournot | 100% (92/92) | 100% (110/110) |
| vickrey | 11% (12/107) | 99% (105/106) |
| repeated_pd | 0% (0/96) | 0% (0/108) |
| public_goods | 70% (61/87) | 25% (23/92) |

## Why the equilibrium was missed (STRATEGIC_GAP answers)

| Game | Wording | Gaps | COLLUSIVE | DUOPOLY_FORMULA | TRUTHFUL_DEFAULT | COOPERATION_NORM | GROUP_OPTIMUM | MISMATCH | KNEW_AND_DEVIATED | UNCODED |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| public_goods | named | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 |

## How the model reasoned (all counted answers)

| Game | Wording | Names a concept | Dominance | Best response | Backward induction |
|---|---|---:|---:|---:|---:|
| cournot | disguised | 99% (109/110) | 0% (0/110) | 77% (85/110) | 0% (0/110) |
| cournot | named | 95% (87/92) | 0% (0/92) | 60% (55/92) | 0% (0/92) |
| public_goods | disguised | 95% (87/92) | 96% (88/92) | 0% (0/92) | 0% (0/92) |
| public_goods | named | 95% (83/87) | 95% (83/87) | 1% (1/87) | 0% (0/87) |
| repeated_pd | disguised | 100% (108/108) | 99% (107/108) | 0% (0/108) | 75% (81/108) |
| repeated_pd | named | 98% (94/96) | 100% (96/96) | 0% (0/96) | 38% (36/96) |
| vickrey | disguised | 92% (97/106) | 95% (101/106) | 0% (0/106) | 0% (0/106) |
| vickrey | named | 93% (100/107) | 96% (103/107) | 0% (0/107) | 0% (0/107) |
