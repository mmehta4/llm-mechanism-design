"""Stage 5 draft materials: the Stage 2A named PD plus one subsidy rule, nothing else."""
import pytest

from games import GAMES, repeated_pd
from games.subsidy import (PROBE, RULE, SUBSIDY_GAMES, SUBSIDY_PROBES, key_for, rational_play,
                           render, sample)


@pytest.mark.parametrize("w", [0, 1, 2])
def test_only_the_rule_is_added_to_the_stage_2a_question(w):
    p = repeated_pd.sample(7)
    original = repeated_pd.SPEC.prompt("named", w, **p)
    new = render(1.5, w, seed=7)
    rule = RULE.format(tau=1.5) + "\n"
    assert new.count(rule) == 1 and new.replace(rule, "") == original


def test_not_runnable_until_registered():
    assert not set(SUBSIDY_GAMES) & set(GAMES)


def test_same_draws_as_stage_2a():
    for s in range(20):
        a, b = repeated_pd.sample(s), sample(s, 3.0)
        assert all(a[k] == b[k] for k in ("T", "R", "P", "S", "n_rounds", "round_num"))


def test_rational_benchmark():
    assert [rational_play(t) for t in (0, 0.9, 1.5, 2.1, 10)] == ["D", "D", "mixed", "C", "C"]


def test_maths_check_requires_the_subsidy():
    _, _, answer = SUBSIDY_PROBES[(key_for(1.5), "named")]
    assert answer(**sample(1, 1.5)) == 1.5
    assert "1.5" in PROBE.format(**sample(1, 1.5))
