"""Expert review and calibration utilities for Research Integrity Risk Framework v1.1-prep.1.

This module supports expert-review infrastructure: weight survey aggregation,
disagreement metrics, and Delphi-style round comparison. It does not conduct
human-subjects research by itself and does not imply that expert review has
already been completed.
"""

from __future__ import annotations

from statistics import mean, median, pstdev
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

try:
    from .scoring import WEIGHTS
    from .sensitivity import validate_weights, normalize_weights
except ImportError:  # pragma: no cover
    from scoring import WEIGHTS
    from sensitivity import validate_weights, normalize_weights

MODULES = tuple(WEIGHTS.keys())


def _extract_weight_vector(response: Mapping[str, object], normalize: bool = True) -> Dict[str, float]:
    """Extract M1-M9 weights from an expert response row.

    If normalize=True, non-negative raw weights are normalized to sum to 1.
    This is useful because experts may provide percentages, points, or decimals.
    """
    raw = {m: float(response.get(m, 0) or 0) for m in MODULES}
    if normalize:
        return normalize_weights(raw)
    validate_weights(raw)
    return raw


def validate_expert_response(response: Mapping[str, object], normalize: bool = True) -> None:
    """Validate one expert survey response."""
    _extract_weight_vector(response, normalize=normalize)
    if not str(response.get("ExpertID", "")).strip():
        raise ValueError("ExpertID is required")


def aggregate_expert_weights(
    responses: Sequence[Mapping[str, object]],
    normalize: bool = True,
) -> Dict[str, Dict[str, float]]:
    """Aggregate expert weights by module.

    Returns mean, median, standard deviation, min, max, and range for each M1-M9.
    These statistics describe expert disagreement; they do not prove optimality.
    """
    if not responses:
        raise ValueError("At least one expert response is required")

    vectors = []
    for response in responses:
        validate_expert_response(response, normalize=normalize)
        vectors.append(_extract_weight_vector(response, normalize=normalize))

    summary: Dict[str, Dict[str, float]] = {}
    for module in MODULES:
        values = [v[module] for v in vectors]
        summary[module] = {
            "mean": round(mean(values), 6),
            "median": round(median(values), 6),
            "std": round(pstdev(values), 6),
            "min": round(min(values), 6),
            "max": round(max(values), 6),
            "range": round(max(values) - min(values), 6),
        }
    return summary


def mean_weight_profile(responses: Sequence[Mapping[str, object]], normalize: bool = True) -> Dict[str, float]:
    """Return a normalized mean expert weight profile."""
    summary = aggregate_expert_weights(responses, normalize=normalize)
    profile = {m: summary[m]["mean"] for m in MODULES}
    return normalize_weights(profile)


def pairwise_l1_distance(a: Mapping[str, float], b: Mapping[str, float]) -> float:
    """Compute pairwise L1 distance between two M1-M9 weight vectors."""
    validate_weights(a)
    validate_weights(b)
    return round(sum(abs(float(a[m]) - float(b[m])) for m in MODULES), 6)


def expert_disagreement_matrix(
    responses: Sequence[Mapping[str, object]],
    normalize: bool = True,
) -> List[Dict[str, object]]:
    """Return pairwise L1 disagreement between expert weight vectors."""
    if len(responses) < 2:
        return []
    vectors = []
    for response in responses:
        validate_expert_response(response, normalize=normalize)
        vectors.append((str(response.get("ExpertID", "")), _extract_weight_vector(response, normalize=normalize)))

    rows: List[Dict[str, object]] = []
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            id_a, vec_a = vectors[i]
            id_b, vec_b = vectors[j]
            rows.append({
                "ExpertA": id_a,
                "ExpertB": id_b,
                "L1Distance": pairwise_l1_distance(vec_a, vec_b),
            })
    return rows


def summarize_expert_panel(responses: Sequence[Mapping[str, object]]) -> Dict[str, object]:
    """Summarize expert panel composition without identifying individuals."""
    if not responses:
        raise ValueError("At least one expert response is required")
    fields: Dict[str, int] = {}
    roles: Dict[str, int] = {}
    for r in responses:
        field = str(r.get("Field", "Unspecified") or "Unspecified")
        role = str(r.get("Role", "Unspecified") or "Unspecified")
        fields[field] = fields.get(field, 0) + 1
        roles[role] = roles.get(role, 0) + 1
    return {
        "n_experts": len(responses),
        "fields": fields,
        "roles": roles,
        "identity_note": "Panel summary avoids personal identity disclosure; ExpertID should be pseudonymous.",
    }


def identify_high_disagreement_modules(
    aggregate_summary: Mapping[str, Mapping[str, float]],
    range_threshold: float = 0.08,
) -> List[Dict[str, object]]:
    """Flag modules where expert weights show high spread."""
    rows: List[Dict[str, object]] = []
    for module in MODULES:
        stats = aggregate_summary[module]
        spread = float(stats.get("range", 0))
        if spread >= range_threshold:
            rows.append({
                "Module": module,
                "Range": round(spread, 6),
                "Mean": stats.get("mean"),
                "Recommendation": "Discuss in Delphi round; do not treat current mean as stable consensus.",
            })
    return rows


def compare_delphi_rounds(
    round1: Sequence[Mapping[str, object]],
    round2: Sequence[Mapping[str, object]],
    normalize: bool = True,
) -> Dict[str, object]:
    """Compare aggregate weight movement between two Delphi-style rounds."""
    profile1 = mean_weight_profile(round1, normalize=normalize)
    profile2 = mean_weight_profile(round2, normalize=normalize)
    module_changes = {
        m: round(profile2[m] - profile1[m], 6)
        for m in MODULES
    }
    return {
        "round1_mean_profile": profile1,
        "round2_mean_profile": profile2,
        "l1_profile_shift": pairwise_l1_distance(profile1, profile2),
        "module_changes_round2_minus_round1": module_changes,
        "interpretation_note": "Reduced movement across rounds may suggest convergence, but expert review does not create ground truth.",
    }


def calibration_status(
    responses: Sequence[Mapping[str, object]],
    max_pairwise_l1_for_consensus: float = 0.25,
    max_module_range_for_consensus: float = 0.08,
) -> Dict[str, object]:
    """Provide a cautious consensus-status summary for expert weights."""
    agg = aggregate_expert_weights(responses)
    disagreements = expert_disagreement_matrix(responses)
    max_l1 = max((float(r["L1Distance"]) for r in disagreements), default=0.0)
    high_modules = identify_high_disagreement_modules(agg, range_threshold=max_module_range_for_consensus)
    consensus_ready = max_l1 <= max_pairwise_l1_for_consensus and not high_modules
    return {
        "consensus_ready": consensus_ready,
        "max_pairwise_l1": round(max_l1, 6),
        "high_disagreement_modules": high_modules,
        "status_note": "Consensus-ready only means weights are less divergent among sampled experts; it does not prove empirical optimality.",
    }
