"""Stage 5 runner: levels, plan, gate rules, lock."""
from collections import Counter

import pytest

import experiments.stage5 as S5
from games import GAMES
from games.probes import probe_for
from games.subsidy import key_for


@pytest.fixture
def lam(monkeypatch):
    def set_(model, value):
        monkeypatch.setitem(S5.LAMBDA_HAT, model, value)
    return set_


def test_levels_and_gate_rules(lam):
    lam("nemotron", 0.154)
    assert S5.levels_for("nemotron") == (0.0, 1.5, 2.5, 16.2)
    lam("nemotron", 0.01)                        # floor: τ* capped
    assert S5.levels_for("nemotron")[-1] == 50.0
    lam("nemotron", 5.0)                         # ceiling: no separate derived level
    assert S5.levels_for("nemotron") == (0.0, 1.5, 2.5)
    assert S5.LAMBDA_CEILING == pytest.approx(3.662, abs=1e-3)


def test_plan_is_100_per_level_balanced_across_wordings(lam):
    lam("kimi", 0.3)
    p = S5.plan("kimi")
    assert len(p) == 400 and len(set(p)) == 400
    for tau in S5.levels_for("kimi"):
        w = Counter(t[3] for t in p if t[0] == key_for(tau))
        assert sorted(w.values()) == [33, 33, 34]


@pytest.fixture
def clean_registry():
    """register() writes into the shared tables; undo it so other tests see them untouched."""
    from games.probes import PROBES
    g, p = dict(GAMES), dict(PROBES)
    yield
    GAMES.clear(); GAMES.update(g); PROBES.clear(); PROBES.update(p)


def test_registered_questions_render_with_the_right_maths_check(lam, clean_registry):
    lam("kimi", 0.3)
    S5.register(S5.levels_for("kimi"))
    key = key_for(S5.levels_for("kimi")[-1])
    params = GAMES[key].sampler(seed=S5.SEED0)
    prompt, _, correct = probe_for(key, "named", **params)
    assert correct == pytest.approx(params["tau"]) and f"{params['tau']:.1f}" in prompt


def test_refuses_without_lambda_or_lock(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["stage5.py", "--model", "gemini_lite"])
    monkeypatch.delitem(S5.LAMBDA_HAT, "gemini_lite", raising=False)
    assert S5.main() == 1 and "no fitted" in capsys.readouterr().out
    monkeypatch.setitem(S5.LAMBDA_HAT, "gemini_lite", 0.5)
    monkeypatch.setattr(S5, "PREREG4_SHA256", None)
    assert S5.main() == 1 and "not registered" in capsys.readouterr().out
