"""Stage 2C plan: 138 per game, and paired question-for-question with Stage 2A."""
from collections import Counter

from experiments.stage2 import plan as plan_2a
from experiments.stage2c import N, plan, prereg3_locked
from games import GAMES


def test_138_per_game_552_per_model():
    p = plan()
    assert len(p) == 552
    assert set(Counter(g for g, *_ in p).values()) == {N} == {138}


def test_every_2c_question_matches_a_2a_question():
    """Same seed and same wording index as Stage 2A: identical numbers, three wordings."""
    a = {(g, s, w) for g, f, s, w in plan_2a() if f == "disguised"}
    for g, f, s, w in plan():
        assert (g.replace("_extreme", ""), s, w) in a


def test_extreme_questions_carry_the_same_numbers_as_2a():
    for g, f, s, w in plan()[:40]:
        base = g.replace("_extreme", "")
        p2a, p2c = GAMES[base].sampler(seed=s), GAMES[g].sampler(seed=s)
        for k in ("value", "a", "c", "endowment", "M", "n_rounds"):
            if k in p2a:
                assert p2a[k] == p2c[k]


def test_not_registered_yet():
    assert prereg3_locked() is False


def test_answer_box_accepts_fractions_so_nothing_is_cut_at_the_slash():
    """Nemotron writes 683/60; a number-only box kept 683 (deviation 6)."""
    from experiments.trial import deviation_of
    from games.deep import NumberAction
    a = NumberAction(number="683/60", reasoning="")
    assert abs(float(a.number) - 683 / 60) < 1e-9
    assert deviation_of(a.number, 683 / 60) == 0.0
