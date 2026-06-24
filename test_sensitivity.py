import pytest

from src.sensitivity import (
    WEIGHT_PROFILES,
    validate_weights,
    compute_trs_with_weights,
    perturb_single_weight,
    evaluate_weight_profiles,
    classification_stability,
    perturbation_grid,
    rank_stability_summary,
)


def test_all_weight_profiles_sum_to_one():
    for weights in WEIGHT_PROFILES.values():
        validate_weights(weights)


def test_compute_trs_with_biomedical_profile():
    scores = {"M1": 4, "M2": 1, "M3": 3, "M4": 2, "M5": 2, "M6": 2, "M7": 1, "M8": 0, "M9": 0}
    trs = compute_trs_with_weights(scores, WEIGHT_PROFILES["biomedical_experimental"])
    assert trs == pytest.approx(2.12, abs=1e-3)


def test_perturb_single_weight_preserves_sum():
    perturbed = perturb_single_weight(WEIGHT_PROFILES["pilot_expert_prior"], "M1", 0.20)
    assert sum(perturbed.values()) == pytest.approx(1.0)
    assert perturbed["M1"] > WEIGHT_PROFILES["pilot_expert_prior"]["M1"]


def test_evaluate_weight_profiles_returns_all_profiles():
    scores = {"M1": 2, "M2": 1, "M3": 2, "M4": 1, "M5": 1, "M6": 1, "M7": 0, "M8": 0, "M9": 0}
    rows = evaluate_weight_profiles(scores)
    assert len(rows) == len(WEIGHT_PROFILES)
    assert all("TRS" in r and "Classification" in r for r in rows)


def test_classification_stability_summary():
    rows = [
        {"Profile": "a", "TRS": 1.1, "Classification": "C1 Minor concern"},
        {"Profile": "b", "TRS": 1.2, "Classification": "C1 Minor concern"},
    ]
    summary = classification_stability(rows)
    assert summary["stable_classification"] is True
    assert summary["trs_range"] == pytest.approx(0.1)


def test_perturbation_grid_shape():
    scores = {"M1": 3, "M2": 1, "M3": 2, "M4": 2, "M5": 1, "M6": 1, "M7": 1, "M8": 0, "M9": 0}
    rows = perturbation_grid(scores, relative_changes=(-0.1, 0.1))
    assert len(rows) == 18
    assert {r["PerturbedModule"] for r in rows} == set(WEIGHT_PROFILES["pilot_expert_prior"].keys())


def test_rank_stability_summary():
    cases = [
        {"CaseID": "A", "M1": 4, "M2": 0, "M3": 3, "M4": 4, "M5": 1, "M6": 1, "M7": 0, "M8": 0, "M9": 0},
        {"CaseID": "B", "M1": 0, "M2": 4, "M3": 4, "M4": 2, "M5": 3, "M6": 2, "M7": 0, "M8": 0, "M9": 0},
    ]
    summary = rank_stability_summary(cases)
    assert set(summary.keys()) == {"A", "B"}
    assert all("rank_range" in v for v in summary.values())
