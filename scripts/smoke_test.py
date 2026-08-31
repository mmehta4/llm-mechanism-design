"""Phase 0 deliverable: prove the whole trial pipeline works end to end.

This is deliberately not a "hello world". It runs a single real Vickrey auction
trial -- the smallest possible instance of what every later experiment does:

    draw a private value -> prompt a model -> get a STRUCTURED action back
    -> parse it -> compare to the equilibrium -> report the deviation

If this passes, authentication, structured output, parsing, and the deviation
metric are all confirmed working. Run:

    python scripts/smoke_test.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pydantic import BaseModel, Field

import config


class BidResponse(BaseModel):
    """The structured action we require back from an agent.

    Forcing a schema is what makes trials machine-parseable at scale. Free-text
    replies like "I'd bid around 68" are the single most common cause of silent
    null rows in this kind of experiment.
    """
    bid: float = Field(description="The sealed bid to submit, in tokens.")
    reasoning: str = Field(description="One sentence explaining the bid.")


PROMPT = (
    "You are bidding in a sealed-bid auction for a single item against 2 other "
    "bidders. The highest bidder wins and pays the SECOND-highest bid submitted. "
    "Your private value for the item is {value} tokens -- winning at a price "
    "below that value profits you the difference; winning above it loses you the "
    "difference. Submit your bid."
)

TRUE_VALUE = 73.0
EQUILIBRIUM_BID = TRUE_VALUE  # truthful bidding is dominant in a Vickrey auction


def cost_usd(spec: config.ModelSpec, usage) -> float:
    return (
        usage.input_tokens / 1_000_000 * spec.input_usd_per_mtok
        + usage.output_tokens / 1_000_000 * spec.output_usd_per_mtok
    )


def run_anthropic(model_key: str) -> bool:
    import anthropic

    spec = config.MODELS[model_key]
    client = anthropic.Anthropic(api_key=config.api_key("anthropic"))

    # NOTE: no `temperature` argument. Sampling parameters were removed on the
    # current Anthropic models and passing one returns HTTP 400.
    response = client.messages.parse(
        model=spec.api_id,
        max_tokens=config.MAX_TOKENS,
        messages=[{"role": "user", "content": PROMPT.format(value=TRUE_VALUE)}],
        output_format=BidResponse,
    )

    action = response.parsed_output
    report(spec, action, cost_usd(spec, response.usage))
    return True


def run_openai(model_key: str) -> bool:
    from openai import OpenAI

    spec = config.MODELS[model_key]
    client = OpenAI(api_key=config.api_key("openai"))

    completion = client.chat.completions.parse(
        model=spec.api_id,
        messages=[{"role": "user", "content": PROMPT.format(value=TRUE_VALUE)}],
        response_format=BidResponse,
    )
    action = completion.choices[0].message.parsed
    report(spec, action, cost_usd(spec, completion.usage) if spec.input_usd_per_mtok else 0.0)
    return True


def report(spec: config.ModelSpec, action: BidResponse, cost: float) -> None:
    deviation = action.bid - EQUILIBRIUM_BID
    print(f"  model         {spec.api_id}")
    print(f"  private value {TRUE_VALUE}")
    print(f"  equilibrium   {EQUILIBRIUM_BID}  (truthful bidding is dominant)")
    print(f"  observed bid  {action.bid}")
    print(f"  DEVIATION     {deviation:+.2f}")
    print(f"  reasoning     {action.reasoning[:100]}")
    print(f"  cost          ${cost:.5f}")


def main() -> int:
    targets = [("anthropic", "opus5", run_anthropic), ("openai", "openai", run_openai)]
    results = {}

    for provider, model_key, runner in targets:
        print(f"\n--- {provider} ---")
        try:
            config.api_key(provider)
        except RuntimeError as e:
            print(f"  SKIPPED: {e}")
            results[provider] = None
            continue
        try:
            runner(model_key)
            results[provider] = True
        except Exception as e:
            print(f"  FAILED: {type(e).__name__}: {e}")
            results[provider] = False

    print("\n=== summary ===")
    for provider, ok in results.items():
        status = {True: "OK", False: "FAILED", None: "no key set"}[ok]
        print(f"  {provider:<12} {status}")

    passed = [v for v in results.values() if v is True]
    if not passed:
        print("\nPhase 0 NOT complete -- no provider returned a parsed action.")
        return 1
    print(f"\nPhase 0 pipeline confirmed on {len(passed)} provider(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
