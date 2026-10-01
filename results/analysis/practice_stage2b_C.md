# PRACTICE ROUND ONLY (not confirmatory)

## Block C: number sweep

| Game | Size | Normal | Disguised |
|---|---|---:|---:|
| vickrey | n_others = 1 | 100% (1/1) | 100% (1/1) |
| vickrey | n_others = 3 | 100% (1/1) | 100% (1/1) |
| vickrey | n_others = 7 | 100% (1/1) | 100% (1/1) |
| cournot | a = 60 | 100% (1/1) | 0% (0/1) |
| cournot | a = 100 | 100% (1/1) | 0% (0/1) |
| cournot | a = 200 | 0% (0/1) | 100% (1/1) |
| public_goods | n_others = 2 | 100% (1/1) | 100% (1/1) |
| public_goods | n_others = 3 | 100% (1/1) | 100% (1/1) |
| public_goods | n_others = 7 | 100% (1/1) | 100% (1/1) |
| repeated_pd | n_rounds = 2 | 100% (1/1) | 100% (1/1) |
| repeated_pd | n_rounds = 10 | 100% (1/1) | 0% (0/1) |
| repeated_pd | n_rounds = 50 | 0% (0/1) | 100% (1/1) |

**Does the wording effect change with size?** (logistic regression, interaction wording × size, Holm across games)

| Game | Interaction (log-odds per size step) | p | Holm p |
|---|---:|---:|---:|
| vickrey | not estimable: every answer has the same outcome | nan | nan |
| cournot | not estimable: separation (a group is all-correct or all-wrong); see the table | nan | nan |
| public_goods | not estimable: every answer has the same outcome | nan | nan |
| repeated_pd | not estimable: separation (a group is all-correct or all-wrong); see the table | nan | nan |
