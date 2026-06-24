"""Benchmark utilities for Research Integrity Risk Framework v1.1-prep.1.

This module evaluates synthetic or officially documented benchmark cases against
expected C0-C7 classification prefixes. It is designed to test the framework's
logic, not to adjudicate real-world misconduct.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from .scoring import CaseFlags, classify_case, compute_trs, recommended_statement

MODULE_COLUMNS = tuple(f"M{i}" for i in range(1, 10))
FLAG_COLUMNS = tuple(CaseFlags.__dataclass_fields__.keys())


def _clean(value: object) -> str:
    if value is None:
        return ""
    return " ".join(str(value).split())


def parse_bool(value: object) -> bool:
    """Parse common CSV boolean values."""
    text = _clean(value).lower()
    return text in {"1", "true", "yes", "y", "t"}


def load_benchmark_cases(path: str | Path) -> List[Dict[str, str]]:
    """Load benchmark cases from CSV.

    Expected columns include case_id, case_type, expected_category_prefix, M1-M9,
    and optional CaseFlags fields.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Benchmark file not found: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(row) for row in csv.DictReader(f)]


def scores_from_case(row: Dict[str, object]) -> Dict[str, float]:
    """Extract M1-M9 scores from a benchmark row."""
    scores: Dict[str, float] = {}
    for module in MODULE_COLUMNS:
        raw = _clean(row.get(module, ""))
        scores[module] = float(raw) if raw else 0.0
    return scores


def flags_from_case(row: Dict[str, object]) -> CaseFlags:
    """Extract CaseFlags from a benchmark row."""
    kwargs = {name: parse_bool(row.get(name, "")) for name in FLAG_COLUMNS}
    return CaseFlags(**kwargs)


def evaluate_benchmark_case(row: Dict[str, object]) -> Dict[str, object]:
    """Evaluate one benchmark case and compare predicted vs expected category."""
    scores = scores_from_case(row)
    flags = flags_from_case(row)
    trs = compute_trs(scores)
    predicted = classify_case(trs, flags=flags, scores=scores)
    expected_prefix = _clean(row.get("expected_category_prefix", ""))
    passed = bool(expected_prefix and predicted.startswith(expected_prefix))
    return {
        "case_id": _clean(row.get("case_id", "")),
        "case_type": _clean(row.get("case_type", "")),
        "expected_category_prefix": expected_prefix,
        "predicted_classification": predicted,
        "passed": passed,
        "trs": trs,
        "rationale": recommended_statement(predicted),
    }


def run_benchmark(cases: Iterable[Dict[str, object]]) -> List[Dict[str, object]]:
    """Evaluate all benchmark cases."""
    return [evaluate_benchmark_case(row) for row in cases]


def summarize_benchmark(results: Iterable[Dict[str, object]]) -> Dict[str, object]:
    """Summarize benchmark results."""
    rows = list(results)
    total = len(rows)
    passed = sum(1 for row in rows if row.get("passed"))
    return {
        "total_cases": total,
        "passed_cases": passed,
        "failed_cases": total - passed,
        "pass_rate": round(passed / total, 3) if total else 0.0,
        "status": "PASS" if total and passed == total else "NEEDS_REVIEW",
    }


def write_benchmark_report_markdown(
    results: Iterable[Dict[str, object]], output_path: str | Path, title: str = "Benchmark Report"
) -> Path:
    """Write a compact benchmark report in Markdown."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = list(results)
    summary = summarize_benchmark(rows)
    lines = [
        f"# {title}",
        "",
        "This report evaluates benchmark cases against expected classification prefixes.",
        "Benchmark results test model logic only; they do not validate real-world misconduct determinations.",
        "",
        "## Summary",
        "",
        f"- Total cases: {summary['total_cases']}",
        f"- Passed cases: {summary['passed_cases']}",
        f"- Failed cases: {summary['failed_cases']}",
        f"- Pass rate: {summary['pass_rate']}",
        f"- Status: {summary['status']}",
        "",
        "## Case Results",
        "",
        "| Case ID | Type | TRS | Expected | Predicted | Pass |",
        "|---|---|---:|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['case_id']} | {row['case_type']} | {row['trs']} | "
            f"{row['expected_category_prefix']} | {row['predicted_classification']} | {row['passed']} |"
        )
    lines.extend([
        "",
        "## Boundary Statement",
        "",
        "A benchmark pass means the implementation follows the expected rule logic for the provided cases. It does not prove that the model is empirically optimal, legally valid, or capable of replacing formal research-integrity review.",
    ])
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path
