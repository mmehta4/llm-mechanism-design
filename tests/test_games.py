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
    for key in ["cournot", "repeated_pd", "public_goods"]:
        spec = ALL_GAMES[key]
        with pytest.raises(DisguisedPromptMissing):
            spec.prompt("disguised", **spec.sampler(seed=1))


def test_twin_progress():
    """Fails until all four twins are written. Delete this test when done."""
    missing = [k for k, s in ALL_GAMES.items() if not s.has_twin()]
    assert not missing, f"disguised twins still to write: {missing}"
