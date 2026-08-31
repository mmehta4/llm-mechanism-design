"""Central configuration: model roster, pricing, and reproducibility constants.

Every experiment imports from here so that the exact model versions used in a
run are recorded in one place and logged with every trial row.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, asdict

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class ModelSpec:
    """One arm of the cross-model comparison.

    `api_id` is the exact version string sent to the provider and written into
    every logged row. Never log a friendly name alone -- providers deprecate and
    silently update models, and a result that cannot name its subject cannot be
    rechecked later.
    """
    key: str
    provider: str          # "anthropic" | "openai" | "openrouter"
    api_id: str
    input_usd_per_mtok: float
    output_usd_per_mtok: float
    supports_temperature: bool


# --- The roster -------------------------------------------------------------
# Cross-model comparison is what distinguishes a genuine phenomenon from one
# model's idiosyncrasy (overview section 6.1). Three arms, deliberately spanning
# capability tiers.
MODELS: dict[str, ModelSpec] = {
    "opus5": ModelSpec(
        key="opus5",
        provider="anthropic",
        api_id="claude-opus-5",
        input_usd_per_mtok=5.00,
        output_usd_per_mtok=25.00,
        # Sampling parameters (temperature/top_p/top_k) were REMOVED on the
        # current Anthropic models -- passing them returns HTTP 400. Determinism
        # cannot be pinned this way; see docs/reproducibility.md.
        supports_temperature=False,
    ),
    "sonnet5": ModelSpec(
        key="sonnet5",
        provider="anthropic",
        api_id="claude-sonnet-5",
        input_usd_per_mtok=2.00,
        output_usd_per_mtok=10.00,
        supports_temperature=False,
    ),
    "haiku45": ModelSpec(
        key="haiku45",
        provider="anthropic",
        api_id="claude-haiku-4-5",
        input_usd_per_mtok=1.00,
        output_usd_per_mtok=5.00,
        supports_temperature=True,
    ),
    # Second-provider arm. VERIFY this identifier against OpenAI's current model
    # list before you rely on it -- it is a placeholder, not a checked value.
    "openai": ModelSpec(
        key="openai",
        provider="openai",
        api_id=os.getenv("OPENAI_MODEL_ID", "gpt-4.1"),
        input_usd_per_mtok=float(os.getenv("OPENAI_INPUT_PRICE", "0")),
        output_usd_per_mtok=float(os.getenv("OPENAI_OUTPUT_PRICE", "0")),
        supports_temperature=True,
    ),
}

DEFAULT_MODEL = "opus5"

# --- Reasoning depth --------------------------------------------------------
# The overview lists "chain-of-thought allowed vs. not" as a condition. On the
# current Anthropic models thinking is adaptive and on by default, so a clean
# on/off binary is not available. `effort` is the real lever and is a better
# experimental factor anyway: it is ordinal, not binary.
EFFORT_LEVELS = ["low", "medium", "high", "xhigh", "max"]
DEFAULT_EFFORT = "high"

# --- Reproducibility --------------------------------------------------------
MASTER_SEED = 20260831           # seeds all private-value draws
MAX_TOKENS = 4096                # ample for a single game action + reasoning


def api_key(provider: str) -> str:
    env_var = {
        "anthropic": "ANTHROPIC_API_KEY",
        "openai": "OPENAI_API_KEY",
        "openrouter": "OPENROUTER_API_KEY",
    }[provider]
    key = os.getenv(env_var)
    if not key:
        raise RuntimeError(
            f"{env_var} is not set. Copy .env.example to .env and fill it in."
        )
    return key


def run_metadata(model_key: str, effort: str) -> dict:
    """Metadata stamped onto every logged trial row."""
    spec = MODELS[model_key]
    return {
        "model_key": spec.key,
        "model_api_id": spec.api_id,
        "provider": spec.provider,
        "effort": effort,
        "master_seed": MASTER_SEED,
    }
