"""LLM agent: send a prompt, get a structured action back.

One client path serves local Ollama, OpenRouter and Groq, because all three expose
an OpenAI-compatible endpoint.

Parse failures are CAUGHT AND RECORDED rather than raised. That is deliberate: a
model replying "I'd bid around 68" is data about the model, not an exception. If
these crashed the run we would learn nothing from them, and if they were silently
coerced to a number we would learn something false.
"""
from __future__ import annotations

import time
from typing import Type

from openai import OpenAI
from pydantic import BaseModel

import config
from agents.base import AgentResponse


class LLMAgent:
    def __init__(self, model_key: str):
        self.spec = config.MODELS[model_key]
        self.client = OpenAI(
            base_url=config.BASE_URLS[self.spec.provider],
            api_key=config.api_key(self.spec.provider),
        )

    def act(self, prompt: str, action_model: Type[BaseModel]) -> AgentResponse:
        started = time.perf_counter()
        try:
            completion = self.client.chat.completions.parse(
                model=self.spec.api_id,
                messages=[{"role": "user", "content": prompt}],
                response_format=action_model,
            )
        except Exception as e:
            return AgentResponse(
                action=None, reasoning="", raw="", parse_ok=False,
                latency_s=time.perf_counter() - started,
                model_api_id=self.spec.api_id,
                error=f"{type(e).__name__}: {e}",
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
        )

    def cost_usd(self, r: AgentResponse) -> float:
        if not (r.input_tokens and r.output_tokens):
            return 0.0
        return (
            r.input_tokens / 1_000_000 * self.spec.input_usd_per_mtok
            + r.output_tokens / 1_000_000 * self.spec.output_usd_per_mtok
        )
