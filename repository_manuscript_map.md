# Repository-Manuscript Map

**Current package version:** v1.0.0

This file maps repository components to likely manuscript sections.

| Manuscript section | Repository support |
|---|---|
| Introduction | `manuscript/introduction_draft.md`, `docs/limitations.md` |
| Methods: scoring framework | `docs/scoring_model.md`, `src/scoring.py`, `tests/test_scoring.py` |
| Methods: database integration | `docs/database_integration.md`, `src/database.py`, `tests/test_database.py` |
| Methods: verification workflow | `docs/verification_workflow.md`, `templates/audit_report_template.md` |
| Methods: benchmark | `docs/benchmark_validation.md`, `src/benchmark.py`, `examples/benchmark_cases.csv` |
| Methods: real-case validation | `docs/case_validation_workflow.md`, `src/validation.py`, validation templates |
| Methods: sensitivity analysis | `docs/weight_sensitivity.md`, `src/sensitivity.py`, sensitivity templates |
| Methods: expert review | `docs/expert_review_protocol.md`, `docs/weight_calibration_protocol.md`, `src/expert_review.py` |
| Ethics and limitations | `manuscript/limitations_and_ethics.md`, `docs/ethical_guidelines.md`, `docs/interview_ethics_and_consent.md` |
| Figures and tables | `manuscript/figures_and_tables_plan.md` |
| References | `manuscript/references_plan.md`, `manuscript/citation_verification_table.csv` |

## Boundary

Repository files are scaffolds and implementation support. They do not remove the need for citation verification, real-case validation, or independent review before manuscript submission.
