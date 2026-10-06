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
    # Sent only when set. None means the provider's default, which is what every
    # Stage 2A request used -- so Stage 2A requests are byte-for-byte unchanged.
    reasoning_effort: str | None = None


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
    # --- Alibaba, open weights, via Groq's free tier (TPM-limited, no daily cap).
    # NOT the dropped qwen2.5:7b above -- a newer generation and ~4x the size.
    # Groq lists it as a PREVIEW model, which can be withdrawn; OpenRouter serves
    # the same weights as qwen/qwen3.8-27b:free, so there is a fallback.
    "qwen27b": ModelSpec(
        key="qwen27b",
        provider="groq",
        api_id="qwen/qwen3.8-27b",
        input_usd_per_mtok=0.0,
        output_usd_per_mtok=0.0,
        supports_temperature=True,
    ),
    # --- NVIDIA, open weights, the largest free model available (550B total,
    # 55B active). Served direct from NVIDIA (build.nvidia.com) rather than via
    # OpenRouter, which avoids OpenRouter's 50-requests/day free cap. Model id
    # verified against NVIDIA's live /v1/models list on 2026-09-30.
    "nemotron": ModelSpec(
        key="nemotron",
        provider="nvidia",
        api_id="nvidia/nemotron-3-ultra-550b-a55b",
        input_usd_per_mtok=0.0,
        output_usd_per_mtok=0.0,
        supports_temperature=True,
    ),
    # --- Moonshot AI, open weights, via the NVIDIA key. Id verified against
    # NVIDIA's /v1/models on 2026-09-30. (DeepSeek v4.1 Flash was also trialled
    # for this slot and dropped: NVIDIA's endpoint returned empty content for every
    # structured-output request.)
    "kimi": ModelSpec(
        key="kimi",
        provider="nvidia",
        api_id="moonshotai/kimi-k3",
        input_usd_per_mtok=0.0,
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
    # --- Stage 2B Block D: the same gpt-oss at the two ends of its reasoning
    # setting. Groq's default, used for Stage 2A, is the middle ("medium").
    "gptoss120b_low": ModelSpec(
        key="gptoss120b_low",
        provider="groq",
        api_id="openai/gpt-oss-120b",
        input_usd_per_mtok=0.0,
        output_usd_per_mtok=0.0,
        supports_temperature=True,
        reasoning_effort="low",
    ),
    "gptoss120b_high": ModelSpec(
        key="gptoss120b_high",
        provider="groq",
        api_id="openai/gpt-oss-120b",
        input_usd_per_mtok=0.0,
        output_usd_per_mtok=0.0,
        supports_temperature=True,
        reasoning_effort="high",
    ),
    # --- Replacement for "gemini" in Stage 2. Gemini 3.8 Flash's free tier allows
    # 20 requests/day (AI Studio Rate Limit page, 2026-09-30); one model needs
    # ~2,208, i.e. ~110 days. 3.5 Flash Lite allows 500/day (~5 days), is still
    # Google's closed model, and was swapped in before any Gemini Stage 2 data
    # existed. Disclosed as a deviation from preregistration-1 Section 4.
    "gemini_lite": ModelSpec(
        key="gemini_lite",
        provider="gemini",
        api_id="gemini-3.5-flash-lite",
        input_usd_per_mtok=0.0,      # free tier
        output_usd_per_mtok=0.0,
        supports_temperature=True,
    ),
}

# The study roster: four models from four different companies -- OpenAI, NVIDIA,
# Moonshot, Google -- three of four open-weight. The same effect across all four
# rules out one company's quirk.
#
# Kimi took the fourth slot over Qwen 3.8 27B on the practice rounds: Qwen was
# fast (~30s/trial) but only 5/8 usable, including a mid-answer drift into
# Russian that broke JSON generation; Kimi was 3/3 usable but slow (~165s/trial).
# Reliability won, because every unusable trial is excluded before fitting. That
# rests on only 3 Kimi trials -- revisit if its remaining practice trials fail.
#
# qwen7b is DROPPED from the study: 75% competence failure in the pilot meant most
# of its trials were excluded before fitting. Its spec stays above only so the
# pilot rows that reference it remain interpretable.
CAPABILITY_ORDER = ["gptoss120b", "nemotron", "kimi", "gemini_lite"]

# Deviation 11 (docs/deviations-from-preregistration.md): gpt-oss-120b's Stage 2B blocks are
# served by Cerebras, which hosts the same open weights, because Groq's free daily cap would
# otherwise delay them to November. Set per process by the launcher (GPTOSS_PROVIDER), so
# Stage 2A, Stage 2C and Stage 5 -- the paired comparisons -- stay on Groq. reasoning_effort
# is pinned to "medium", Groq's default, so the setting is identical on both providers.
if os.getenv("GPTOSS_PROVIDER") == "cerebras":
    from dataclasses import replace as _replace
    MODELS["gptoss120b"] = _replace(MODELS["gptoss120b"], provider="cerebras",
                                    api_id="gpt-oss-120b", reasoning_effort="medium")

# Base URLs by provider. Ollama exposes an OpenAI-compatible endpoint, so one
# client code path serves local, OpenRouter, and Groq alike.
BASE_URLS = {
    "ollama": "http://localhost:11434/v1",
    "openrouter": "https://openrouter.ai/api/v1",
    "groq": "https://api.groq.com/openai/v1",
    "nvidia": "https://integrate.api.nvidia.com/v1",
    "cerebras": "https://api.cerebras.ai/v1",
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
        "nvidia": "NVIDIA_API_KEY",
        "cerebras": "CEREBRAS_API_KEY",
    }[provider]
    # A second Gemini key (a second person's free-tier account, with his consent; Google
    # Support confirmed this is permitted -- docs/deviations-from-preregistration.md, item 12).
    # Chosen per process, so each key serves exactly one run at a time.
    if provider == "gemini" and os.getenv("GEMINI_KEY_SLOT") == "2":
        env_var = "GEMINI_API_KEY_2"
    # A second Groq key (a second person's free-tier account, with consent; Groq Support
    # confirmed this is permitted -- item 13). Same provider, so no change to the design.
    if provider == "groq" and os.getenv("GROQ_KEY_SLOT") == "2":
        env_var = "GROQ_API_KEY_2"
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
