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

---

# The prisoner's dilemma with a cooperation subsidy

## Set-up

- Stage 2A's PD payoffs: T = 5, R = 3, P = 1, S = 0.
- **Rule S(τ):** every player who cooperates is paid an extra τ. (A tax of τ on defecting is
  the same rule for the players, since only the payoff difference between the two actions
  matters.)
- **Symmetric logit QRE** (as in the Stage 3 fits). Against an opponent who cooperates with
  probability p, defecting pays more by ΔU(p) = p(T − R) + (1 − p)(P − S). Under S(τ), that
  advantage becomes ΔU(p) − τ, so

  p = 1 / (1 + exp(λ (ΔU(p) − τ))).

## Theorem 3: the subsidy needed for a cooperation target, in closed form

Write logit(p) = ln(p / (1 − p)). The τ at which the QRE cooperation rate equals p* is

  **τ(p\*, λ) = ΔU(p\*) + logit(p\*) / λ.**

**Proof.** Rearrange the QRE condition: (1 − p)/p = exp(λ (ΔU(p) − τ)), so
−logit(p) = λ (ΔU(p) − τ). Solve for τ. ∎

Since T − R ≥ P − S, ΔU increases in p, so the right-hand side of the QRE condition falls in p
and the fixed point is unique. Each target has exactly one subsidy.

**Corollary (a prediction with no free parameter).** logit(1/2) = 0, so at

  **τ½ = ΔU(1/2) = ((T − R) + (P − S)) / 2 = 1.5**

every logit-QRE population cooperates exactly half the time, **whatever its λ**. Rational
players agree. Between τ = P − S = 1 and τ = T − R = 2, the subsidised game is "chicken", and
its symmetric equilibrium is mixed, with p = τ − 1. That gives p = 1/2 at τ = 1.5 too. So all
the QRE curves cross the rational ramp at the same point; λ only sets how steep the curve is
there.

**Cooperation rate under subsidy τ:**

| λ | τ = 0 | 1 | **1.5** | 2 | 3 | 5 | 10 | 20 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.154 (Nemotron, Stage 2A fit) | 44% | 48% | **50%** | 52% | 56% | 63% | 78% | 94% |
| 0.5 | 34% | 44% | **50%** | 56% | 66% | 83% | 98% | 100% |
| 2.0 | 10% | 34% | **50%** | 66% | 90% | 100% | 100% | 100% |
| rational (λ → ∞) | 0% | 0% | **50%** | 100% | 100% | 100% | 100% | 100% |

Nemotron's observed first-round cooperation at τ = 0 is 41% (Stage 2A, named wording).

**Subsidy needed for a target:**

| λ | p\* = 25% | 50% | 75% | 90% | 99% |
|---:|---:|---:|---:|---:|---:|
| 0.154 | −5.9 (a *tax* on cooperating) | 1.5 | 8.9 | 16.2 | 31.8 |
| 0.5 | −0.9 | 1.5 | 3.9 | 6.3 | 11.2 |
| 2.0 | 0.7 | 1.5 | 2.3 | 3.0 | 4.3 |

**What this means:**
- Noisy players are cheap to nudge to partial cooperation, and very expensive to get to near
  certainty. Rational theory says τ just above 2 buys 100% cooperation. For Nemotron's fitted
  λ, 90% costs about 16.
- **For Stage 5, this is a much stronger test than the auction.** The effects are tens of
  percentage points, not 1%.
- **The halfway point separates the behaviour models with no fitting at all:**
  - any logit-QRE player cooperates 50% at τ = 1.5;
  - a model that recalls "always defect in a finitely repeated PD" stays near 0%;
  - a model driven by a cooperation norm (the reasoning code `COOPERATION_NORM`) sits well
    above 50%.

**Caveats, stated now:**
- The Stage 2A PD is round 1 of a known 10-round game. The stage-game QRE ignores
  continuation play, which is harmless for a rational player (backward induction) but is a
  modelling choice for a noisy one.
- Nemotron's PD λ is uncertain: the 95% interval is [0.0016, 0.47]. Predictions away from the
  halfway point inherit that uncertainty; the halfway point does not.

## Cournot: no mechanism target, so far

After the fraction-slip correction, Nemotron plays the Cournot equilibrium in about 98% of
counted answers. Its misses were mostly answers cut at a fraction bar, and a mechanism that
corrects a formatting error isn't mechanism design. The decision gate rechecks this with all
four models.

**Beyond logit (Meet Mehta, Stage 4A Task 5f).** The halfway-point prediction does not depend
on the logit form. In any *regular* quantal response with symmetric errors, a player who is
indifferent chooses each action with probability ½. ΔU − τ rises in p, while the response
falls in ΔU − τ, so the fixed point is unique. At τ = ΔU(½) it is therefore p = ½. A miss at
τ = 1.5 can't be blamed on having chosen logit: it rejects the whole regular-QRE family.

**Correction: the stage game vs the 10-round game (Meet Mehta, final workbook, Task 1).** The
halfway-point prediction is for the one-shot *stage* game. For 1 < τ < 2 the subsidised stage
game is chicken, with two pure equilibria that pay each player differently (5 vs τ). In a
finitely repeated game with several stage equilibria like this, early cooperation can be
subgame-perfect (Benoît & Krishna, 1985): play (C, C), and punish a deviator in the last round
with the equilibrium worst for them. At τ = 1.5:
- deviating from C gains 5 − 4.5 = 0.5;
- the last-round punishment costs at least 3 − 1.5 = 1.5 (against the mixed equilibrium) and up
  to 5 − 1.5 = 3.5.

So mutual cooperation in round 1 is consistent with fully rational play. At τ = 0, 2.5 and τ\*
the stage equilibrium is unique, so nothing changes there. Stage 5 keeps τ = 1.5, for
comparability with the stage-game λ fits, and reads a cooperation rate above 50% there as either
a norm or repeated-game reasoning (`docs/interpretation-key.md`).

**The headline test (author's amendment).** "τ\* gives more cooperation than 2.5" is nearly
guaranteed, because τ\* = 1.9 + ln 9/λ > 2.5 whenever λ < 3.66. The real test compares the
theories' predictions: at τ = 2.5, is QRE closer than classical theory's 100%? And at τ\* is the
observed rate within 90 ± 15?
