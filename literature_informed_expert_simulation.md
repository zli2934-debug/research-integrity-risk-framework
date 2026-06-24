# Literature-Informed Simulated Expert Review Layer

**Current package version:** v1.1-prep.1  
**Data status:** Simulated / literature-informed placeholder  
**Use for calibration:** No  
**Use for publication result:** No  
**Use for workflow testing:** Yes

## Purpose

This layer provides a workflow rehearsal for a future hybrid expert review process. It simulates how online surveys, Zoom interviews, and in-person semi-structured interviews might produce expert weight preferences and qualitative feedback.

The simulated panel is not a real expert panel. It is not evidence of expert consensus. It must not be used to claim that the model weights are empirically validated or expert-calibrated.

## Literature Rationale

- COPE retraction guidance emphasizes that retraction is intended to correct the literature and preserve its integrity rather than punish authors. This supports the framework's distinction between formal correction/retraction, confirmed misconduct, and possible non-intentional error.
- Retraction Watch reason taxonomy distinguishes categories such as results/conclusions concerns, third-party involvement, peer review concerns, plagiarism/duplication, data concerns, and image concerns. This supports a modular evidence design rather than a single retraction = misconduct shortcut.
- Delphi methodology uses iterative expert questionnaires with controlled feedback to seek expert consensus. This supports a Round 1 / Round 2 workflow for later real expert review, but simulated Delphi rounds remain only workflow tests.

## Simulated Aggregate Profile

| Module | Weight | Interpretation |
|---|---:|---|
| M1 Figures/images | 0.16 | High relevance in biomedical/life-science integrity review |
| M2 Tables | 0.09 | Important for clinical and tabular evidence |
| M3 Statistics | 0.16 | Core signal for data consistency and reliability |
| M4 Raw data | 0.17 | Highest-value reproducibility evidence |
| M5 Methods | 0.10 | Experimental design and ethical approvals affect reliability |
| M6 Conclusions | 0.07 | Overclaim matters, but should not dominate |
| M7 External records | 0.13 | Formal database/journal records organize evidence but do not adjudicate misconduct |
| M8 Author history | 0.07 | Useful but limited by same-name and identity-confirmation risk |
| M9 Responsibility | 0.05 | Critical as hard-logic condition, but not high as a TRS-weighted module |

## Files

- `examples/literature_informed_simulated_expert_panel.csv`
- `examples/literature_informed_simulated_delphi_round_1.csv`
- `examples/literature_informed_simulated_delphi_round_2.csv`
- `templates/literature_review_to_expert_preference_matrix.csv`
- `templates/hybrid_interview_log_template.md`
- `manuscript/simulated_expert_review_placeholder.md`

## Safeguards

All simulated rows must include:

```text
DataType = Simulated
EvidenceStatus = Literature-informed placeholder
UseForCalibration = No
UseForPublicationResult = No
UseForWorkflowTesting = Yes
```

Real expert data must be stored separately and should only be used for calibration or publication if consent and institutional review requirements allow it.
