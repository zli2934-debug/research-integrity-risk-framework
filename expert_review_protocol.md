# Expert Review Protocol

**Component introduced:** v1.0.0  
**Current package version:** v1.0.0

## Purpose

This protocol describes how to use expert review to refine the Research Integrity Risk Framework. The purpose is to evaluate whether the module weights, hard-logic rules, and classification boundaries are reasonable for different scholarly contexts.

Expert review is used for calibration planning, not final truth-making. Expert agreement does not prove that a weight profile is empirically optimal, and expert disagreement should be reported rather than hidden.

## Recommended study design

The preferred design is a mixed expert-review process:

1. semi-structured interview;
2. structured module-weight survey;
3. review of synthetic cases;
4. optional review of officially documented public cases;
5. Delphi-style feedback round;
6. documented revision of weight profiles and boundary rules.

## Expert panel composition

Recommended target: 10–15 experts if feasible.

Suggested categories:

- biomedical or biomedical engineering researchers;
- statistics or biostatistics experts;
- publication ethics or research-integrity personnel;
- journal editors or experienced peer reviewers;
- image-integrity or data-integrity specialists;
- database / metadata curation specialists.

A smaller pilot panel can be used for internal alpha testing, but limitations must be disclosed.

## Interview format

Recommended duration: 30–45 minutes.

Core interview topics:

- which evidence modules should carry higher or lower weight;
- when C5 or C6 should be allowed;
- whether C7 should override high TRS cases;
- how to interpret Retraction Watch, official notices, PubPeer, and other records;
- safeguards against same-name author errors;
- safeguards against over-attribution of responsibility;
- differences between biomedical experimental, clinical, and author-history contexts.

## Structured weight survey

Experts should assign M1–M9 weights using either:

- percentages that sum to 100;
- points that are later normalized;
- decimals that sum to 1.

Responses should be normalized before aggregation. The aggregation output should include mean, median, standard deviation, min, max, and range for each module.

## Delphi-style round

After Round 1, the research team can provide experts with anonymized aggregate results and areas of disagreement. Experts may then revise their weights in Round 2. The protocol should report whether the panel converged, but convergence should not be described as empirical truth.

## Output artifacts

- expert_weight_matrix.csv;
- expert_feedback_matrix.csv;
- interview_summary_table.csv;
- expert_disagreement_report.md;
- calibration_protocol.md;
- updated scenario-specific weight profiles.

## Boundaries

This protocol must not be used to label an individual as having committed misconduct. It is designed to improve a risk-assessment framework and preserve uncertainty.
