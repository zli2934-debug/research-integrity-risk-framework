import pytest

from src.scoring import WEIGHTS, CaseFlags, classify_case, compute_trs, preliminary_classification


def test_weight_sum_equals_one():
    assert round(sum(WEIGHTS.values()), 10) == 1.0


def test_synthetic_case_01_trs():
    scores = {"M1": 4, "M2": 1, "M3": 3, "M4": 2, "M5": 2, "M6": 2, "M7": 1, "M8": 0, "M9": 0}
    assert compute_trs(scores) == 2.03


def test_invalid_score_rejected():
    with pytest.raises(ValueError):
        compute_trs({"M1": 6})


def test_unknown_module_rejected():
    with pytest.raises(ValueError):
        compute_trs({"M10": 1})


def test_missing_modules_default_zero():
    assert compute_trs({"M1": 5}) == 0.9


def test_preliminary_trs_above_four_is_c3_plus_not_c4():
    assert preliminary_classification(4.2).startswith("C3+")


def test_c4_override():
    assert classify_case(1.1, CaseFlags(has_official_retraction=True)).startswith("C4")


def test_c5_override():
    assert classify_case(2.1, CaseFlags(has_official_misconduct_wording=True)).startswith("C5")


def test_c5_has_priority_over_c7():
    flags = CaseFlags(
        has_official_retraction=True,
        has_official_misconduct_wording=True,
        has_non_misconduct_or_error_wording=True,
        author_cooperated_or_requested_correction=True,
        no_repeated_pattern_found=True,
    )
    assert classify_case(2.1, flags).startswith("C5")


def test_c6_requires_clear_responsibility():
    flags = CaseFlags(
        has_official_misconduct_wording=True,
        has_multiple_formal_records=True,
        same_author_identity_confirmed=True,
        has_repeated_similar_pattern=True,
        has_clear_responsibility=False,
    )
    assert classify_case(2.5, flags).startswith("C5")


def test_c6_override_with_clear_responsibility():
    flags = CaseFlags(
        has_official_misconduct_wording=True,
        has_multiple_formal_records=True,
        same_author_identity_confirmed=True,
        has_repeated_similar_pattern=True,
        has_clear_responsibility=True,
    )
    assert classify_case(2.5, flags).startswith("C6")


def test_c6_requires_same_author_identity_confirmation():
    flags = CaseFlags(
        has_official_misconduct_wording=True,
        has_multiple_formal_records=True,
        same_author_identity_confirmed=False,
        has_repeated_similar_pattern=True,
        has_clear_responsibility=True,
    )
    assert classify_case(2.5, flags).startswith("C5")


def test_c7_override_low_trs_non_misconduct():
    flags = CaseFlags(
        has_official_retraction=True,
        has_non_misconduct_or_error_wording=True,
        author_cooperated_or_requested_correction=True,
        no_repeated_pattern_found=True,
    )
    assert classify_case(2.4, flags, scores={"M1": 2, "M3": 2, "M4": 2}).startswith("C7")


def test_c7_does_not_override_high_trs():
    flags = CaseFlags(
        has_official_retraction=True,
        has_non_misconduct_or_error_wording=True,
        author_cooperated_or_requested_correction=True,
        no_repeated_pattern_found=True,
    )
    assert classify_case(3.2, flags, scores={"M1": 2, "M3": 2, "M4": 2}).startswith("C4")


def test_c7_does_not_override_high_core_module():
    flags = CaseFlags(
        has_official_retraction=True,
        has_non_misconduct_or_error_wording=True,
        author_cooperated_or_requested_correction=True,
        no_repeated_pattern_found=True,
    )
    assert classify_case(2.4, flags, scores={"M1": 4, "M3": 1, "M4": 1}).startswith("C4")
