"""Phase 0 deliverable: prove the whole trial pipeline works end to end.

Not a "hello world". It runs the smallest real instance of what every later
experiment does, on a locally-hosted model at zero cost:

    draw a private value -> prompt a model -> get a STRUCTURED action back
    -> parse it -> compare to the equilibrium -> record the deviation

It also runs a COMPETENCE CHECK alongside the trial. This separates two failure
modes that would otherwise be confounded:

    "the model cannot work out the equilibrium"      (competence)
    "the model knows it but does not play it"        (strategy)

Only the second is interesting. Without this split, a small model that simply
fails at the arithmetic looks identical to one making a strategic error, and the
project's central question collapses. See docs/reproducibility.md.

Run:  ./venv/bin/python scripts/smoke_test.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from openai import OpenAI
from pydantic import BaseModel, Field

import config


class BidResponse(BaseModel):
    """The structured action required back from an agent.

    Forcing a schema is what makes trials machine-parseable at scale. Free-text
    replies like "I'd bid around 68" are the most common cause of silent null
    rows in this kind of experiment.
    """
    bid: float = Field(description="The sealed bid to submit, in tokens.")
    reasoning: str = Field(description="One sentence explaining the bid.")


class StrategyKnowledge(BaseModel):
    """The competence probe: does the agent know the rule, asked directly?"""
    optimal_bid_equals_true_value: bool = Field(
        description="True if the optimal bid equals your exact private value."
    )
    explanation: str = Field(description="One sentence justification.")


PLAY_PROMPT = (
    "You are bidding in a sealed-bid auction for a single item against 2 other "
    "bidders. The highest bidder wins and pays the SECOND-highest bid submitted. "
    "Your private value for the item is {value} tokens -- winning at a price "
    "below that value profits you the difference; winning above it loses you the "
    "difference. Submit your bid."
)

KNOW_PROMPT = (
    "In a sealed-bid auction where the highest bidder wins but pays the "
    "second-highest bid submitted, what is the optimal bid for a rational bidder "
    "whose private value is known only to them?"
)

TRUE_VALUE = 73.0
EQUILIBRIUM_BID = TRUE_VALUE  # truthful bidding is weakly dominant


def client_for(spec: config.ModelSpec) -> OpenAI:
    return OpenAI(
        base_url=config.BASE_URLS[spec.provider],
        api_key=config.api_key(spec.provider),
    )


def run_trial(model_key: str) -> bool:
    spec = config.MODELS[model_key]
    client = client_for(spec)

    play = client.chat.completions.parse(
        model=spec.api_id,
        messages=[{"role": "user", "content": PLAY_PROMPT.format(value=TRUE_VALUE)}],
        response_format=BidResponse,
    ).choices[0].message.parsed

    know = client.chat.completions.parse(
        model=spec.api_id,
        messages=[{"role": "user", "content": KNOW_PROMPT}],
        response_format=StrategyKnowledge,
    ).choices[0].message.parsed

    deviation = play.bid - EQUILIBRIUM_BID
    print(f"  model          {spec.api_id}  (local, $0.00)")
    print(f"  private value  {TRUE_VALUE}")
    print(f"  equilibrium    {EQUILIBRIUM_BID}   (truthful bidding is weakly dominant)")
    print(f"  observed bid   {play.bid}")
    print(f"  DEVIATION      {deviation:+.2f}")
    print(f"  play reasoning {play.reasoning[:140]}")
    print()
    print(f"  COMPETENCE     knows bid==value? {know.optimal_bid_equals_true_value}")
    print(f"  know reasoning {know.explanation[:140]}")
    print()

    if know.optimal_bid_equals_true_value and abs(deviation) > 1e-9:
        verdict = "STRATEGIC GAP -- knows the rule, did not play it (the interesting case)"
    elif not know.optimal_bid_equals_true_value:
        verdict = "COMPETENCE GAP -- does not know the rule; deviation is not strategic"
    else:
        verdict = "AT EQUILIBRIUM -- knows the rule and played it"
    print(f"  VERDICT        {verdict}")
    return True


def main() -> int:
    ok = 0
    for model_key in ["qwen7b"]:
        print(f"\n--- {model_key} ---")
        try:
            run_trial(model_key)
            ok += 1
        except Exception as e:
            print(f"  FAILED: {type(e).__name__}: {e}")

    print("\n=== summary ===")
    if not ok:
        print("Phase 0 NOT complete -- no model returned a parsed action.")
        print("Is the Ollama server running?  ollama serve")
        return 1
    print(f"Phase 0 pipeline confirmed on {ok} model(s), at zero cost.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
