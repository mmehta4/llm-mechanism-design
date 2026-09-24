"""Tests for the game specs and their framings."""
import pytest

from games import ALL_GAMES, DisguisedPromptMissing


def test_all_four_games_present():
    assert set(ALL_GAMES) == {"vickrey", "cournot", "repeated_pd", "public_goods"}


@pytest.mark.parametrize("key", list(ALL_GAMES))
def test_named_prompt_renders(key):
    spec = ALL_GAMES[key]
    params = spec.sampler(seed=1)
    text = spec.prompt("named", **params)
    assert len(text) > 50 and "{" not in text


@pytest.mark.parametrize("key", list(ALL_GAMES))
def test_sampler_is_deterministic_under_seed(key):
    """Same seed must give the same parameters, or nothing is reproducible."""
    spec = ALL_GAMES[key]
    assert spec.sampler(seed=42) == spec.sampler(seed=42)


def test_vickrey_twin_is_isomorphic():
    """The worked example: both framings must carry the same value and equilibrium."""
    spec = ALL_GAMES["vickrey"]
    p = spec.sampler(seed=7)
    named, disguised = spec.prompt("named", **p), spec.prompt("disguised", **p)

    assert str(p["value"]) in named and str(p["value"]) in disguised
    assert p["equilibrium"] == p["value"]
    # the disguise must not leak auction vocabulary
    for word in ["auction", "bid", "bidder", "bidding"]:
        assert word not in disguised.lower(), f"'{word}' leaked into the disguised prompt"


def test_missing_twins_fail_loudly():
    """A missing disguised prompt must RAISE, never silently fall back.

    A silent fallback would make every disguised trial secretly a named trial:
    delta-lambda would come out at zero and nothing would look wrong.
    """
    for key, spec in ALL_GAMES.items():
        if spec.has_twin():
            continue
        with pytest.raises(DisguisedPromptMissing):
            spec.prompt("disguised", **spec.sampler(seed=1))


def test_twin_progress():
    """Fails until all four twins are written. Delete this test when done."""
    missing = [k for k, s in ALL_GAMES.items() if not s.has_twin()]
    assert not missing, f"disguised twins still to write: {missing}"


def test_cournot_twin_is_isomorphic():
    """Both framings must carry the same numbers and leak no economics vocabulary."""
    spec = ALL_GAMES["cournot"]
    p = spec.sampler(seed=3)
    named, disguised = spec.prompt("named", **p), spec.prompt("disguised", **p)

    for value in [str(p["a"]), str(p["b"]), str(p["c"])]:
        assert value in named and value in disguised

    leaks = ["firm", "profit", "payoff", "market", "produce", "price", "product"]
    for word in leaks:
        assert word not in disguised.lower(), f"'{word}' leaked into the disguised prompt"

    # both framings must state the no-visibility condition, or the disguised
    # version is easier than the named one and delta-lambda is biased downward
    assert "sees the other" in named and "sees the other" in disguised


def test_public_goods_twin_is_isomorphic():
    """Both framings carry the same numbers and leak no cooperation vocabulary."""
    spec = ALL_GAMES["public_goods"]
    p = spec.sampler(seed=5)
    named, disguised = spec.prompt("named", **p), spec.prompt("disguised", **p)

    for value in [str(p["endowment"]), str(p["M"]), str(p["n_total"])]:
        assert value in named and value in disguised

    # words that pre-load a cooperation frame before any reasoning happens
    leaks = ["contribute", "pot", "share", "player", "public", "common", "donate"]
    for word in leaks:
        assert word not in disguised.lower(), f"'{word}' leaked into the disguised prompt"

    # both framings must state the two facts needed to compute the marginal return
    for text in (named, disguised):
        assert "evenly" in text or "equally" in text
        assert "keep whatever" in text


def test_public_goods_action_bounds():
    from games.public_goods import is_valid_action
    assert is_valid_action(0.0, 20.0)
    assert is_valid_action(20.0, 20.0)
    assert not is_valid_action(25.0, 20.0)      # more than you hold
    assert not is_valid_action(-1.0, 20.0)
