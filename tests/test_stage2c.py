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


def test_preregistration_3_untouched():
    """Locked: editing docs/preregistration-3.md now stops every real Stage 2C run."""
    assert prereg3_locked() is True


def test_stage2c_box_is_neutral_and_shaped_like_stage2a():
    """Number-only, answer first, reasoning second: only the field's words change."""
    from games.deep import NumberAction
    from games.vickrey import BidAction
    neutral = NumberAction.model_json_schema()
    assert neutral["properties"]["number"]["type"] == "number"
    assert list(neutral["properties"]) == ["number", "reasoning"]
    assert list(BidAction.model_json_schema()["properties"]) == ["bid", "reasoning"]
    from openai.lib._pydantic import to_strict_json_schema
    text = str(to_strict_json_schema(NumberAction)).lower()   # exactly what is sent
    assert "description" not in to_strict_json_schema(NumberAction)
    for leak in ("bid", "sealed", "quantity", "produce", "contribut", "endowment", "auction"):
        assert leak not in text


def test_fraction_slip_correction():
    from analysis.slips import corrected, scored
    r = "x = (80.3/3 - 4)/2 = 68.3/6 = 683/60 ≈ 11.3833."
    assert abs(corrected(683, r) - 683 / 60) < 1e-9
    assert abs(corrected(23215, "so x = 232/15 ≈ 15.4667") - 232 / 15) < 1e-9   # slash dropped
    # a fraction used mid-way, but the reasoning ends elsewhere: left as written
    assert corrected(30, "best response is (90 - 30)/2, so I choose 30.") is None
    # an ordinary correct decimal answer is never changed
    assert corrected(11.3833, "x ≈ 11.3833") is None and scored(11.3833, "x ≈ 11.3833") == 11.3833
