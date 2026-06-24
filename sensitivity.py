"""Weight sensitivity analysis utilities for Research Integrity Risk Framework v1.1-prep.1.

This module tests how Total Risk Score (TRS) and preliminary classifications
change under alternative weighting assumptions. It is not empirical weight
calibration and does not prove that any weight profile is optimal.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

try:
    from .scoring import WEIGHTS, compute_trs, preliminary_classification, classify_case, CaseFlags
except ImportError:  # pragma: no cover
    from scoring import WEIGHTS, compute_trs, preliminary_classification, classify_case, CaseFlags

MODULES = tuple(WEIGHTS.keys())

WEIGHT_PROFILES: Dict[str, Dict[str, float]] = {
    "pilot_expert_prior": dict(WEIGHTS),
    "biomedical_experimental": {
        "M1": 0.20, "M2": 0.07, "M3": 0.15, "M4": 0.18, "M5": 0.10,
        "M6": 0.07, "M7": 0.10, "M8": 0.08, "M9": 0.05,
    },
    "clinical_epidemiology": {
        "M1": 0.03, "M2": 0.16, "M3": 0.20, "M4": 0.16, "M5": 0.14,
        "M6": 0.10, "M7": 0.10, "M8": 0.08, "M9": 0.03,
    },
    "author_history_review": {
        "M1": 0.12, "M2": 0.04, "M3": 0.08, "M4": 0.12, "M5": 0.04,
        "M6": 0.04, "M7": 0.18, "M8": 0.22, "M9": 0.16,
    },
}


def validate_weights(weights: Mapping[str, float], tolerance: float = 1e-9) -> None:
    """Validate that a weight mapping covers M1-M9 and sums to 1."""
    missing = set(MODULES) - set(weights)
    extra = set(weights) - set(MODULES)
    if missing or extra:
        raise ValueError(f"Weight modules mismatch. Missing={sorted(missing)}, extra={sorted(extra)}")
    total = sum(float(weights[m]) for m in MODULES)
    if abs(total - 1.0) > tolerance:
        raise ValueError(f"Weights must sum to 1.0; got {total}")
    for module, value in weights.items():
        if float(value) < 0:
            raise ValueError(f"Weight for {module} must be non-negative")


def compute_trs_with_weights(scores: Mapping[str, float], weights: Mapping[str, float]) -> float:
    """Compute TRS using an explicit weight profile."""
    validate_weights(weights)
    # Reuse scoring validation by computing once with default weights.
    compute_trs(dict(scores))
    total = sum(float(scores.get(m, 0)) * float(weights[m]) for m in MODULES)
    return round(total, 3)


def normalize_weights(raw_weights: Mapping[str, float]) -> Dict[str, float]:
    """Normalize non-negative M1-M9 weights to sum to 1."""
    missing = set(MODULES) - set(raw_weights)
    extra = set(raw_weights) - set(MODULES)
    if missing or extra:
        raise ValueError(f"Weight modules mismatch. Missing={sorted(missing)}, extra={sorted(extra)}")
    values = {m: float(raw_weights[m]) for m in MODULES}
    if any(v < 0 for v in values.values()):
        raise ValueError("Raw weights must be non-negative")
    total = sum(values.values())
    if total <= 0:
        raise ValueError("At least one raw weight must be positive")
    return {m: values[m] / total for m in MODULES}


def perturb_single_weight(weights: Mapping[str, float], module: str, relative_change: float) -> Dict[str, float]:
    """Perturb one module weight and renormalize all weights.

    relative_change=0.20 means the target module raw weight is increased by 20%.
    relative_change=-0.20 means it is decreased by 20% before normalization.
    """
    validate_weights(weights)
    if module not in MODULES:
        raise ValueError(f"Unknown module {module}")
    raw = dict(weights)
    raw[module] = max(0.0, float(raw[module]) * (1.0 + float(relative_change)))
    return normalize_weights(raw)


def evaluate_weight_profiles(
    scores: Mapping[str, float],
    profiles: Optional[Mapping[str, Mapping[str, float]]] = None,
    flags: Optional[CaseFlags] = None,
) -> List[Dict[str, object]]:
    """Evaluate a case under multiple weight profiles."""
    profiles = profiles or WEIGHT_PROFILES
    rows: List[Dict[str, object]] = []
    for name, weights in profiles.items():
        trs = compute_trs_with_weights(scores, weights)
        classification = classify_case(trs, flags=flags, scores=dict(scores))
        rows.append({"Profile": name, "TRS": trs, "Classification": classification})
    return rows


def classification_stability(rows: Sequence[Mapping[str, object]]) -> Dict[str, object]:
    """Summarize whether classifications are stable across profiles."""
    classes = [str(r["Classification"]) for r in rows]
    trs_values = [float(r["TRS"]) for r in rows]
    unique_classes = sorted(set(classes))
    return {
        "stable_classification": len(unique_classes) == 1,
        "unique_classifications": unique_classes,
        "trs_min": round(min(trs_values), 3) if trs_values else None,
        "trs_max": round(max(trs_values), 3) if trs_values else None,
        "trs_range": round(max(trs_values) - min(trs_values), 3) if trs_values else None,
    }


def perturbation_grid(
    scores: Mapping[str, float],
    base_weights: Optional[Mapping[str, float]] = None,
    relative_changes: Sequence[float] = (-0.20, -0.10, 0.10, 0.20),
) -> List[Dict[str, object]]:
    """Evaluate TRS under one-at-a-time weight perturbations."""
    base_weights = base_weights or WEIGHTS
    validate_weights(base_weights)
    rows: List[Dict[str, object]] = []
    for module in MODULES:
        for change in relative_changes:
            perturbed = perturb_single_weight(base_weights, module, change)
            trs = compute_trs_with_weights(scores, perturbed)
            rows.append({
                "PerturbedModule": module,
                "RelativeChange": float(change),
                "TRS": trs,
                "PreliminaryClassification": preliminary_classification(trs),
            })
    return rows


def rank_cases_by_profile(
    cases: Sequence[Mapping[str, object]],
    profile_weights: Mapping[str, float],
    case_id_field: str = "CaseID",
) -> List[Dict[str, object]]:
    """Rank cases by TRS under a specified weight profile.

    Each case must include CaseID and M1-M9 numeric score fields.
    """
    ranked: List[Dict[str, object]] = []
    for case in cases:
        scores = {m: float(case.get(m, 0) or 0) for m in MODULES}
        trs = compute_trs_with_weights(scores, profile_weights)
        ranked.append({"CaseID": case.get(case_id_field, ""), "TRS": trs})
    ranked.sort(key=lambda x: x["TRS"], reverse=True)
    for i, row in enumerate(ranked, start=1):
        row["Rank"] = i
    return ranked


def rank_stability_summary(
    cases: Sequence[Mapping[str, object]],
    profiles: Optional[Mapping[str, Mapping[str, float]]] = None,
) -> Dict[str, object]:
    """Summarize rank ranges for cases across weight profiles."""
    profiles = profiles or WEIGHT_PROFILES
    ranks_by_case: Dict[str, List[int]] = {}
    for profile_name, weights in profiles.items():
        for row in rank_cases_by_profile(cases, weights):
            ranks_by_case.setdefault(str(row["CaseID"]), []).append(int(row["Rank"]))
    return {
        case_id: {
            "min_rank": min(ranks),
            "max_rank": max(ranks),
            "rank_range": max(ranks) - min(ranks),
        }
        for case_id, ranks in sorted(ranks_by_case.items())
    }
