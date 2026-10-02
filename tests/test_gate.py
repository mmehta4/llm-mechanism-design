"""Decision gate: on simulated QRE players the held-out calibration must pass."""
import numpy as np

from analysis import gate
from analysis.qre import sample_answer
from games import GAMES
from experiments.trial import at_equilibrium, deviation_of


def _synthetic(lams, n=90, seed=0):
    rng = np.random.default_rng(seed)
    rows = []
    for game, lam in lams.items():
        for k in range(n):
            p = GAMES[game].sampler(seed=1000 + k)
            a = sample_answer(game, p, "named", lam, rng)
            eq = p.get("equilibrium_named", p["equilibrium"])
            ok = at_equilibrium(deviation_of(a, eq), eq)
            rows.append({"game": game, "framing": "named", "paraphrase_idx": str(k % 3),
                         "params": p, "observed_action": a,
                         "verdict": "AT_EQUILIBRIUM" if ok else "STRATEGIC_GAP"})
    return rows


def test_qre_players_pass_the_gate():
    rows = _synthetic({"vickrey": 0.5, "cournot": 0.02, "repeated_pd": 0.4, "public_goods": 1.0})
    calibrated = [gate.calibration(rows, g)["calibrated"] for g in gate.GAMES_2A]
    assert sum(calibrated) >= 3


def test_pd_cooperation_above_half_is_a_hard_fail():
    rows = [{"game": "repeated_pd", "framing": "named", "paraphrase_idx": str(k % 3),
             "params": GAMES["repeated_pd"].sampler(seed=k), "observed_action": "C" if k % 10 < 7 else "D",
             "verdict": "AT_EQUILIBRIUM" if k % 10 >= 7 else "STRATEGIC_GAP"} for k in range(60)]
    c = gate.calibration(rows, "repeated_pd")
    assert c["hard_fail"] and not c["calibrated"]


def test_eq_prob_limits():
    p = GAMES["repeated_pd"].sampler(seed=1)
    assert gate.eq_prob("repeated_pd", p, 1e-3) == __import__("pytest").approx(0.5, abs=0.01)
    assert gate.eq_prob("repeated_pd", p, 100.0) > 0.99
