# Weight Sensitivity Analysis

**Component introduced:** v0.7-alpha  
**Current package version:** v1.0.0

## Purpose

v0.7-alpha adds a sensitivity-analysis layer for testing how the Total Risk Score (TRS) and preliminary C0-C3/C3+ categories behave under different weighting assumptions.

This layer does **not** empirically validate the weights. It helps identify whether a case classification is stable or unstable when reasonable alternative weight profiles are used.

## Why this matters

The default v0.1-v0.7 weights are pilot expert-prior weights. They were assigned using evidentiary proximity, verifiability, and misclassification-risk principles. They are not validated optimal weights.

Sensitivity analysis is therefore required before using model outputs in manuscripts, reports, or public-facing applications.

## Built-in profiles

v0.7-alpha includes four profiles:

| Profile | Intended use |
|---|---|
| `pilot_expert_prior` | Default general-purpose pilot profile |
| `biomedical_experimental` | Biomedical laboratory studies with figures/images, raw data, and experimental methods |
| `clinical_epidemiology` | Clinical, epidemiological, cohort, RCT, or meta-analysis style papers |
| `author_history_review` | Cautious author-history and repeated-pattern review; still not identity confirmation |

## Core functions

`src/sensitivity.py` provides:

- `WEIGHT_PROFILES`
- `validate_weights()`
- `compute_trs_with_weights()`
- `evaluate_weight_profiles()`
- `classification_stability()`
- `perturb_single_weight()`
- `perturbation_grid()`
- `rank_cases_by_profile()`
- `rank_stability_summary()`

## Interpretation

Stable classification across profiles suggests the output is less sensitive to the initial weighting choice. Unstable classification means that the report should explicitly state that the case sits near a classification boundary or depends on weight assumptions.

## Boundary statement

Sensitivity analysis does not prove misconduct, validate intent, confirm identity, or replace official investigation. It only evaluates robustness of the scoring layer under alternative plausible weights.
