import pytest

from src.expert_review import (
    aggregate_expert_weights,
    mean_weight_profile,
    expert_disagreement_matrix,
    summarize_expert_panel,
    identify_high_disagreement_modules,
    compare_delphi_rounds,
    calibration_status,
)


RESPONSES = [
    {"ExpertID": "E01", "Field": "Biomedical", "Role": "Faculty", "M1": 20, "M2": 7, "M3": 15, "M4": 18, "M5": 10, "M6": 7, "M7": 10, "M8": 8, "M9": 5},
    {"ExpertID": "E02", "Field": "Statistics", "Role": "Faculty", "M1": 8, "M2": 14, "M3": 22, "M4": 16, "M5": 12, "M6": 8, "M7": 10, "M8": 7, "M9": 3},
    {"ExpertID": "E03", "Field": "Research Integrity", "Role": "Compliance", "M1": 12, "M2": 6, "M3": 12, "M4": 14, "M5": 8, "M6": 6, "M7": 18, "M8": 14, "M9": 10},
]


def test_aggregate_expert_weights_returns_modules():
    summary = aggregate_expert_weights(RESPONSES)
    assert set(summary.keys()) == {f"M{i}" for i in range(1, 10)}
    assert "mean" in summary["M1"]
    assert summary["M1"]["mean"] == pytest.approx(0.133333, abs=1e-6)


def test_mean_weight_profile_sums_to_one():
    profile = mean_weight_profile(RESPONSES)
    assert sum(profile.values()) == pytest.approx(1.0)


def test_disagreement_matrix_pair_count():
    rows = expert_disagreement_matrix(RESPONSES)
    assert len(rows) == 3
    assert all("L1Distance" in r for r in rows)


def test_panel_summary_uses_pseudonymous_counts():
    summary = summarize_expert_panel(RESPONSES)
    assert summary["n_experts"] == 3
    assert summary["fields"]["Biomedical"] == 1
    assert "identity_note" in summary


def test_high_disagreement_modules_detects_spread():
    agg = aggregate_expert_weights(RESPONSES)
    high = identify_high_disagreement_modules(agg, range_threshold=0.07)
    assert any(r["Module"] == "M1" for r in high)


def test_compare_delphi_rounds_reports_shift():
    round2 = [dict(r) for r in RESPONSES]
    round2[0]["M1"] = 18
    round2[0]["M4"] = 20
    result = compare_delphi_rounds(RESPONSES, round2)
    assert "l1_profile_shift" in result
    assert result["l1_profile_shift"] >= 0


def test_calibration_status_has_boundary_note():
    status = calibration_status(RESPONSES)
    assert "consensus_ready" in status
    assert "does not prove empirical optimality" in status["status_note"]


def test_missing_expert_id_rejected():
    bad = dict(RESPONSES[0])
    bad["ExpertID"] = ""
    with pytest.raises(ValueError):
        aggregate_expert_weights([bad])
