"""The analysis lock: the Stage 3 method, fingerprinted before it meets real data.

Same idea as the pre-registrations. docs/analysis-plan.md says in words how the
answers are turned into results; the files below are the code that does it. Once
locked, the fingerprint of all of them together is recorded here, and the confirmatory
analysis (analysis/stage2a.py) refuses to run on real Stage 2 data if any has changed.
Fixing a bug after the lock is allowed only as a recorded deviation, never silently.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LOCKED_FILES = [
    "docs/analysis-plan.md",
    "analysis/qre.py",
    "analysis/fit.py",
    "analysis/stage2a.py",
]
ANALYSIS_SHA256 = "22a26a68e2090c948062471098636bfa897a5b3278ba4570e2d7aeeeb61fccea"


def fingerprint() -> str:
    h = hashlib.sha256()
    for rel in LOCKED_FILES:
        h.update(rel.encode() + b"\0" + (ROOT / rel).read_bytes() + b"\0")
    return h.hexdigest()


def analysis_locked() -> bool:
    return ANALYSIS_SHA256 is not None and fingerprint() == ANALYSIS_SHA256
