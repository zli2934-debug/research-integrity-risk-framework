# Changelog

## v1.1-prep.1

- Documentation/version-consistency patch for v1.1-prep.
- Fixed residual current-package version markers from v1.0.0 to v1.1-prep.1.
- Fixed malformed source docstrings including `v1.1-prep.1` and `v1.1-prep.1`.
- Added patch release notes, release readiness report, and final audit report.
- No scoring/database/benchmark/validation/sensitivity/expert-review/simulated-expert logic changes.

## v1.1-prep

- Added literature-informed simulated expert-review workflow placeholders.
- Added hybrid online/offline interview simulation examples.
- Added simulated Delphi Round 1 / Round 2 example files.
- Added `src/simulated_expert.py` and tests.
- Added safeguards to keep simulated expert data separate from real expert validation and calibration evidence.

# Changelog

## v1.0.0

Final v1.0.0 stable release prepared from v1.0-rc1 after release-candidate audit. This version consolidates the full framework into the first stable release package and adds final release notes, release-readiness report, and final audit report. No scoring, database, benchmark, validation, sensitivity, or expert-review logic was changed from the audited release candidate.

Boundary: v1.0.0 is a stable framework release, but it is not a completed empirical validation study, not a misconduct detector, and not a substitute for formal review.

## v0.9.1-alpha

Citation metadata and final pre-release cleanup patch.

- Corrected `CITATION.cff`: `cff-version` now uses the Citation File Format schema version `1.2.0` rather than the project version.
- Updated project package version markers to `v0.9.1-alpha` / `0.9.1a0`.
- Added release-audit guidance distinguishing package-artifact cache checks from runtime-generated local cache files that may appear after tests.
- Preserved all scoring, database, benchmark, validation, sensitivity, expert-review, and project-audit logic.

## v0.9-alpha

Pre-release consolidation and project-integration release.

- Added `docs/pre_release_consolidation.md`.
- Added `docs/api_reference.md`.
- Added `docs/release_checklist.md`.
- Added `docs/final_audit_checklist.md`.
- Added `docs/repository_manuscript_map.md`.
- Added `docs/v1_0_roadmap.md`.
- Added `templates/release_readiness_report_template.md`.
- Added `templates/final_audit_report_template.md`.
- Added `src/project_audit.py` for expected-file, cache-artifact, private-data, and release-readiness checks.
- Added `tests/test_project_audit.py`.
- Updated README, model card, citation metadata, and package version to v0.9-alpha.
- No changes to core scoring, database, benchmark, validation, sensitivity, or expert-review logic.

## v0.8.1-alpha

- Documentation-consistency patch for the v0.8 Expert Review and Calibration Protocol Release.
- Updated current package version markers to v0.8.1-alpha across README, model card, code docstrings, templates, manuscript planning files, and documentation.
- Clarified that modules introduced in earlier releases are retained in v0.8.1-alpha.
- Strengthened interview ethics guidance: before conducting in-person interviews for publishable or publicly released work, project teams should obtain a determination from the relevant institutional review body / human-subjects review office.
- No scoring, database, benchmark, validation, sensitivity, or expert-review logic was changed.

## v0.8.1-alpha

Expert Review and Calibration Protocol Release.

- Added `src/expert_review.py` for expert weight aggregation, disagreement metrics, Delphi round comparison, and calibration-status summaries.
- Added `docs/expert_review_protocol.md`.
- Added `docs/interview_ethics_and_consent.md`.
- Added `docs/weight_calibration_protocol.md`.
- Added expert-review templates: semi-structured interview guide, information sheet, expert weight survey, feedback matrix, and expert review report.
- Added `examples/expert_weight_responses_template.csv`.
- Added `manuscript/expert_review_methods_plan.md`.
- Added tests for expert-review utilities.
- Updated README, model card, publication roadmap, manuscript future-validation plan, citation metadata, and package version to v0.8.1-alpha.
- Important boundary: v0.8 provides expert-review protocol infrastructure; it does not claim that expert review has already been completed or that weights are empirically optimal.

## v0.7.1-alpha

Documentation-consistency patch for v0.7-alpha.

- Corrected `docs/publication_roadmap.md` so the current package is described as a documentation-consistency patch for the v0.7 Weight Sensitivity Analysis Release, not as a real-case validation infrastructure patch.
- Updated README, model card, citation metadata, package metadata, and `src.__version__` to v0.7.1-alpha.
- Preserved all v0.7 sensitivity-analysis functionality.
- No scoring, database, benchmark, validation, or sensitivity-analysis logic was changed.

## v0.7-alpha

Weight Sensitivity Analysis Release.

- Added `src/sensitivity.py` for weight sensitivity analysis.
- Added built-in weight profiles: pilot expert-prior, biomedical experimental, clinical/epidemiology, and author-history review.
- Added one-at-a-time weight perturbation utilities.
- Added classification-stability and rank-stability summaries.
- Added `docs/weight_sensitivity.md`.
- Added `templates/sensitivity_analysis_report_template.md`.
- Added `examples/sensitivity_cases.csv`.
- Added `tests/test_sensitivity.py`.
- Boundary: v0.7-alpha tests robustness of pilot weights; it does not empirically optimize or validate weights.

## v0.6.3-alpha

Final documentation consistency patch before v0.7.

- Corrected remaining package-version marker in `manuscript/references_plan.md`.
- Updated package metadata to v0.6.3-alpha.
- No scoring, database, benchmark, or validation logic was changed.

## v0.6.2-alpha

Documentation consistency cleanup patch.

- Cleaned residual v0.6/v0.6.1 version-scope wording.
- Clarified component introduction versions versus current package version.
- Preserved real-case validation infrastructure.

## v0.6.1-alpha

Documentation / version-scope consistency patch for v0.6-alpha.

- Corrected README version scope from method-paper patch wording to real-case validation infrastructure wording.
- Retained the boundary that v0.6 provides validation infrastructure, not completed empirical validation.

## v0.6-alpha

Real-Case Validation Infrastructure Release.

- Added `src/validation.py`.
- Added `docs/case_validation_workflow.md`.
- Added real-case validation registry and report templates.
- Added validation summary and boundary-risk checks.
- Boundary: v0.6-alpha provides validation infrastructure, not completed large-scale empirical validation.

## v0.5.1-alpha

Manuscript/documentation consistency patch.

- Corrected C6 wording to require clear responsibility, not merely plausible responsibility.
- Added citation-planning scaffolds.

## v0.5-alpha

Method Paper Framework Release.

- Added manuscript title, abstract, outline, introduction, methods, limitations, figure/table plan, and future validation plan drafts.
- Boundary: v0.5-alpha is a method-paper drafting layer, not a submission-ready manuscript.

## v0.4-alpha

Benchmark and Validation Release.

- Added synthetic benchmark cases and benchmark execution utilities.
- Added EvidenceLevel and SourceConfidence fields.
- Boundary: synthetic benchmark success does not prove empirical validity.

## v0.3-alpha

Database Integration Release.

- Added Retraction Watch CSV loading and search utilities.
- Added DOI, author-name, institution, journal, publisher, reason-category, timeline, and evidence-table utilities.
- Boundary: database evidence organization does not confirm author identity, misconduct, intent, or responsibility.

## v0.2.1-alpha

Audit-fix patch for v0.2-alpha.

- Tightened C6 responsibility conditions.
- Restricted C7 overrides for high-risk cases.
- Added verification workflow and audit-report template.

## v0.2-alpha

Rule-based scoring model release.

- Added TRS scoring, C0-C7 classification, hard overrides, definitions, limitations, and model-card documentation.

## v0.1-alpha

Initial prototype.

- Added initial SOP, nine-module scoring concept, preliminary weights, and templates.
