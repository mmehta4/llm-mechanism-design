"""The fraction-slip correction, fixed in pre-registration 3 before any Stage 2C data.

A model that derives a fractional answer ("x = 683/60 ≈ 11.383") and writes it into a
number-only answer box keeps only part of it: the numerator (683), or numerator and
denominator run together (23215 for 232/15). Nemotron does this in 11% of Stage 2A Cournot
answers and in every practice answer to the extreme Cournot question, whose correct answer
is almost always an awkward fraction. Left uncorrected, the stage comparison would measure
how often the answer is a fraction, not how the model plays.

The rule is mechanical and applied identically to Stage 2A and Stage 2C answers in the
Stage 2C comparison. Read an answer as the fraction n/d when BOTH hold:

  1. the box holds n, or n and d written together (e.g. 232/15 -> 23215), for a fraction
     n/d that appears in the model's own reasoning; and
  2. the reasoning ends on that fraction: its last number is n/d's value (within 1%), or
     its last two numbers are n and d themselves.

Otherwise the answer is used exactly as written.
"""
from __future__ import annotations

import re

FRACTION = re.compile(r"(-?\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)")
NUMBER = re.compile(r"-?\d+(?:\.\d+)?")


def corrected(answer, reasoning: str) -> float | None:
    """The fraction the box was cut from, or None if the rule does not apply."""
    try:
        a = float(answer)
    except (TypeError, ValueError):
        return None
    nums = [float(x) for x in NUMBER.findall(reasoning or "")]
    if not nums:
        return None
    for n_txt, d_txt in reversed(FRACTION.findall(reasoning or "")):
        n, d = float(n_txt), float(d_txt)
        if d == 0:
            continue
        joined = n_txt.lstrip("-").isdigit() and d_txt.isdigit() and a == float(n_txt + d_txt)
        if not (a == n or joined):
            continue
        value = n / d
        ends_on_value = abs(nums[-1] - value) <= 0.01 * max(1.0, abs(value))
        ends_on_fraction = len(nums) >= 2 and nums[-2] == n and nums[-1] == d
        if ends_on_value or ends_on_fraction:
            return value
    return None


def scored(answer, reasoning: str) -> float | None:
    """The answer used in the Stage 2C comparison: corrected if the rule applies."""
    c = corrected(answer, reasoning)
    if c is not None:
        return c
    try:
        return float(answer)
    except (TypeError, ValueError):
        return None
