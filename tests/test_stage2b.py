"""Stage 2B plans and trap answers -- the stopping rules and the maths, pinned."""
from collections import Counter

import pytest

from config import MASTER_SEED
from experiments.stage2 import plan as plan_2a
from experiments.stage2b import PLANS, plan_B, plan_C, plan_D, plan_E, prereg2_locked
from experiments.trial import equilibrium_for
from games import GAMES, STRESS_GAMES
from games.probes import probe_for


def test_block_sizes():
    assert len(plan_B()) == 1104
    assert len(plan_C()) == 1104
    assert len(plan_D()) == 1104
    assert len(plan_E()) == 828


def test_every_cell_is_138_or_46():
    assert set(Counter((g, f) for g, f, *_ in plan_B()).values()) == {138}
    assert set(Counter((g, f) for g, f, *_ in plan_E()).values()) == {138}
    assert set(Counter((g, f) for g, f, *_ in plan_C()).values()) == {46}


def test_block_d_asks_stage_2a_questions_exactly():
    assert plan_D() == plan_2a()


@pytest.mark.parametrize("block", ["B", "C", "E"])
def test_named_and_disguised_paired(block):
    p = PLANS[block]()
    for game in {g for g, *_ in p}:
        named = {(s, w) for g, f, s, w in p if g == game and f == "named"}
        disguised = {(s, w) for g, f, s, w in p if g == game and f == "disguised"}
        assert named == disguised


def test_seeds_fresh_and_disjoint():
    seeds_2a = {s for _, _, s, _ in plan_2a()}
    blocks = {b: {s for _, _, s, _ in PLANS[b]()} for b in "BCE"}
    for b, seeds in blocks.items():
        assert seeds.isdisjoint(seeds_2a), b
        assert seeds.isdisjoint(range(1000, 1020)), b
    assert blocks["B"].isdisjoint(blocks["C"]) and blocks["C"].isdisjoint(blocks["E"])


def test_wordings_balanced_in_traps_and_endgame():
    for block in "BE":
        counts = Counter((g, f, w) for g, f, _, w in PLANS[block]())
        assert set(counts.values()) == {46}


def test_every_planned_game_exists_with_both_twins():
    for block in "BCDE":
        for g, f, s, w in PLANS[block](n=3, base=900_000):
            spec = GAMES[g]
            params = spec.sampler(seed=s)
            assert spec.prompt(f, w, **params)
            assert probe_for(g, f, **params)


def test_trap_answers():
    v = STRESS_GAMES["vickrey_trap"].sampler(seed=1)
    assert equilibrium_for(v, "named") == pytest.approx(v["value"] / 2)
    c = STRESS_GAMES["cournot_trap"].sampler(seed=1)
    assert equilibrium_for(c, "named") == pytest.approx((c["a"] - c["c"]) / 4)
    pd = STRESS_GAMES["repeated_pd_trap"].sampler(seed=1)
    assert equilibrium_for(pd, "named") == "C"
    assert equilibrium_for(pd, "disguised") == pd["coop"]
    pg = STRESS_GAMES["public_goods_trap"].sampler(seed=1)
    assert equilibrium_for(pg, "named") == pg["endowment"]


def test_traps_change_only_what_they_should():
    """Every trap wording is its Stage 2A twin with the trap edit and nothing else."""
    from games import ALL_GAMES
    v, vt = ALL_GAMES["vickrey"], STRESS_GAMES["vickrey_trap"]
    for f in ("named", "disguised"):
        for a, b in zip(v.prompts(f), vt.prompts(f)):
            assert b.replace("TWICE ", "") == a
    for key, trap in [("repeated_pd", "repeated_pd_trap"), ("public_goods", "public_goods_trap")]:
        assert GAMES[key].prompts("named") == GAMES[trap].prompts("named")
        assert GAMES[key].prompts("disguised") == GAMES[trap].prompts("disguised")


def test_endgame_history_in_each_framings_labels():
    spec = STRESS_GAMES["repeated_pd_round10"]
    p = spec.sampler(seed=3)
    named = spec.prompt("named", 0, **p)
    disguised = spec.prompt("disguised", 0, **p)
    assert "This is round 10" in named and "rounds 1 to 9, you both chose C" in named
    assert f"rounds 1 to 9, you both set {p['coop']}" in disguised
    assert " C " not in disguised.replace(p["coop"], "")
    assert equilibrium_for(p, "named") == "D"
    assert equilibrium_for(p, "disguised") == p["defect"]


def test_preregistration_2_untouched():
    """Locked: editing docs/preregistration-2.md now stops every real 2B run."""
    assert prereg2_locked() is True
