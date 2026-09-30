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


def test_block_not_done_while_refusals_remain(tmp_path, monkeypatch):
    """A pass that leaves server-refused questions must not report the block done."""
    from experiments import stage2
    rows = iter([{"verdict": "INFRA_FAIL", "infra": "overloaded"},
                 {"verdict": "AT_EQUILIBRIUM", "infra": None}])

    def fake_trial(game, framing, model, seed, paraphrase_idx):
        r = next(rows)
        return {"game": game, "framing": framing, "seed": seed,
                "paraphrase_idx": paraphrase_idx, "total_latency_s": 0.0, **r}

    monkeypatch.setattr(stage2, "run_trial", fake_trial)
    plan = [("vickrey", "named", 1, 0), ("vickrey", "named", 2, 0)]
    out = tmp_path / "run.csv"
    assert stage2.run_plan("m", plan, out) == stage2.EXIT_INFRA
    rows = iter([{"verdict": "AT_EQUILIBRIUM", "infra": None}])
    assert stage2.run_plan("m", plan, out) == stage2.EXIT_DONE


def test_daily_limit_refusals_never_set_a_question_aside(tmp_path):
    """Hourly probes against a spent daily cap must not count against the question."""
    import csv as _csv
    from experiments.stage2 import MAX_TRIES_PER_TRIAL, infra_attempts
    from experiments.trial_log import FIELDS
    out = tmp_path / "run.csv"
    with out.open("w", newline="") as f:
        w = _csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        for _ in range(MAX_TRIES_PER_TRIAL + 5):
            w.writerow({"game": "vickrey", "framing": "named", "seed": 1,
                        "paraphrase_idx": 0, "verdict": "INFRA_FAIL", "infra": "quota"})
        w.writerow({"game": "vickrey", "framing": "named", "seed": 2,
                    "paraphrase_idx": 0, "verdict": "INFRA_FAIL", "infra": "overloaded"})
    counts = infra_attempts(out)
    assert counts[("vickrey", "named", 1, 0)] == 0
    assert counts[("vickrey", "named", 2, 0)] == 1
