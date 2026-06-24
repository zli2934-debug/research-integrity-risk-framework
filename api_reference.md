# API Reference

**Current package version:** v1.0.0

This document summarizes the main user-facing Python functions. Function behavior is conservative: outputs organize evidence and risk signals, not misconduct determinations.

## `src.scoring`

- `compute_trs(scores)`: calculate the Total Risk Score from M1-M9 module scores using pilot expert-prior weights.
- `classify_case(...)`: return preliminary or official-record-overridden C0-C7 classification.

## `src.database`

- `load_retraction_watch_csv(path, max_rows=None)`: load Retraction Watch CSV records.
- `search_by_doi(records, doi)`: search DOI-related fields.
- `search_by_author(records, author_name, limit=None)`: substring author-name search; not identity confirmation.
- `search_by_author_exact(records, author_name, limit=None)`: stricter name-token search; still not identity confirmation.
- `search_by_institution(records, institution, limit=None)`: search institution field.
- `search_by_journal(records, journal, limit=None)`: search journal field.
- `search_by_publisher(records, publisher, limit=None)`: search publisher field.
- `classify_retraction_reason(reason_text)`: keyword-based reason tagging; not official adjudication.
- `generate_author_history_summary(records, author_name)`: summarize name-matched records with boundary warnings.

## `src.benchmark`

- `load_benchmark_cases(path)`: load synthetic benchmark cases.
- `run_benchmark(cases)`: compare expected and actual classifications.
- `summarize_benchmark(results)`: summarize benchmark pass/fail status.

## `src.validation`

- `load_validation_cases(path)`: load curated real-case validation registry.
- `run_validation(cases)`: compare model behavior with expected cautious outputs.
- `summarize_validation(results)`: summarize validation status and boundary risks.

## `src.sensitivity`

- `WEIGHT_PROFILES`: pilot, biomedical, clinical, and author-history profiles.
- `evaluate_weight_profiles(scores)`: compare TRS/classification across profiles.
- `perturbation_grid(scores)`: test one-at-a-time weight perturbations.
- `classification_stability(rows)`: summarize classification robustness.
- `rank_stability_summary(cases)`: estimate ranking stability across profiles.

## `src.expert_review`

- `aggregate_expert_weights(responses)`: aggregate expert module weights.
- `mean_weight_profile(responses)`: create a normalized mean profile.
- `expert_disagreement_matrix(responses)`: compare expert weight profiles.
- `compare_delphi_rounds(round1, round2)`: summarize Delphi-style changes.
- `calibration_status(responses)`: generate cautious calibration-status summary.

## `src.project_audit`

- `verify_expected_files(root_path)`: check whether expected project files are present.
- `find_cache_artifacts(root_path)`: detect `__pycache__` or `.pytest_cache` artifacts.
- `release_readiness_summary(root_path)`: return a lightweight pre-release readiness summary.


## Runtime cache note for project audit

`release_readiness_summary()` checks the current directory tree. If tests have just been run, Python may create local `__pycache__` or `.pytest_cache` directories. For release packaging, run the audit on a clean export or delete runtime-generated cache directories before creating the zip artifact.


## Simulated Expert Workflow Utilities

```python
from src.simulated_expert import (
    literature_informed_simulated_profile,
    validate_simulated_expert_row,
    simulated_panel_summary,
)
```

These utilities validate simulated expert-review rows and enforce safeguards that simulated data are for workflow testing only. They do not create real expert consensus or calibration evidence.
