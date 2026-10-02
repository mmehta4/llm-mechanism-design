"""Stage 2C analysis: decoding, the PD λ scale, the paired statistics, and the lock."""
import math

import numpy as np
import pytest

from analysis import stage2c as A
from analysis.qre import LAMBDA, pd_logprob
from experiments.stage2c import plan
from games import GAMES


def _row(game, seed, answer, reasoning="", verdict="AT_EQUILIBRIUM", framing="disguised", w=0):
    p = GAMES[game].sampler(seed=seed)
    return A.enrich({"game": game, "framing": framing, "seed": str(seed), "paraphrase_idx": str(w),
                     "verdict": verdict, "observed_action": answer, "equilibrium": p["equilibrium"],
                     "play_reasoning": reasoning, "play_prompt": ""})


@pytest.mark.parametrize("fam", ["vickrey", "cournot", "public_goods"])
def test_the_extreme_equilibrium_decodes_to_the_2a_equilibrium(fam):
    for _, _, s, w in [t for t in plan() if t[0] == f"{fam}_extreme"][:25]:
        x = GAMES[f"{fam}_extreme"].sampler(seed=s)["equilibrium"]
        _, p2a, _, ans = A.decode(_row(f"{fam}_extreme", s, x))
        assert ans == pytest.approx(p2a["equilibrium"], abs=1e-9)


def test_pd_extreme_labels_are_the_2a_disguised_labels():
    for _, _, s, _ in [t for t in plan() if t[0] == "repeated_pd_extreme"][:40]:
        p2a, p2c = GAMES["repeated_pd"].sampler(seed=s), GAMES["repeated_pd_extreme"].sampler(seed=s)
        assert (p2a["coop"], p2a["defect"]) == (p2c["coop"], p2c["defect"])


def test_pd_fit_on_original_payoffs_is_twice_the_shifted_lambda():
    """Pre-registration 3: a 2C PD λ is multiplied by 2. Fitting on the 2A payoffs at λ
    equals fitting on the 2u − 4 payoffs at λ/2."""
    orig = dict(T=5.0, R=3.0, P=1.0, S=0.0)
    shifted = {k: 2 * v - 4 for k, v in orig.items()}
    lam = LAMBDA[(LAMBDA > 0.01) & (LAMBDA < 100)]
    for coop in (True, False):
        assert np.allclose(pd_logprob(orig, coop, lam), pd_logprob(shifted, coop, lam / 2), atol=1e-9)


def test_fraction_slip_is_corrected_and_scored_in_both_stages():
    s = 20260931
    p = GAMES["cournot_extreme"].sampler(seed=s)
    # x* = (K - 12) / 6 = (10K - 120) / 60 exactly; box the numerator only
    n = round(10 * p["K"] - 120)
    r = _row("cournot_extreme", s, n, f"so x = {n}/60", verdict="STRATEGIC_GAP")
    assert n / 60 == pytest.approx(p["equilibrium"])
    assert r["slip"] and r["correct"] and not r["correct_raw"]


def test_conversion_slip_is_counted_only_when_wrong():
    s = 20260931
    p = GAMES["vickrey_extreme"].sampler(seed=s)
    r = _row("vickrey_extreme", s, p["value"], verdict="STRATEGIC_GAP")
    assert r["conversion"] and not r["correct"]
    ok = _row("vickrey_extreme", s, p["equilibrium"])
    assert ok["correct"] and not ok["conversion"]


def test_strict_tolerance_is_stricter_for_vickrey():
    s = 20260931
    p = GAMES["vickrey_extreme"].sampler(seed=s)
    r = _row("vickrey_extreme", s, p["equilibrium"] + 0.4)      # offer off by 1.2
    assert r["correct"] and not r["correct_strict"]


def test_mcnemar_and_interval():
    assert A.mcnemar_exact(0, 0) == 1.0
    assert A.mcnemar_exact(10, 0) == pytest.approx(2 * 0.5 ** 10)
    d, lo, hi = A.paired_diff_ci(50, 30, 10, 10)
    assert d == pytest.approx(0.2) and lo < 0.2 < hi
    d, lo, hi = A.paired_diff_ci(100, 0, 0, 0)
    assert d == 0 and lo < 0 < hi


def test_pairs_need_both_answers_to_count():
    s = 20260931
    x = _row("vickrey_extreme", s, GAMES["vickrey_extreme"].sampler(seed=s)["equilibrium"])
    n_ok = _row("vickrey", s, GAMES["vickrey"].sampler(seed=s)["equilibrium"], framing="named")
    n_bad = dict(n_ok, kept=False)
    assert sum(A.table([(n_ok, None, x)], "normal", "correct")) == 1
    assert sum(A.table([(n_bad, None, x)], "normal", "correct")) == 0
    assert sum(A.table([(n_ok, None, x)], "disguised", "correct")) == 0


def test_pooled_mcnemar_sums_discordant_pairs_over_models():
    s = 20260931
    eq = GAMES["vickrey"].sampler(seed=s)["equilibrium"]
    good = _row("vickrey", s, eq, framing="named")
    bad = _row("vickrey", s, eq + 10, framing="named", verdict="STRATEGIC_GAP")
    x = _row("vickrey_extreme", s, GAMES["vickrey_extreme"].sampler(seed=s)["equilibrium"])
    for r in (good, bad, x):
        r["conv_ok"] = r["correct"] or r["conversion"]
    by_model = {"m1": {"vickrey": [(bad, None, x)] * 6}, "m2": {"vickrey": [(bad, None, x)] * 4}}
    lines = A.comparison(by_model, "normal", "correct", "t")
    pooled = [l for l in lines if l.startswith("| **all models** | Vickrey")][0]
    assert f"| {A.mcnemar_exact(0, 10):.3g} |" in pooled


def test_real_data_is_refused_until_locked(monkeypatch, capsys):
    monkeypatch.setattr(A, "STAGE2C_ANALYSIS_SHA256", None)
    monkeypatch.setattr("sys.argv", ["stage2c.py", "--model", "nemotron"])
    assert A.main() == 1
    assert "not locked" in capsys.readouterr().out


def test_the_stage2c_analysis_is_locked():
    """Any edit to analysis/stage2c.py, analysis/slips.py or docs/analysis-plan-2c.md
    after the lock must be a recorded deviation, never silent."""
    assert A.stage2c_locked()
