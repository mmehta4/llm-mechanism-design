"""Shared structure for all four games.

Every game exists in TWO framings with identical payoff mathematics:

    NAMED      -- standard vocabulary: "sealed-bid auction", "contribute to the pot"
    DISGUISED  -- same structure, every recognisable label stripped, new surface story

The whole project turns on that pair. These games appear thousands of times in
any model's training data, so strong play in the NAMED framing is ambiguous --
the model may have derived the equilibrium or merely recalled it. Stripping the
labels removes recall as an option, and the gap between the two framings is the
headline measurement:

    delta-lambda  =  lambda_named  -  lambda_disguised

A disguised twin is only valid if it is a GENUINE ISOMORPHISM.

    HOLD CONSTANT:  action space (same type, range, bounds)
                    payoff magnitudes (identical numbers)
                    information structure (same things known and unknown)
                    cognitive load (similar length and syntax)

    MAY CHANGE:     domain vocabulary, surface story, unit names

    MUST NOT:       add an inference step, change the number of reasoning steps,
                    use vocabulary that is itself hard, or make it longer

That last group is the failure mode. If the disguised version requires the model
to first work out THAT IT IS an allocation problem, an extra step has been added
-- and delta-lambda then measures reading comprehension rather than retrieval,
which silently invalidates the central result.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Type

from pydantic import BaseModel


class DisguisedPromptMissing(RuntimeError):
    """Raised when a disguised trial is requested but no twin has been written.

    Deliberately loud. A silent fallback to the named prompt would quietly
    destroy the experiment: every disguised trial would secretly be a named
    trial, delta-lambda would come out at zero, and nothing would look wrong.
    """


@dataclass(frozen=True)
class GameSpec:
    key: str
    named_prompt: str
    disguised_prompt: str | None      # None until written -- see docstring above
    action_model: Type[BaseModel]
    equilibrium: Callable[..., float]
    sampler: Callable[..., dict]

    def prompt(self, framing: str, **params) -> str:
        if framing == "named":
            return self.named_prompt.format(**params)
        if framing == "disguised":
            if self.disguised_prompt is None:
                raise DisguisedPromptMissing(
                    f"No disguised twin written for '{self.key}'. "
                    f"See games/base.py for the isomorphism criteria, and "
                    f"games/vickrey.py for a worked example."
                )
            return self.disguised_prompt.format(**params)
        raise ValueError(f"framing must be 'named' or 'disguised', got {framing!r}")

    def has_twin(self) -> bool:
        return self.disguised_prompt is not None
