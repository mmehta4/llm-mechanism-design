"""Competence probes — separating "cannot compute" from "will not play it".

Fitted lambda conflates two very different agents: one that computes the equilibrium
correctly but responds noisily, and one that cannot do the arithmetic at all. Only
the first is a behavioural finding; "small models are bad at algebra" is not a paper.

So every trial is paired with a probe that asks about the PAYOFF MECHANICS directly,
separately from asking the agent to play.

Two design decisions worth stating:

1. PROBES ARE NUMERIC WHERE POSSIBLE, not yes/no. A boolean probe tests recall of an
   answer; a numeric one tests whether the agent can actually push the numbers
   through. Observed in the very first pilot run back in Phase 0: a model answered a
   boolean probe correctly while justifying it with reasoning about a completely
   different auction format. A number is much harder to get right by accident.

2. THEY REPORT ONLY THE AGENT'S OWN PAYOFF, and lead every line with the agent's own
   choice. The first version listed four two-player outcomes ("you D and they C: you
   5, them 0") and the model inverted the rows in BOTH framings -- a prompt-design
   fault, not a model failure. Bookkeeping the opponent's score is irrelevant to the
   question being asked, so it was removed.

3. PROBES MATCH THE FRAMING OF THE TRIAL. A named probe after a disguised trial would
   hand the model the vocabulary the disguise exists to withhold. It would also
   misclassify an agent that knows the textbook rule but cannot read the disguised
   mechanics -- that agent is not competent *on this trial*, and the probe must say so.
"""
from __future__ import annotations

from pydantic import BaseModel, Field


class NumericProbe(BaseModel):
    answer: float = Field(description="The numeric answer.")
    reasoning: str = Field(description="One or two sentences of working.")


class ChoiceProbe(BaseModel):
    """`answer` must be the bare label and nothing else.

    A model that writes "setting Y would give you more" into this field has answered
    CORRECTLY but formatted wrongly. Scoring that as a competence failure would
    exclude a correct trial from the behavioural fits -- see PROBE_FORMAT_FAIL in
    experiments/trial.py, which keeps the two apart.
    """
    answer: str = Field(
        description="The chosen label ONLY -- a single token such as X or Y. "
                    "No sentence, no explanation, no punctuation."
    )
    reasoning: str = Field(description="One or two sentences of working.")


# ---------------------------------------------------------------------------
# Each entry: (prompt template, schema, function computing the correct answer)
# The templates take the same parameters as the game they belong to.
# ---------------------------------------------------------------------------

PROBES = {
    ("vickrey", "named"): (
        "In a sealed-bid auction the highest bidder wins and pays the SECOND-highest "
        "bid submitted. Your private value is 50 and you bid 50. The highest bid among "
        "the other bidders is 60. What is your payoff?",
        NumericProbe,
        lambda **_: 0.0,          # you lose the auction, so payoff is zero
    ),
    ("vickrey", "disguised"): (
        "Research stations request a processing slot. The station with the highest "
        "request receives the slot and is charged the amount of the SECOND-highest "
        "request. The slot is worth 50 credits to your station and you request 50. The "
        "highest request among the other stations is 60. What is your net result?",
        NumericProbe,
        lambda **_: 0.0,
    ),

    ("cournot", "named"): (
        "Two firms choose quantities. Market price is P = 100 - 1 * (q1 + q2). Each "
        "unit costs 10 to make, and profit is (P - 10) * your quantity. The other "
        "firm produces 30 units. What quantity maximises YOUR profit?",
        NumericProbe,
        lambda **_: 30.0,         # (100 - 10 - 30) / 2 = 30
    ),
    ("cournot", "disguised"): (
        "Two operators draw from one reservoir. The amount each channel delivers is "
        "V = 100 - 1 * (your channels + their channels). Each channel costs 10 "
        "credits to maintain, and what you gain is (V - 10) * your number of "
        "channels. The other operator opens 30 channels. How many channels maximise "
        "what YOU gain?",
        NumericProbe,
        lambda **_: 30.0,
    ),

    ("public_goods", "named"): (
        "Four players each hold 20 tokens. Each contributes some amount to a common "
        "pot; the pot is multiplied by 2 and split equally among all four regardless "
        "of who contributed. If you contribute exactly 1 more token, how much of that "
        "token comes back to you?",
        NumericProbe,
        lambda M=2.0, n_total=4, **_: M / n_total,     # 0.5
    ),
    ("public_goods", "disguised"): (
        "Four operators each hold 20 units of signal. Each routes some amount into a "
        "central amplifier; the total routed is multiplied by 2 and divided evenly "
        "among all four regardless of who routed what. If you route exactly 1 more "
        "unit, how much of that unit comes back to you?",
        NumericProbe,
        lambda M=2.0, n_total=4, **_: M / n_total,
    ),

    ("repeated_pd", "named"): (
        "Two players simultaneously choose C or D. Your own score:\n"
        "  you choose C, they choose C  ->  you score 3\n"
        "  you choose D, they choose C  ->  you score 5\n"
        "  you choose C, they choose D  ->  you score 0\n"
        "  you choose D, they choose D  ->  you score 1\n"
        "Consider ONE round in isolation. They choose C. Which of your two choices "
        "scores you more? Reply with the single letter only.",
        ChoiceProbe,
        lambda **_: "D",
    ),
    ("repeated_pd", "disguised"): (
        "Two technicians simultaneously set panels to position {coop} or {defect}. "
        "Your own units received:\n"
        "  you set {coop}, they set {coop}  ->  you receive 3\n"
        "  you set {defect}, they set {coop}  ->  you receive 5\n"
        "  you set {coop}, they set {defect}  ->  you receive 0\n"
        "  you set {defect}, they set {defect}  ->  you receive 1\n"
        "Consider ONE round in isolation. They set {coop}. Which of your two settings "
        "gives you more? Reply with the single letter only.",
        ChoiceProbe,
        lambda defect="Y", **_: defect,
    ),
}


def probe_for(game_key: str, framing: str, **params):
    """Returns (rendered prompt, schema, correct answer) for this game and framing."""
    template, schema, correct = PROBES[(game_key, framing)]
    return template.format(**params), schema, correct(**params)


def is_malformed(given, correct) -> bool:
    """True when the answer is unusable as given, rather than wrong.

    A discrete answer should be a bare label. When a model returns a whole sentence
    it has usually answered correctly and formatted badly -- and substring matching
    cannot rescue it, because a sentence like "if they set X then Y gives you more"
    contains BOTH labels. So this is flagged as its own failure mode rather than
    guessed at.
    """
    if given is None:
        return True
    if isinstance(correct, str):
        return len(str(given).strip()) > 3
    try:
        float(given)
        return False
    except (TypeError, ValueError):
        return True


def probe_passed(given, correct, tolerance: float = 0.01) -> bool:
    """Numeric answers within tolerance; discrete answers by exact match.

    Returns False for malformed answers too -- callers must check is_malformed()
    first if they need to tell "wrong" from "unusable".
    """
    if is_malformed(given, correct):
        return False
    if isinstance(correct, str):
        return str(given).strip().upper() == correct.strip().upper()
    try:
        return abs(float(given) - float(correct)) <= tolerance
    except (TypeError, ValueError):
        return False
