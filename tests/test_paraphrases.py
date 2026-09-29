"""Paraphrases: same facts, same numbers, different words -- and paired across framings.

These tests encode the rule "reword and reorder, never add or drop a fact" as far
as a test can. They cannot prove two sentences mean the same thing, but they do
catch the failures that actually happen: a dropped number, a leaked label, an
unfilled placeholder, a paraphrase identical to another.
"""
import pytest

from games import ALL_GAMES

# words that would pre-load the named frame into a disguised prompt
LEAKS = {
    "vickrey": ["auction", "bid", "bidder"],
    "cournot": ["firm", "profit", "payoff", "market", "produce", "price", "product"],
    "repeated_pd": ["cooperate", "defect", "betray", "honest", "cheat", "loyal",
                    "share", "hoard", "selfish", "fair", "trust", "punish", "player"],
    "public_goods": ["contribute", "pot", "share", "player", "public", "common", "donate"],
}

# sampled values every paraphrase of a cell must state
NUMBERS = {
    "vickrey": ["value"],
    "cournot": ["a", "b", "c"],
    "repeated_pd": ["T", "R", "P", "S", "n_rounds"],
    "public_goods": ["endowment", "M", "n_total"],
}

GAMES = list(ALL_GAMES)
FRAMINGS = ["named", "disguised"]


@pytest.mark.parametrize("game", GAMES)
def test_paired_counts(game):
    """Same number of paraphrases in each framing, so index k is comparable."""
    spec = ALL_GAMES[game]
    assert spec.n_paraphrases("named") == spec.n_paraphrases("disguised") >= 3


@pytest.mark.parametrize("game", GAMES)
@pytest.mark.parametrize("framing", FRAMINGS)
def test_every_paraphrase_renders_and_carries_the_numbers(game, framing):
    spec = ALL_GAMES[game]
    for seed in (1, 7, 1000):
        p = spec.sampler(seed=seed)
        for k in range(spec.n_paraphrases(framing)):
            text = spec.prompt(framing, k, **p)
            assert "{" not in text and "}" not in text, f"unfilled placeholder in {game}/{framing}/{k}"
            for key in NUMBERS[game]:
                assert str(p[key]) in text, f"{game}/{framing}/{k} dropped {key}={p[key]}"


@pytest.mark.parametrize("game", GAMES)
@pytest.mark.parametrize("framing", FRAMINGS)
def test_paraphrases_are_distinct(game, framing):
    spec = ALL_GAMES[game]
    p = spec.sampler(seed=1)
    texts = [spec.prompt(framing, k, **p) for k in range(spec.n_paraphrases(framing))]
    assert len(set(texts)) == len(texts)


@pytest.mark.parametrize("game", GAMES)
def test_disguised_paraphrases_leak_nothing(game):
    spec = ALL_GAMES[game]
    p = spec.sampler(seed=11)
    for k in range(spec.n_paraphrases("disguised")):
        text = spec.prompt("disguised", k, **p).lower()
        for word in LEAKS[game]:
            assert word not in text, f"'{word}' leaked into {game}/disguised/{k}"


@pytest.mark.parametrize("game", GAMES)
@pytest.mark.parametrize("framing", FRAMINGS)
def test_every_paraphrase_states_simultaneity_or_privacy(game, framing):
    """The information structure must survive rewording in every variant."""
    spec = ALL_GAMES[game]
    p = spec.sampler(seed=3)
    for k in range(spec.n_paraphrases(framing)):
        t = spec.prompt(framing, k, **p).lower()
        assert any(m in t for m in ["simultaneous", "same time", "same moment",
                                    "privately", "sealed", "sees the other"]), (
            f"{game}/{framing}/{k} lost its information structure")


def test_pd_horizon_is_common_knowledge_in_every_paraphrase():
    """Backward induction needs the horizon to be COMMON knowledge, not just known."""
    spec = ALL_GAMES["repeated_pd"]
    p = spec.sampler(seed=3)
    for framing in FRAMINGS:
        for k in range(spec.n_paraphrases(framing)):
            assert "known to both" in spec.prompt(framing, k, **p)


def test_pd_variant_one_lists_defection_first_in_both_framings():
    """Variant 1 exists to measure first-listed-is-default; it must actually flip."""
    spec = ALL_GAMES["repeated_pd"]
    p = spec.sampler(seed=3)
    named = spec.prompt("named", 1, **p)
    assert named.index("choose D") < named.index("choose C")
    disguised = spec.prompt("disguised", 1, **p)
    assert disguised.index(f"position {p['defect']}") < disguised.index(f"position {p['coop']}")


def test_out_of_range_paraphrase_raises():
    spec = ALL_GAMES["vickrey"]
    with pytest.raises(IndexError):
        spec.prompt("named", 99, **spec.sampler(seed=1))
