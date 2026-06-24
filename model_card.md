# Model Card: Research Integrity Risk Framework v1.1-prep.1

Current package version: v1.1-prep.1. Components introduced in earlier versions are retained unless noted otherwise.

## Model type

Transparent rule-based scoring framework with hard logic overrides, database evidence organization, validation infrastructure, weight sensitivity analysis, and expert-review protocol support. This is not a misconduct adjudication system.

## Intended use

- Research-integrity education
- Structured literature screening
- Evidence mapping
- Preliminary risk assessment
- Case-report drafting

## Out-of-scope use

- Determining guilt or intent
- Publicly accusing individuals
- Replacing institutional, journal, funder, or legal investigations
- Automated personal misconduct labeling

## Inputs

- Module scores M1–M9
- External database status
- Official correction/retraction/misconduct wording
- Author identity and repeated-pattern evidence
- Alternative explanations and author cooperation information

## Outputs

- TRS score from 0 to 5
- C0–C7 classification
- Recommended cautious wording

## Known risks

- Misclassification from incomplete records
- Same-name author errors
- Overweighting weak public allegations
- Confusing paper-level risk with person-level responsibility

## Validation status

Not yet empirically validated. v0.8 introduced expert-review and calibration protocol infrastructure; v0.9 adds pre-release consolidation and project-integration utilities. Expert review has not yet been completed. Current weights are pilot expert-prior weights.


## Independent verification status

This release includes an internal second-pass verification workflow. It has not undergone external third-party validation. All classifications remain preliminary risk assessments unless supported by official records.


## v0.4 Database Integration Boundary

The database-integration component was introduced in v0.3/v0.4-alpha and is retained in v1.1-prep.1. It includes Retraction Watch CSV loading and search utilities. These utilities organize records by DOI, author-name string, institution, journal, publisher, reason category, and timeline. They do not confirm author identity, misconduct, intent, or personal responsibility.

## v1.1-prep.1 Validation Boundary

v0.6-alpha introduced curated case-validation infrastructure; v1.1-prep.1 retains it. Validation cases must be source-verified and boundary-audited before being used for manuscript claims. Passing a validation case indicates consistency with provided scores, flags, and source metadata; it does not prove empirical optimality or assign misconduct.


## v0.7-alpha sensitivity-analysis layer retained in v1.1-prep.1

v0.7-alpha added `src/sensitivity.py`; v1.1-prep.1 retains it for testing whether TRS and preliminary classifications remain stable under alternative pilot weight profiles. This is a robustness and transparency feature, not empirical weight calibration.

The model remains an alpha-stage framework. Sensitivity stability does not establish misconduct, intent, identity, responsibility, or publication-ready validity.


## v0.9 Pre-release Consolidation

v1.1-prep.1 adds pre-release integration documents, an API reference, final audit checklists, repository-manuscript mapping, and project-level release-readiness utilities. It does not claim final empirical validation or production readiness.
