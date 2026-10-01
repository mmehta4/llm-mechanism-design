"""Stage 2A is running and registered: its questions must never change.

Fingerprint of every Stage 2A question -- play prompt, probe prompt, correct probe
answer and scored equilibrium, in plan order -- taken 2026-09-30 before any Stage 2B
code was written. If this fails, a change meant for Stage 2B has leaked into the
registered experiment.
"""
import hashlib

from experiments.stage2 import plan
from experiments.trial import equilibrium_for
from games import ALL_GAMES
from games.probes import probe_for

STAGE_2A_SHA256 = "df29a8528a4168e03f4eaf454f46df74cb822dbfd8d20d715186c645db867f62"


def test_stage2a_questions_unchanged():
    h = hashlib.sha256()
    for g, f, s, p in plan():
        spec = ALL_GAMES[g]
        params = spec.sampler(seed=s)
        probe_prompt, _, probe_correct = probe_for(g, f, **params)
        h.update("\x1e".join([
            g, f, str(s), str(p), spec.prompt(f, p, **params),
            probe_prompt, str(probe_correct), str(equilibrium_for(params, f)),
        ]).encode())
    assert h.hexdigest() == STAGE_2A_SHA256


def test_stage2a_games_unchanged():
    assert list(ALL_GAMES) == ["vickrey", "cournot", "repeated_pd", "public_goods"]
