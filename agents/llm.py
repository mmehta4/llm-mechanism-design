"""LLM agent: send a prompt, get a structured action back.

One client path serves local Ollama, OpenRouter and Groq, because all three expose
an OpenAI-compatible endpoint.

Parse failures are CAUGHT AND RECORDED rather than raised. That is deliberate: a
model replying "I'd bid around 68" is data about the model, not an exception. If
these crashed the run we would learn nothing from them, and if they were silently
coerced to a number we would learn something false.
"""
from __future__ import annotations

import random
import time
from typing import Type

from openai import OpenAI
from pydantic import BaseModel

import config
from agents.base import AgentResponse
from agents.pacer import TokenPacer

# One pacer per provider, shared across agents, since the limit is per account.
_PACERS: dict[str, TokenPacer] = {}

# Request-per-minute caps that bind before the token cap (AI Studio Rate Limit
# page, 2026-09-30: Gemini 3.5 Flash Lite free tier = 15 RPM).
RPM_LIMITS = {"gemini": 15}


def pacer_for(provider: str) -> TokenPacer | None:
    """Local inference is unmetered, so it needs no pacing."""
    if provider in config.NO_KEY_PROVIDERS:
        return None
    if provider not in _PACERS:
        _PACERS[provider] = TokenPacer(requests_per_minute=RPM_LIMITS.get(provider))
    return _PACERS[provider]


# Transient on free-tier hosted models: rate limits and capacity spikes. Observed
# immediately on the first real Gemini call -- a 503 "experiencing high demand".
# These are infrastructure, not data: retrying is correct, and silently recording
# them as failures would understate the model and corrupt the parse-failure rate.
RETRY_STATUS = {408, 409, 425, 429, 500, 502, 503, 504}
MAX_ATTEMPTS = 5
REQUEST_TIMEOUT_S = 420
BASE_BACKOFF_S = 2.0


def infra_kind(exc: Exception | None) -> str | None:
    """Classify a failure that happened BEFORE the model ever saw the question.

    These are infrastructure, not behaviour, and must never be recorded as the model
    failing. Observed on the Gemini practice round: six trials were logged as
    PARSE_FAIL -- "the model gave an unreadable answer" -- when Google had in fact
    refused the request outright. The model answered 2/2 of the questions it
    actually received.
    """
    if exc is None:
        return None
    code = getattr(exc, "status_code", None)
    msg = str(exc).lower()
    # Google says "exceeded your current quota" for BOTH its per-minute and per-day
    # caps; only the quotaId tells them apart. Groq says "tokens per day (TPD)".
    if code == 429 and "perminute" in msg:
        return "rate_limit"
    if code == 429 and any(s in msg for s in ("quota", "per day", "(tpd)", "(rpd)")):
        return "quota"            # a DAILY cap -- will not clear by retrying
    if code == 429:
        return "rate_limit"       # a per-minute cap -- clears in seconds
    if code in (500, 502, 503, 504):
        return "overloaded"
    if type(exc).__name__ in {"APIConnectionError", "APITimeoutError"}:
        return "connection"
    return None


def _is_transient(exc: Exception) -> bool:
    code = getattr(exc, "status_code", None)
    # A daily quota does not clear on a timescale any backoff can wait out.
    # Retrying it five times -- as this function used to -- only burns more of
    # the cap: ~180 of the ~200 requests Gemini logged on the practice day were
    # retries against an already-exhausted quota.
    if infra_kind(exc) == "quota":
        return False
    if code in RETRY_STATUS:
        return True
    name = type(exc).__name__
    return name in {"APIConnectionError", "APITimeoutError", "RateLimitError",
                    "InternalServerError", "APIStatusError"}


class LLMAgent:
    def __init__(self, model_key: str):
        self.spec = config.MODELS[model_key]
        self.client = OpenAI(
            base_url=config.BASE_URLS[self.spec.provider],
            api_key=config.api_key(self.spec.provider),
            # A request that stalls must fail and be retried, not hang: Stage 2's
            # first Nemotron run sat on one call for 8+ minutes while the endpoint
            # answered fresh requests in under a second. The slowest legitimate
            # call seen is Kimi at ~3 min, so 7 min only ever cuts a dead request.
            timeout=REQUEST_TIMEOUT_S,
            # retrying is done below, where it is counted and classified; the SDK's
            # own silent retries would hide attempts from the log
            max_retries=0,
        )
        self.pacer = pacer_for(self.spec.provider)
        # rough per-call estimate, refined from observed usage as the run proceeds
        self._est_tokens = 1100

    def act(self, prompt: str, action_model: Type[BaseModel]) -> AgentResponse:
        started = time.perf_counter()
        kwargs = dict(
            model=self.spec.api_id,
            messages=[{"role": "user", "content": prompt}],
            response_format=action_model,
        )

        if self.pacer is not None:
            self.pacer.wait_for(self._est_tokens)

        completion, last_error, attempts = None, None, 0
        for attempt in range(1, MAX_ATTEMPTS + 1):
            attempts = attempt
            try:
                try:
                    completion = self.client.chat.completions.parse(**kwargs)
                except (AttributeError, NotImplementedError, TypeError):
                    # Gemini's compatibility layer documents the .beta path; Ollama
                    # and Groq serve the stable one. Try stable first and fall back,
                    # rather than branching on provider.
                    completion = self.client.beta.chat.completions.parse(**kwargs)
                break
            except Exception as e:
                last_error = e
                if attempt == MAX_ATTEMPTS or not _is_transient(e):
                    break
                # exponential backoff with jitter, so parallel workers do not
                # synchronise their retries into a second thundering herd
                delay = BASE_BACKOFF_S * (2 ** (attempt - 1))
                time.sleep(delay + random.uniform(0, delay * 0.3))

        if completion is None:
            return AgentResponse(
                action=None, reasoning="", raw="", parse_ok=False,
                latency_s=time.perf_counter() - started,
                model_api_id=self.spec.api_id,
                error=f"{type(last_error).__name__}: {last_error}",
                extra={"attempts": attempts, "infra": infra_kind(last_error)},
            )

        latency = time.perf_counter() - started
        if self.pacer is not None and completion.usage is not None:
            actual = getattr(completion.usage, "total_tokens", None) or self._est_tokens
            self.pacer.record(actual)
            # ease the estimate toward reality so pacing self-corrects
            self._est_tokens = int(0.7 * self._est_tokens + 0.3 * actual)

        message = completion.choices[0].message
        raw = message.content or ""
        parsed = getattr(message, "parsed", None)
        usage = completion.usage

        if parsed is None:
            return AgentResponse(
                action=None, reasoning="", raw=raw, parse_ok=False,
                latency_s=latency, model_api_id=self.spec.api_id,
                error="structured output returned no parsed object",
                input_tokens=getattr(usage, "prompt_tokens", None),
                output_tokens=getattr(usage, "completion_tokens", None),
                extra={"attempts": attempts},
            )

        return AgentResponse(
            action=parsed,
            reasoning=getattr(parsed, "reasoning", ""),
            raw=raw,
            parse_ok=True,
            latency_s=latency,
            model_api_id=self.spec.api_id,
            input_tokens=getattr(usage, "prompt_tokens", None),
            output_tokens=getattr(usage, "completion_tokens", None),
            extra={"attempts": attempts},
        )

    def cost_usd(self, r: AgentResponse) -> float:
        if not (r.input_tokens and r.output_tokens):
            return 0.0
        return (
            r.input_tokens / 1_000_000 * self.spec.input_usd_per_mtok
            + r.output_tokens / 1_000_000 * self.spec.output_usd_per_mtok
        )
