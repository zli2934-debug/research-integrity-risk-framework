"""Project-level release audit utilities for Research Integrity Risk Framework v1.1-prep.1."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

EXPECTED_FILES = [
    "README.md",
    "CITATION.cff",
    "LICENSE-CODE",
    "LICENSE-DOCS",
    "src/scoring.py",
    "src/database.py",
    "src/benchmark.py",
    "src/validation.py",
    "src/sensitivity.py",
    "src/expert_review.py",
    "src/simulated_expert.py",
    "docs/SOP.md",
    "docs/scoring_model.md",
    "docs/database_integration.md",
    "docs/benchmark_validation.md",
    "docs/case_validation_workflow.md",
    "docs/weight_sensitivity.md",
    "docs/expert_review_protocol.md",
    "docs/pre_release_consolidation.md",
    "docs/api_reference.md",
    "docs/release_checklist.md",
    "docs/final_audit_checklist.md",
    "docs/repository_manuscript_map.md",
    "docs/literature_informed_expert_simulation.md",
    "docs/release_notes_v1_1_prep.md",
    "docs/release_readiness_report_v1_1_prep.md",
    "docs/final_audit_report_v1_1_prep.md",
    "docs/release_notes_v1_1_prep_1.md",
    "docs/release_readiness_report_v1_1_prep_1.md",
    "docs/final_audit_report_v1_1_prep_1.md",
    "examples/literature_informed_simulated_expert_panel.csv",
    "examples/literature_informed_simulated_delphi_round_1.csv",
    "examples/literature_informed_simulated_delphi_round_2.csv",
    "templates/literature_review_to_expert_preference_matrix.csv",
    "templates/hybrid_interview_log_template.md",
    "manuscript/simulated_expert_review_placeholder.md",
    "docs/v1_0_roadmap.md",
    "docs/release_notes_v1_0_0.md",
    "docs/release_readiness_report_v1_0_0.md",
    "docs/final_audit_report_v1_0_0.md",
    "manuscript/paper_outline.md",
    "manuscript/citation_verification_table.csv",
    "templates/release_readiness_report_template.md",
    "templates/final_audit_report_template.md",
]

FORBIDDEN_ARTIFACT_NAMES = {"__pycache__", ".pytest_cache"}
PRIVATE_DATA_PATTERNS = ("retraction_watch.csv",)


def verify_expected_files(root_path: str | Path) -> Dict[str, object]:
    """Check whether expected project files are present."""
    root = Path(root_path)
    missing: List[str] = []
    for rel in EXPECTED_FILES:
        if not (root / rel).exists():
            missing.append(rel)
    return {
        "expected_count": len(EXPECTED_FILES),
        "missing_count": len(missing),
        "missing_files": missing,
        "status": "PASS" if not missing else "NEEDS_REVISION",
    }


def find_cache_artifacts(root_path: str | Path) -> List[str]:
    """Find cache artifacts that should not be included in release zips.

    This checks the current directory tree. Runtime-generated local caches may
    appear after tests are run; release zips should be made from a clean tree.
    """
    root = Path(root_path)
    found: List[str] = []
    for path in root.rglob("*"):
        if path.name in FORBIDDEN_ARTIFACT_NAMES:
            found.append(str(path.relative_to(root)))
    return sorted(found)


def find_private_data_artifacts(root_path: str | Path) -> List[str]:
    """Find raw/private data files that should not be redistributed."""
    root = Path(root_path)
    found: List[str] = []
    for path in root.rglob("*"):
        if path.is_file() and path.name.lower() in PRIVATE_DATA_PATTERNS:
            found.append(str(path.relative_to(root)))
    return sorted(found)


def release_readiness_summary(root_path: str | Path) -> Dict[str, object]:
    """Return a lightweight release-readiness summary for release audit."""
    file_check = verify_expected_files(root_path)
    cache_artifacts = find_cache_artifacts(root_path)
    private_data = find_private_data_artifacts(root_path)
    passed = (
        file_check["missing_count"] == 0
        and not cache_artifacts
        and not private_data
    )
    return {
        "file_check": file_check,
        "cache_artifacts": cache_artifacts,
        "private_data_artifacts": private_data,
        "release_readiness": "PASS" if passed else "NEEDS_REVISION",
        "boundary_note": "Release readiness does not imply empirical validation, expert consensus, or misconduct adjudication capability. Cache checks apply to the current directory tree; runtime-generated local caches after tests should be removed before packaging.",
    }
