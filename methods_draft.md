# Methods Draft

## Framework design

The Research Integrity Risk Framework is designed as a transparent, rule-based system for preliminary assessment of research-integrity risk in scholarly articles. The framework does not assign guilt, intent, or personal responsibility. Instead, it organizes evidence into structured modules and applies explicit decision rules to separate preliminary risk levels from formal record-based classifications.

## Evidence modules

Each article or case is decomposed into nine modules:

| Module | Description |
|---|---|
| M1 | Figures and images |
| M2 | Tables |
| M3 | Statistics |
| M4 | Raw data and supplementary files |
| M5 | Methods and experimental design |
| M6 | Claims and conclusions |
| M7 | External database and post-publication records |
| M8 | Author-history records |
| M9 | Responsibility attribution |

Each module is scored from 0 to 5. A score of 0 indicates no visible concern. A score of 5 is reserved for a formally confirmed issue. Intermediate scores represent increasing levels of concern, from minor inconsistency to strong manipulation risk.

## Total Risk Score

The preliminary Total Risk Score is calculated as a weighted sum of module scores. The current weights are pilot expert-prior weights based on evidentiary proximity, verifiability, and misclassification risk. They are not empirically optimized and should be recalibrated in future work using expert review, real-case benchmarks, and sensitivity analysis.

## Classification system

The framework uses C0–C7 categories. C0–C3 describe preliminary risk levels based on the Total Risk Score. C4–C7 require formal-record or hard-logic conditions. In particular, confirmed misconduct requires official wording, and repeated misconduct pattern requires multiple formal records, confirmed same-author identity, repeated similar pattern, clear responsibility, and official misconduct wording.

## Database integration

The database module supports Retraction Watch CSV loading, DOI search, author-name search, institution search, journal search, publisher search, reason classification, timeline generation, author-history summary, and evidence table generation. Database outputs include boundary notes stating that database evidence is not a misconduct determination or identity confirmation.

## Benchmark testing

Synthetic benchmark cases are used to test whether the implemented logic produces expected classifications. These cases cover C0–C7 examples and are intended to validate implementation behavior, not empirical real-world performance. Unit tests cover scoring functions, hard logic overrides, database utilities, and benchmark execution.

## Verification workflow

All outputs are subject to a second-pass verification workflow. The audit step checks source accuracy, formal logic, scoring calculations, hard override behavior, classification boundaries, and ethical or misuse risk. Outputs may be marked as Verified, Needs Revision, Unsupported, or Risky Claim.
