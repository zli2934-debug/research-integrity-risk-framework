# Future Validation Plan

## Phase 1. Real-case benchmark set

Construct a curated benchmark set using only cases with formal public records. Suggested groups:

- confirmed misconduct cases
- formal retraction without misconduct wording
- correction cases
- honest-error or non-intentional cases
- expression-of-concern cases
- clean control articles

## Phase 2. Annotation protocol

Develop an annotation sheet separating:

- article-level issue
- database record
- official wording
- author identity confidence
- responsibility attribution
- inferred risk level
- uncertainty level

## Phase 3. Weight sensitivity analysis

Test whether classification outcomes are stable under:

- equal weights
- biomedical experimental weights
- clinical/statistical weights
- author-history-focused weights
- random perturbations around current weights

## Phase 4. Reason classification evaluation

Measure keyword-based reason classification against manually coded labels.

## Phase 5. Author-name false-positive audit

Estimate false-positive risks in author-name search by comparing:

- exact name match
- normalized name match
- DOI-linked authorship
- affiliation-supported identity
- ORCID-supported identity when available

## Phase 6. Expert review

Invite independent reviewers from relevant areas:

- biomedical research
- statistics
- publication ethics
- research integrity
- journal editing
- data curation

## Phase 7. Revision and calibration

Revise weights, reason categories, and hard override conditions based on benchmark results and expert feedback.

## v0.6-alpha Case-Validation Infrastructure

The v1.0.0 package retains a validation module and templates for curated official-case validation. These materials support the future validation plan but do not replace independent citation checking or official-notice verification.


## Weight sensitivity and calibration plan added in v0.7-alpha

The pilot expert-prior weights should be evaluated using:

1. scenario-specific profiles;
2. one-at-a-time perturbation analysis;
3. rank-stability testing across cases;
4. curated real-case benchmark sets;
5. expert review or Delphi-style consensus in later versions.

v1.0.0 retains the v0.7 sensitivity-analysis infrastructure, but it does not yet claim empirically optimized weights.


## v1.0.0 Expert Review and Calibration Protocol

v1.0.0 adds infrastructure for semi-structured expert interviews, expert weight surveys, Delphi-style feedback, disagreement metrics, and weight calibration planning. This stage is protocol-level. It does not claim that expert interviews have already been completed or that weights are empirically optimal.

If interviews are used for publishable research, the team should consult the relevant institutional review process before collecting expert data.
