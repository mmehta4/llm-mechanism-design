"""Stage 5 analysis on simulated QRE players, plus its refusal before the lock."""
from analysis import stage5 as A


def test_simulated_qre_players_read_as_qre():
    data, fit, coop = A.synthetic(0.154, n=400, seed=3)
    lines, row = A.model_section("sim", data, fit, coop)
    assert row["test1"] == "QRE"
    assert "within 90 ± 15" in row["test2"]
    assert "QRE describes" in A.interpret(row, data)


def test_tau_parsing():
    assert A.tau_of("repeated_pd_subsidy_1p5") == 1.5 and A.tau_of("repeated_pd_subsidy_16p2") == 16.2
    assert A.tau_of("repeated_pd_subsidy_0") == 0.0


def test_refuses_before_lock(monkeypatch, capsys):
    monkeypatch.setattr(A, "STAGE5_ANALYSIS_SHA256", None)
    monkeypatch.setattr("sys.argv", ["stage5.py", "--model", "nemotron"])
    assert A.main() == 1 and "not locked" in capsys.readouterr().out


def test_the_stage5_analysis_is_locked():
    """Edits to analysis/stage5.py, analysis/gate.py or the three design documents after
    the lock must be recorded deviations."""
    assert A.stage5_locked()
