"""Scoring utilities for Research Integrity Risk Framework v1.1-prep.1.

This module implements a transparent rule-based Total Risk Score (TRS)
and hard-logic classification overrides. It is a scoring framework, not a
database-integrated misconduct adjudication system. Database utilities are available in src.database, but classification remains a cautious scoring framework.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

WEIGHTS: Dict[str, float] = {
    "M1": 0.18,  # Figures/images
    "M2": 0.08,  # Tables
    "M3": 0.15,  # Statistics
    "M4": 0.18,  # Raw data
    "M5": 0.08,  # Methods
    "M6": 0.07,  # Conclusions
    "M7": 0.12,  # External databases / official records
    "M8": 0.09,  # Author history
    "M9": 0.05,  # Responsibility attribution
}

CORE_MODULES = ("M1", "M3", "M4")


@dataclass
class CaseFlags:
    """Formal-record and context flags used for hard logic overrides.

    Important boundary rule:
    C5 and C6 must not be inferred from TRS alone. They require official
    misconduct-type wording and, for C6, confirmed author identity, repeated
    pattern, multiple formal records, and clear responsibility linkage.
    """

    has_official_retraction: bool = False
    has_official_correction: bool = False
    has_expression_of_concern: bool = False
    has_official_misconduct_wording: bool = False
    has_multiple_formal_records: bool = False
    same_author_identity_confirmed: bool = False
    has_repeated_similar_pattern: bool = False
    has_clear_responsibility: bool = False
    has_non_misconduct_or_error_wording: bool = False
    author_cooperated_or_requested_correction: bool = False
    no_repeated_pattern_found: bool = False


def validate_scores(scores: Dict[str, float]) -> None:
    """Validate that all provided module scores are between 0 and 5."""
    for module, value in scores.items():
        if module not in WEIGHTS:
            raise ValueError(f"Unknown module {module}; expected one of {sorted(WEIGHTS)}")
        numeric = float(value)
        if numeric < 0 or numeric > 5:
            raise ValueError(f"{module} score must be between 0 and 5")


def compute_trs(scores: Dict[str, float]) -> float:
    """Compute total risk score from module scores.

    Parameters
    ----------
    scores:
        Mapping from M1-M9 to numeric scores from 0 to 5. Missing modules
        are treated as 0 so partial scoring sheets can still be evaluated.

    Returns
    -------
    float
        Weighted total risk score rounded to three decimals.
    """
    validate_scores(scores)
    total = 0.0
    for module, weight in WEIGHTS.items():
        total += float(scores.get(module, 0)) * weight
    return round(total, 3)


def has_high_core_module(scores: Optional[Dict[str, float]]) -> bool:
    """Return True if any core evidence module has score >= 4."""
    if not scores:
        return False
    validate_scores({k: v for k, v in scores.items() if k in WEIGHTS})
    return any(float(scores.get(module, 0)) >= 4 for module in CORE_MODULES)


def preliminary_classification(trs: float) -> str:
    """Return preliminary risk category based on TRS only.

    TRS alone cannot produce C4-C7. Those categories require formal records,
    official wording, repeated-pattern evidence, or non-misconduct wording.
    """
    if trs < 1.0:
        return "C0 No visible concern"
    if trs < 2.0:
        return "C1 Minor concern"
    if trs < 3.0:
        return "C2 Serious concern"
    if trs < 4.0:
        return "C3 Strong manipulation risk"
    return "C3+ Very high manipulation risk; official-record review required"


def classify_case(
    trs: float,
    flags: Optional[CaseFlags] = None,
    scores: Optional[Dict[str, float]] = None,
) -> str:
    """Classify a case using TRS plus hard logic overrides.

    Parameters
    ----------
    trs:
        Total Risk Score from 0 to 5.
    flags:
        Formal-record and context flags.
    scores:
        Optional module-level scores. Required for the safest C7 logic because
        C7 should not automatically override high TRS or high core-module risk.

    Logic priority
    --------------
    C6 > C5 > C7/C4 > TRS-only categories.
    C7 is only allowed when official wording supports non-misconduct/error or
    inconclusive interpretation AND the case is not high TRS and has no high
    core-module abnormality.
    """
    flags = flags or CaseFlags()

    # C6 has priority over C5 only when repeated formal pattern is established.
    if (
        flags.has_multiple_formal_records
        and flags.same_author_identity_confirmed
        and flags.has_repeated_similar_pattern
        and flags.has_clear_responsibility
        and flags.has_official_misconduct_wording
    ):
        return "C6 Repeated misconduct pattern"

    # C5 requires official misconduct-type wording. TRS alone cannot trigger it.
    if flags.has_official_misconduct_wording:
        return "C5 Confirmed misconduct"

    formal_record_exists = (
        flags.has_official_retraction
        or flags.has_official_correction
        or flags.has_expression_of_concern
    )

    # C7 is conservative: it cannot override high TRS or high core evidence risk
    # unless a future version introduces stronger official non-misconduct records.
    if (
        formal_record_exists
        and flags.has_non_misconduct_or_error_wording
        and (flags.author_cooperated_or_requested_correction or flags.no_repeated_pattern_found)
        and not flags.has_repeated_similar_pattern
        and trs < 3.0
        and not has_high_core_module(scores)
    ):
        return "C7 Possible non-intentional error or inconclusive retraction"

    if formal_record_exists:
        return "C4 Formal correction or retraction"

    return preliminary_classification(trs)


def recommended_statement(classification: str) -> str:
    """Return cautious wording for a classification."""
    if classification.startswith("C6"):
        return "Multiple formal records, confirmed identity, repeated patterns, and clear responsibility linkage support a repeated misconduct pattern. Avoid labeling individuals beyond the official record."
    if classification.startswith("C5"):
        return "Official records explicitly state misconduct-type wording. Classify as confirmed misconduct based on the official notice, not on the score alone."
    if classification.startswith("C7"):
        return "Available records are more consistent with non-intentional error or an inconclusive retraction than confirmed misconduct. Preserve uncertainty."
    if classification.startswith("C4"):
        return "The article has a formal correction/retraction/concern record, but misconduct should not be inferred unless official wording supports it."
    if classification.startswith("C3+"):
        return "The article shows very high data-integrity risk by scoring, but official records are still required before classifying misconduct."
    if classification.startswith("C3"):
        return "The article shows strong data-integrity risk and requires formal review. This does not by itself prove misconduct."
    if classification.startswith("C2"):
        return "The article shows serious research-integrity concerns requiring clarification or further review."
    if classification.startswith("C1"):
        return "The article shows minor concerns that may require clarification."
    return "No visible concern based on the current scoring inputs."
