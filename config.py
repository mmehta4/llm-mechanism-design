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
    # --- Local, via Ollama. Free, unlimited, and PERFECTLY reproducible: the
    # weights are pinned and downloadable, so anyone can rerun this experiment
    # exactly. Frontier API models get deprecated and silently updated, which is
    # the single biggest reproducibility hole in this kind of study -- running on
    # open weights closes it. Treat this as a genuine methodological strength,
    # not just a budget compromise.
    "qwen7b": ModelSpec(
        key="qwen7b",
        provider="ollama",
        api_id="qwen2.5:7b",
        input_usd_per_mtok=0.0,
        output_usd_per_mtok=0.0,
        supports_temperature=True,
    ),
    "qwen7b_coder": ModelSpec(
        key="qwen7b_coder",
        provider="ollama",
        api_id="qwen2.5-coder:7b",
        input_usd_per_mtok=0.0,
        output_usd_per_mtok=0.0,
        supports_temperature=True,
    ),
    # --- Capable open-weight arm, via Groq's free tier.
    # 120B open weights: capable enough to differentiate a quadratic, and PINNED --
    # anyone can rerun this experiment against the same weights in five years. That
    # is what keeps the reproducibility argument alive once a hosted frontier arm is
    # in the roster, since free-tier hosted models get deprecated and replaced.
    "gptoss120b": ModelSpec(
        key="gptoss120b",
        provider="groq",
        api_id="openai/gpt-oss-120b",
        input_usd_per_mtok=0.0,      # free tier
        output_usd_per_mtok=0.0,
        supports_temperature=True,
    ),
    # --- Most capable arm reachable at zero cost, via Google AI Studio's free tier.
    # Not reproducible in the way open weights are -- note that in limitations.
    "gemini": ModelSpec(
        key="gemini",
        provider="gemini",
        api_id="gemini-3.8-flash",
        input_usd_per_mtok=0.0,      # free tier
        output_usd_per_mtok=0.0,
        supports_temperature=True,
    ),
}

# The roster spans roughly 7B -> 120B -> frontier. That ladder is deliberate: it
# lets delta-lambda be read against capability, rather than only against framing.
CAPABILITY_ORDER = ["qwen7b", "gptoss120b", "gemini"]

# Base URLs by provider. Ollama exposes an OpenAI-compatible endpoint, so one
# client code path serves local, OpenRouter, and Groq alike.
BASE_URLS = {
    "ollama": "http://localhost:11434/v1",
    "openrouter": "https://openrouter.ai/api/v1",
    "groq": "https://api.groq.com/openai/v1",
    # Gemini's OpenAI-compatibility layer. Trailing slash is required.
    "gemini": "https://generativelanguage.googleapis.com/v1beta/openai/",
}

# Providers that need no credential (local inference).
NO_KEY_PROVIDERS = {"ollama"}

DEFAULT_MODEL = "qwen7b"

# --- Reasoning depth --------------------------------------------------------
# The overview lists "chain-of-thought allowed vs. not" as a condition. On the
# current Anthropic models thinking is adaptive and on by default, so a clean
# on/off binary is not available. `effort` is the real lever and is a better
# experimental factor anyway: it is ordinal, not binary.
# Convenient parity: OpenAI's GPT-5.6 family exposes the same reasoning ladder
# (none/low/medium/high/xhigh/max), so this factor can be held comparable across
# providers rather than being confounded with them.
EFFORT_LEVELS = ["low", "medium", "high", "xhigh", "max"]
DEFAULT_EFFORT = "high"

# --- Reproducibility --------------------------------------------------------
MASTER_SEED = 20260831           # seeds all private-value draws
MAX_TOKENS = 4096                # ample for a single game action + reasoning


def api_key(provider: str) -> str:
    if provider in NO_KEY_PROVIDERS:
        return "not-needed"
    env_var = {
        "gemini": "GEMINI_API_KEY",
        "openrouter": "OPENROUTER_API_KEY",
        "groq": "GROQ_API_KEY",
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
