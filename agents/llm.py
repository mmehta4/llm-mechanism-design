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


# Transient on free-tier hosted models: rate limits and capacity spikes. Observed
# immediately on the first real Gemini call -- a 503 "experiencing high demand".
# These are infrastructure, not data: retrying is correct, and silently recording
# them as failures would understate the model and corrupt the parse-failure rate.
RETRY_STATUS = {408, 409, 425, 429, 500, 502, 503, 504}
MAX_ATTEMPTS = 5
BASE_BACKOFF_S = 2.0


def _is_transient(exc: Exception) -> bool:
    code = getattr(exc, "status_code", None)
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
        )

    def act(self, prompt: str, action_model: Type[BaseModel]) -> AgentResponse:
        started = time.perf_counter()
        kwargs = dict(
            model=self.spec.api_id,
            messages=[{"role": "user", "content": prompt}],
            response_format=action_model,
        )

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
                extra={"attempts": attempts},
            )

        latency = time.perf_counter() - started
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
