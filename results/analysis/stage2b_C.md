# Stage 2B confirmatory analysis

## Block C: number sweep

| Game | Size | Normal | Disguised |
|---|---|---:|---:|
| vickrey | n_others = 1 | 100% (184/184) | 99% (135/137) |
| vickrey | n_others = 3 | 100% (184/184) | 99% (133/135) |
| vickrey | n_others = 7 | 100% (184/184) | 100% (137/137) |
| cournot | a = 60 | 96% (173/181) | 71% (127/179) |
| cournot | a = 100 | 96% (172/179) | 66% (121/182) |
| cournot | a = 200 | 95% (172/182) | 65% (115/176) |
| public_goods | n_others = 2 | 100% (178/178) | 87% (139/160) |
| public_goods | n_others = 3 | 99% (182/184) | 90% (166/184) |
| public_goods | n_others = 7 | 99% (180/182) | 96% (175/183) |
| repeated_pd | n_rounds = 2 | 83% (152/184) | 81% (149/184) |
| repeated_pd | n_rounds = 10 | 47% (86/184) | 65% (120/184) |
| repeated_pd | n_rounds = 50 | 34% (62/184) | 64% (118/184) |

**Does the wording effect change with size?** (logistic regression, interaction wording × size, Holm across games)

| Game | Interaction (log-odds per size step) | p | Holm p |
|---|---:|---:|---:|
| vickrey | not estimable: separation (a group is all-correct or all-wrong); see the table | nan | nan |
| cournot | -0.0868 | 0.768 | 0.768 |
| public_goods | +1.36 | 0.0706 | 0.141 |
| repeated_pd | +0.737 | 2.67e-05 | 8e-05 |
