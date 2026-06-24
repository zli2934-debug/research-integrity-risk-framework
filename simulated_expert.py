"""Literature-informed simulated expert-review utilities for Research Integrity Risk Framework v1.1-prep.1.

This module supports workflow rehearsal with simulated expert panel data. It does
not create real expert consensus, real calibration evidence, or empirical model
validation.
"""

from __future__ import annotations

from typing import Dict, Mapping, Sequence, List

try:
    from .scoring import WEIGHTS
    from .sensitivity import validate_weights, normalize_weights
except ImportError:  # pragma: no cover
    from scoring import WEIGHTS
    from sensitivity import validate_weights, normalize_weights

MODULES = tuple(WEIGHTS.keys())
SIMULATED_DATA_TYPE = "Simulated"
LITERATURE_INFORMED_STATUS = "Literature-informed placeholder"

LITERATURE_INFORMED_SIMULATED_PROFILE: Dict[str, float] = {
    "M1": 0.16,
    "M2": 0.09,
    "M3": 0.16,
    "M4": 0.17,
    "M5": 0.10,
    "M6": 0.07,
    "M7": 0.13,
    "M8": 0.07,
    "M9": 0.05,
}


def literature_informed_simulated_profile() -> Dict[str, float]:
    """Return the v1.1-prep.1 literature-informed simulated aggregate profile.

    The profile is for workflow testing only. It must not be described as real
    expert consensus or empirically optimized weighting.
    """
    validate_weights(LITERATURE_INFORMED_SIMULATED_PROFILE)
    return dict(LITERATURE_INFORMED_SIMULATED_PROFILE)


def validate_simulated_expert_row(row: Mapping[str, object]) -> None:
    """Validate that a row is explicitly marked as simulated workflow-test data."""
    if str(row.get("DataType", "")).strip() != SIMULATED_DATA_TYPE:
        raise ValueError("Simulated expert rows must have DataType=Simulated")
    if str(row.get("UseForCalibration", "")).strip().lower() not in {"no", "false", "0"}:
        raise ValueError("Simulated expert rows must have UseForCalibration=No")
    if str(row.get("UseForPublicationResult", "")).strip().lower() not in {"no", "false", "0"}:
        raise ValueError("Simulated expert rows must have UseForPublicationResult=No")
    if str(row.get("UseForWorkflowTesting", "")).strip().lower() not in {"yes", "true", "1"}:
        raise ValueError("Simulated expert rows must have UseForWorkflowTesting=Yes")
    weights = {m: float(row.get(m, 0) or 0) for m in MODULES}
    validate_weights(normalize_weights(weights))


def validate_simulated_panel(rows: Sequence[Mapping[str, object]]) -> None:
    """Validate all simulated expert rows."""
    if not rows:
        raise ValueError("At least one simulated expert row is required")
    for row in rows:
        validate_simulated_expert_row(row)


def simulated_panel_summary(rows: Sequence[Mapping[str, object]]) -> Dict[str, object]:
    """Summarize simulated expert panel composition and safeguards."""
    validate_simulated_panel(rows)
    by_mode: Dict[str, int] = {}
    by_role: Dict[str, int] = {}
    for row in rows:
        mode = str(row.get("InterviewMode", "Unspecified") or "Unspecified")
        role = str(row.get("Role", "Unspecified") or "Unspecified")
        by_mode[mode] = by_mode.get(mode, 0) + 1
        by_role[role] = by_role.get(role, 0) + 1
    return {
        "n_simulated_experts": len(rows),
        "by_interview_mode": by_mode,
        "by_role": by_role,
        "safeguard": "Simulated data are for workflow rehearsal only and must not be used as real expert validation or calibration evidence.",
    }
