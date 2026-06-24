# Real-Case Validation Workflow

Component introduced: v0.6-alpha

Current package version: v1.1-prep.1

## Purpose

v0.6-alpha introduced a structured real-case validation layer; v1.0.0 retains it and the v0.7 sensitivity-analysis layer. The goal is to test whether the framework behaves conservatively when applied to curated cases with documented source status, expected classification prefixes, identity boundaries, and responsibility boundaries.

This layer does **not** claim that the model is empirically validated, statistically optimal, or capable of detecting misconduct by itself.

## What the v0.6 Validation Layer Adds

- `src/validation.py` for curated case validation.
- `examples/real_case_validation_template.csv` as a demonstration validation file.
- `templates/real_case_validation_registry_template.csv` for user-curated validation registries.
- `templates/case_validation_report_template.md` for validation reporting.
- `docs/case_validation_workflow.md` to define source and boundary rules.

## Required Source-Boundary Rules

Strong categories require strong source metadata:

| Category | Required boundary evidence |
|---|---|
| C4 | formal correction, retraction, or expression of concern record |
| C5 | official misconduct-type wording |
| C6 | multiple formal records + confirmed same-author identity + repeated similar pattern + clear responsibility + official misconduct-type wording |
| C7 | official wording consistent with non-misconduct/error/inconclusive record + no high TRS / high core-module abnormality |

Secondary database evidence, including Retraction Watch records, should be verified against official journal or institutional notices before being used for strong categories.

## Validation Status Labels

`src.validation` generates three important audit fields:

- `source_verification_status`: whether source metadata is sufficient.
- `boundary_risk_status`: whether the expected category risks overclaiming.
- `validation_passed`: whether model prediction, source verification, and boundary checks all pass.

## Interpreting Validation Results

A validation pass means:

> Given the provided scores, flags, and source metadata, the framework generated the expected classification prefix without violating source-boundary rules.

A validation pass does **not** mean:

- the model can detect misconduct,
- the model is legally or institutionally authoritative,
- the weights are empirically optimal,
- author identity has been confirmed by the tool alone,
- responsibility has been assigned by the tool alone.

## Recommended v0.7 Usage

1. Select official cases from journal notices, institutional statements, or verified formal records.
2. Enter cases into `templates/real_case_validation_registry_template.csv`.
3. Use C4-C7 only when source-boundary requirements are satisfied.
4. Run `src.validation.run_validation()`.
5. Manually review any `NEEDS_REVIEW`, `RISKY_C5_BOUNDARY`, or `RISKY_C6_BOUNDARY` outputs.
6. Write a case-validation report using `templates/case_validation_report_template.md`.

## Current Limitation

v1.0.0 retains the real-case validation infrastructure and demonstration cases while adding weight-sensitivity analysis. A publication-ready validation set still requires manually verified official notices and citation checking.
