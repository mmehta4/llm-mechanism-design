# Hand check, round 3: `NAMES_GAME` in the Stage 2C extreme wording

- **Sample:** 40 real Stage 2C answers (seed 20261004), 10 per game, with the model and verdict
  hidden. Taken from the 80 counted answers available on 2026-10-03 (Nemotron and Kimi).
- **Coder: the author**, blind to the computer's codes.
- **Rule:** "names the game" means the reasoning names the game or a textbook game it is
  recognised as; describing the maths ("dominant", "best response", "Nash") is not naming.

| Game | Second coder: yes | Computer: yes | Agreement |
|---|---:|---:|---:|
| Vickrey | 9/10 | 9/10 | 10/10 |
| Cournot | 0/10 | 0/10 | 10/10 |
| Repeated PD | 7/10 | 7/10 | 10/10 |
| Public goods | 7/10 | 7/10 | 10/10 |
| **All** | 23/40 | 23/40 | **40/40, κ = 1.00** |

**Edge cases noted by the author:**
- #28 uses "sucker" (PD jargon) without naming the game: coded no.
- #19 and #23 use "MPCR" and also say "public goods game": coded yes.
- #4 and #18 give dominance arguments only: coded no.

**How to read this.** This extends rounds 1 and 2 (κ = 1.00 for `NAMES_GAME` on Stage 2A wording)
to the new extreme wording. The automatic recognition code behaves there as a careful human reader
of the definition does, so the Stage 2C recognition numbers can be reported without a warning.
