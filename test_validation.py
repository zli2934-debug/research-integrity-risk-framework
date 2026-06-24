from pathlib import Path

from src.validation import (
    boundary_risk_status,
    evaluate_validation_case,
    load_validation_cases,
    run_validation,
    summarize_validation,
    write_validation_report_markdown,
)

ROOT = Path(__file__).resolve().parents[1]


def test_load_validation_template():
    rows = load_validation_cases(ROOT / "examples" / "real_case_validation_template.csv")
    assert len(rows) == 3
    assert rows[0]["case_id"] == "RV-C4-001"


def test_c6_requires_confirmed_identity_and_clear_responsibility_boundary():
    row = {
        "case_id": "bad-c6",
        "case_type": "boundary",
        "source_type": "official_notice",
        "expected_category_prefix": "C6",
        "official_notice_verified": "true",
        "identity_verification_status": "name_match_only",
        "responsibility_verification_status": "plausible",
    }
    assert boundary_risk_status(row) == "RISKY_C6_BOUNDARY"


def test_official_categories_need_official_notice_verification():
    row = {
        "case_id": "needs-source",
        "case_type": "source",
        "source_type": "secondary_database",
        "expected_category_prefix": "C5",
        "official_notice_verified": "false",
        "M1": "4",
        "M2": "0",
        "M3": "4",
        "M4": "4",
        "M5": "0",
        "M6": "0",
        "M7": "5",
        "M8": "0",
        "M9": "0",
        "has_official_misconduct_wording": "true",
    }
    result = evaluate_validation_case(row)
    assert result["source_verification_status"] == "NEEDS_OFFICIAL_NOTICE_VERIFICATION"
    assert result["validation_passed"] is False


def test_validation_template_passes_demonstration_cases():
    rows = load_validation_cases(ROOT / "examples" / "real_case_validation_template.csv")
    results = run_validation(rows)
    summary = summarize_validation(results)
    assert summary["total_cases"] == 3
    assert summary["model_mismatch_cases"] == 0
    assert summary["boundary_risk_cases"] == 0


def test_write_validation_report(tmp_path):
    rows = load_validation_cases(ROOT / "examples" / "real_case_validation_template.csv")
    results = run_validation(rows)
    out = write_validation_report_markdown(results, tmp_path / "case_validation_report.md")
    text = out.read_text(encoding="utf-8")
    assert "Case Validation Report" in text
    assert "Validation pass rate" in text
