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
    """A game in both framings, each with a primary prompt and paraphrases.

    Paraphrases answer one specific objection: that a framing effect is really a
    WORDING effect. If behaviour moves about as much across paraphrases within a
    framing as it moves between framings, the framing result is not real.

    They are PAIRED across framings -- paraphrase 1 is the same kind of rewording in
    the named and disguised versions, paraphrase 2 the same reordering. So a
    wording sensitivity that shows up identically in both framings cancels out of
    delta-lambda, while one that shows up in only one framing is itself a finding.

    Rule for writing them: reword and reorder, never add or drop a fact. The
    lesson from building the twins applies here too -- making one version more
    explicit than another makes it easier.
    """
    key: str
    named_prompt: str
    disguised_prompt: str | None      # None until written -- see docstring above
    action_model: Type[BaseModel]
    equilibrium: Callable[..., float]
    sampler: Callable[..., dict]
    named_variants: tuple[str, ...] = ()
    disguised_variants: tuple[str, ...] = ()

    def prompts(self, framing: str) -> tuple[str, ...]:
        """Every template for this framing; index 0 is the primary prompt."""
        if framing == "named":
            return (self.named_prompt,) + self.named_variants
        if framing == "disguised":
            if self.disguised_prompt is None:
                raise DisguisedPromptMissing(
                    f"No disguised twin written for '{self.key}'. "
                    f"See games/base.py for the isomorphism criteria, and "
                    f"games/vickrey.py for a worked example."
                )
            return (self.disguised_prompt,) + self.disguised_variants
        raise ValueError(f"framing must be 'named' or 'disguised', got {framing!r}")

    def n_paraphrases(self, framing: str) -> int:
        return len(self.prompts(framing))

    def prompt(self, framing: str, paraphrase_idx: int = 0, **params) -> str:
        templates = self.prompts(framing)
        if not 0 <= paraphrase_idx < len(templates):
            raise IndexError(
                f"{self.key}/{framing} has {len(templates)} paraphrases; "
                f"index {paraphrase_idx} does not exist"
            )
        # Values that must differ by framing -- the PD endgame history is written in
        # C/D or in the disguised X/Y labels -- arrive under "_by_framing".
        params = {**params, **params.get("_by_framing", {}).get(framing, {})}
        return templates[paraphrase_idx].format(**params)

    def has_twin(self) -> bool:
        return self.disguised_prompt is not None
