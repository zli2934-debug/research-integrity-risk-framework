"""Real-case validation utilities for Research Integrity Risk Framework v1.1-prep.1.

This module supports curated validation sets that are built from official notices,
Retraction Watch records, or other documented sources. It is designed to test model
behavior against expected category prefixes while preserving strict evidence boundaries.

Important boundary rule: a validation pass does not prove misconduct detection accuracy.
It only shows that the framework handled a curated case as expected under the provided
scores, flags, and source-verification metadata.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from .benchmark import FLAG_COLUMNS, MODULE_COLUMNS, evaluate_benchmark_case, parse_bool

VALIDATION_REQUIRED_COLUMNS = (
    "case_id",
    "case_type",
    "source_type",
    "expected_category_prefix",
    "official_notice_verified",
    "identity_verification_status",
    "responsibility_verification_status",
)


def _clean(value: object) -> str:
    if value is None:
        return ""
    return " ".join(str(value).split())


def load_validation_cases(path: str | Path) -> List[Dict[str, str]]:
    """Load curated real-case validation rows from CSV.

    Expected columns include the benchmark columns plus source-verification metadata.
    Real-case validation rows should be based on official notices or documented records,
    not informal allegations alone.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Validation case file not found: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = [dict(row) for row in reader]
    return rows


def source_verification_status(row: Dict[str, object]) -> str:
    """Return a conservative source-verification status for a validation row."""
    source_type = _clean(row.get("source_type", "")).lower()
    official_verified = parse_bool(row.get("official_notice_verified", ""))
    expected = _clean(row.get("expected_category_prefix", ""))

    if expected in {"C4", "C5", "C6", "C7"} and not official_verified:
        return "NEEDS_OFFICIAL_NOTICE_VERIFICATION"
    if source_type in {"official_notice", "journal_notice", "institution_notice"} and official_verified:
        return "VERIFIED_SOURCE_METADATA"
    if source_type in {"retraction_watch", "secondary_database"}:
        return "SECONDARY_DATABASE_ONLY_VERIFY_OFFICIAL_NOTICE"
    if source_type in {"synthetic", "placeholder"}:
        return "NOT_REAL_CASE"
    return "NEEDS_SOURCE_REVIEW"


def boundary_risk_status(row: Dict[str, object]) -> str:
    """Flag validation rows that risk overclaiming strong categories."""
    expected = _clean(row.get("expected_category_prefix", ""))
    identity = _clean(row.get("identity_verification_status", "")).lower()
    responsibility = _clean(row.get("responsibility_verification_status", "")).lower()
    official_verified = parse_bool(row.get("official_notice_verified", ""))

    if expected == "C6":
        if identity != "confirmed" or responsibility not in {"clear", "official"} or not official_verified:
            return "RISKY_C6_BOUNDARY"
    if expected == "C5" and not official_verified:
        return "RISKY_C5_BOUNDARY"
    if expected in {"C0", "C1", "C2", "C3"} and official_verified:
        return "CHECK_IF_FORMAL_RECORD_SHOULD_TRIGGER_C4_PLUS"
    return "BOUNDARY_OK"


def evaluate_validation_case(row: Dict[str, object]) -> Dict[str, object]:
    """Evaluate one validation row and attach source/boundary audit metadata."""
    result = evaluate_benchmark_case(row)
    source_status = source_verification_status(row)
    boundary_status = boundary_risk_status(row)
    validation_passed = bool(result["passed"] and source_status != "NEEDS_OFFICIAL_NOTICE_VERIFICATION" and not boundary_status.startswith("RISKY"))
    result.update(
        {
            "source_type": _clean(row.get("source_type", "")),
            "official_notice_verified": parse_bool(row.get("official_notice_verified", "")),
            "identity_verification_status": _clean(row.get("identity_verification_status", "")),
            "responsibility_verification_status": _clean(row.get("responsibility_verification_status", "")),
            "source_verification_status": source_status,
            "boundary_risk_status": boundary_status,
            "validation_passed": validation_passed,
        }
    )
    return result


def run_validation(cases: Iterable[Dict[str, object]]) -> List[Dict[str, object]]:
    """Evaluate all curated validation cases."""
    return [evaluate_validation_case(row) for row in cases]


def summarize_validation(results: Iterable[Dict[str, object]]) -> Dict[str, object]:
    """Summarize curated validation results."""
    rows = list(results)
    total = len(rows)
    passed = sum(1 for row in rows if row.get("validation_passed"))
    needs_source = sum(1 for row in rows if row.get("source_verification_status") == "NEEDS_OFFICIAL_NOTICE_VERIFICATION")
    boundary_risky = sum(1 for row in rows if str(row.get("boundary_risk_status", "")).startswith("RISKY"))
    model_mismatch = sum(1 for row in rows if not row.get("passed"))
    return {
        "total_cases": total,
        "validation_passed_cases": passed,
        "model_mismatch_cases": model_mismatch,
        "needs_official_notice_verification": needs_source,
        "boundary_risk_cases": boundary_risky,
        "validation_pass_rate": round(passed / total, 3) if total else 0.0,
        "status": "PASS" if total and passed == total else "NEEDS_REVIEW",
    }


def write_validation_report_markdown(
    results: Iterable[Dict[str, object]], output_path: str | Path, title: str = "Case Validation Report"
) -> Path:
    """Write a case-validation report in Markdown."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = list(results)
    summary = summarize_validation(rows)
    lines = [
        f"# {title}",
        "",
        "This report evaluates curated validation cases against expected classification prefixes and source-boundary requirements.",
        "A pass does not prove empirical optimality, misconduct detection accuracy, or author responsibility.",
        "",
        "## Summary",
        "",
        f"- Total cases: {summary['total_cases']}",
        f"- Validation passed cases: {summary['validation_passed_cases']}",
        f"- Model mismatch cases: {summary['model_mismatch_cases']}",
        f"- Needs official-notice verification: {summary['needs_official_notice_verification']}",
        f"- Boundary-risk cases: {summary['boundary_risk_cases']}",
        f"- Validation pass rate: {summary['validation_pass_rate']}",
        f"- Status: {summary['status']}",
        "",
        "## Case Results",
        "",
        "| Case ID | Type | TRS | Expected | Predicted | Source Status | Boundary Status | Validation Pass |",
        "|---|---|---:|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['case_id']} | {row['case_type']} | {row['trs']} | {row['expected_category_prefix']} | "
            f"{row['predicted_classification']} | {row['source_verification_status']} | "
            f"{row['boundary_risk_status']} | {row['validation_passed']} |"
        )
    lines.extend(
        [
            "",
            "## Boundary Statement",
            "",
            "Real-case validation requires source verification, identity safeguards, and responsibility-boundary review. Secondary database matches should be verified against official journal or institutional notices before being used for strong classifications such as C5 or C6.",
        ]
    )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path
