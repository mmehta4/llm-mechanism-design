# Informal predictions before any subsidy question was asked

Written by the project author on 2026-10-03, in the Stage 4A workbook (Task 6), before any
prisoner's-dilemma-with-subsidy question had been asked of any model. These are not
pre-registration 4. They are recorded here so the git timestamp shows they came first.

**Nemotron's cooperation rate in round 1 of the 10-round PD, with every cooperator paid τ
extra:**

| Subsidy τ | Author's guess | Logit QRE at Nemotron's fitted λ = 0.154 |
|---:|---:|---:|
| 0 | 41% | 44.5% |
| 1.5 | 65% | 50.0% (at every λ) |
| 5 | 95% | 62.7% |
| 10 | 98% | 78.0% |

**Author's reasoning:** steeper than QRE, i.e. more cooperation than QRE predicts. Nemotron
played the auction perfectly, so its low PD λ is probably a cooperation norm absorbed as
"noise" rather than real noise. Once a subsidy makes cooperation pay, the norm and the payoffs
point the same way, so cooperation should jump towards full. QRE at λ = 0.154 allows only a
sluggish 63–78%.

**What would show this wrong:** cooperation near 50% at τ = 1.5 and close to the QRE column at
τ = 5 and 10.
