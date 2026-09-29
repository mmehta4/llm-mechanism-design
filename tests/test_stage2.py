"""The Stage 2 plan is the stopping rule in code form -- pin it down."""
from collections import Counter

from config import MASTER_SEED
from experiments.stage2 import N_PER_CELL, plan, prereg_intact


def test_exactly_138_per_cell():
    cells = Counter((g, f) for g, f, _, _ in plan())
    assert len(cells) == 8
    assert set(cells.values()) == {N_PER_CELL} == {138}


def test_named_and_disguised_share_seeds_and_wordings():
    p = plan()
    for game in {g for g, *_ in p}:
        named = {(s, w) for g, f, s, w in p if g == game and f == "named"}
        disguised = {(s, w) for g, f, s, w in p if g == game and f == "disguised"}
        assert named == disguised


def test_wordings_balanced():
    counts = Counter((g, f, w) for g, f, _, w in plan())
    assert set(counts.values()) == {46}


def test_fresh_seeds_disjoint_from_practice_runs():
    seeds = {s for _, _, s, _ in plan()}
    assert min(seeds) == MASTER_SEED
    assert seeds.isdisjoint(range(1000, 1020))


def test_order_fixed_and_interleaved():
    p = plan()
    assert p == plan()
    first_50 = {f for _, f, _, _ in p[:50]}
    assert first_50 == {"named", "disguised"}


def test_preregistration_untouched():
    assert prereg_intact()
