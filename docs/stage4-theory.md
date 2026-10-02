# Stage 4A: second-price auctions with noisy (logit QRE) bidders

Derivation notes. The proofs of Theorems 1 and 2 are Meet Mehta's (Stage 4A workbook,
2026-10-03); the numbers come from `mechanisms/auction.py`, and its tests are in
`tests/test_mechanisms.py`.

## Set-up

- n bidders, with values vᵢ i.i.d. uniform on [10, 100] (the Stage 2A Vickrey values).
- **Rule M(r, α):** the highest bid wins if it is at least the reserve r, and the winner pays
  α × max(second-highest bid, r). The ordinary Vickrey auction is M(0, 1).
- **Logit QRE:** a bidder with value v bids b with density ∝ exp(λ · U(b | v)). U is the
  expected payoff against the other bidders' bids, which are themselves the QRE (a symmetric
  fixed point). Payoffs are in value units, so λ is on the scale of the Stage 2A fits.

## Theorem 1: the payment multiplier α does nothing for QRE bidders

If B₁, …, Bₙ is a QRE of M(r, 1) on bid space [0, B̄], then B₁/α, …, Bₙ/α is a QRE of
M(r/α, α) on [0, B̄/α]. The winner, revenue and every payoff are the same.

**Proof.**
1. Against a highest rival bid H, U_α(b | v) = E[(v − αH) · 1{H < b}].
2. With H = H₁/α and b = β/α:
   U_α(β/α | v) = E[(v − H₁) · 1{H₁ < β}] = U₁(β | v).
3. So your M_α bid B has density ∝ exp(λ U₁(αB | v)). By change of variables, X = αB has
   density ∝ exp(λ U₁(x | v)), which is the M₁ QRE density. The normalising constants agree
   because both densities integrate to 1.
4. So the scaled profile is self-consistent, and therefore a QRE.
5. Dividing every bid by α keeps their order, so the same bidder wins. The revenue is
   α · B₍₂₎/α = B₍₂₎. ∎

The theorem needs the bid space to scale with α. With a fixed bid space, the support changes
and the invariance is only approximate. The toolkit lays the bid grid out in value units, and
the identity holds to 10⁻⁹ (test `test_theorem1_alpha_changes_nothing_for_qre_bidders`).

**Why it matters for the project.** α is a change of currency for a noisy deriver: α × bid
has the same distribution at every α. A model that *recalls* "bid your value" bids v whatever
α is. Under M(0, 2) it then pays twice the second-highest bid. With three such bidders, the
winner's expected payoff is E[top] − 2·E[second] = 77.5 − 110 = −32.5. So any dependence of
α × bid on α cannot be QRE noise; it is the fingerprint of recall. Stage 2B's Vickrey trap
(α = 2) measures exactly this.

## Theorem 2: for efficiency, the best reserve is r = 0

Efficiency is the value of the winner, or 0 if there is no sale. For fixed bids, r never
changes who has the highest bid. It only decides whether that bid clears r. So r > 0 either
leaves the outcome unchanged or replaces a value of at least 10 with 0. ∎

This argument covers the mechanical effect. Under QRE the bids also respond to r. That
strategic effect is checked numerically: efficiency falls with r at every λ tested (test
`test_theorem2_a_reserve_never_raises_efficiency`).

**Consequence.** The originally planned problem, "maximise efficiency over (r, α)", has a
trivial answer: r = 0, and any α. Stage 4 therefore maximises **revenue** (workbook Task 4).

## The revenue-optimal reserve r*(λ)

- **Rational bidders (Myerson):** φ(v) = 2v − 100, so r* = 50 for any number of i.i.d.
  bidders.
- **Noisy bidders:** 3 bidders, reserve grid in steps of 0.5:

| λ | r*(λ) | Revenue at r* | Revenue at 50 | Revenue at 0 | Efficiency share at r* |
|---:|---:|---:|---:|---:|---:|
| 0.02 | **57.0** | 69.89 | 69.64 | 66.90 | 0.702 |
| 0.05 | 48.5 | 63.00 | 62.98 | 60.64 | 0.777 |
| 0.1 | 44.0 | 58.68 | 58.37 | 56.63 | 0.848 |
| 0.2 | **41.5** | 56.15 | 55.60 | 54.43 | 0.904 |
| 0.5 | 42.0 | 54.96 | 54.62 | 53.55 | 0.940 |
| 1 | 45.0 | 55.11 | 54.98 | 53.68 | 0.946 |
| 2 | 47.0 | 55.56 | 55.51 | 54.01 | 0.949 |
| 5 | 48.5 | 56.09 | 56.08 | 54.41 | 0.951 |
| 20 | 49.5 | 56.52 | 56.52 | 54.77 | 0.954 |
| 100 | 49.5 | 56.67 | 56.67 | 54.93 | 0.956 |

(At large λ, r* is 49.5 rather than 50 because of the grid and the tie rule.)

**r\*(λ) is U-shaped.** It falls below Myerson's 50 when noise is moderate and rises above it
when noise is extreme. The reason, at r = 50:

| λ | Bidders with v > 50 who bid below 50 | Bidders with v < 50 who bid 50 or more | Mean bid at v = 20 | Mean bid at v = 80 |
|---:|---:|---:|---:|---:|
| 0.02 | 33% | 56% | 59.3 | 73.8 |
| 0.2 | 21% | 13% | 26.8 | 82.8 |
| 5 | 4% | 0% | 24.9 | 79.7 |

- **Moderate noise:** bids still track values, but a fifth of the bidders who would gladly
  pay the reserve slip below it and are excluded. Lowering r wins those sales back, so
  r* < 50.
- **Extreme noise:** bids barely track values; a bidder worth 20 bids 59 on average. The
  reserve is no longer a filter on values. It is a floor under random overbids, and raising it
  extracts more of them, so r* > 50.

**Effect size.** r* beats Myerson's reserve by at most about 0.55 tokens of revenue, about 1%,
around λ ≈ 0.2. A difference that small is unlikely to be detectable in a Stage 5 test with
AI bidders. So the auction result belongs in the paper as theory, not as the mechanism Stage 5
tests. The decision gate (late October) picks the game where the AIs are actually noisy.
