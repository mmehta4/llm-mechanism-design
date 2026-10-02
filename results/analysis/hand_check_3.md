# Hand check, round 3: `NAMES_GAME` in the Stage 2C extreme wording

- **Sample:** 40 real Stage 2C answers (seed 20261004), 10 per game, with the model and verdict
  hidden. Taken from the 80 counted answers available on 2026-10-03 (Nemotron and Kimi).
- **Second coder: Claude (Opus 5.5), not a human.** It coded the sheet at the author's request,
  without seeing the computer's codes.
- **Rule:** "names the game" means the reasoning names the game or a textbook game it is
  recognised as; describing the maths ("dominant", "best response", "Nash") is not naming.

| Game | Second coder: yes | Computer: yes | Agreement |
|---|---:|---:|---:|
| Vickrey | 9/10 | 9/10 | 10/10 |
| Cournot | 0/10 | 0/10 | 10/10 |
| Repeated PD | 7/10 | 7/10 | 10/10 |
| Public goods | 7/10 | 7/10 | 10/10 |
| **All** | 23/40 | 23/40 | **40/40, κ = 1.00** |

**Edge cases noted by the coder:**
- #28 uses "sucker" (PD jargon) without naming the game: coded no.
- #19 and #23 use "MPCR" and also say "public goods game": coded yes.
- #4 and #18 give dominance arguments only: coded no.

**How to read this.** Agreement between two automated coders is weaker evidence than the human
validation of rounds 1 and 2 (κ = 1.00 on Stage 2A wording). The paper reports it as an AI
second coder, not as human validation. It does show the regular expressions behave in the new
wording as an independent reader of the definition would.
