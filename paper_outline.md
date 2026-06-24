# Method Paper Outline

## 1. Introduction

- Research integrity concerns have become increasingly visible in post-publication review, retraction databases, and editorial notices.
- Public databases are valuable, but database records alone do not establish author identity, intent, or responsibility.
- Existing discussions often lack a standardized workflow for separating risk signals from formal misconduct determinations.
- This paper proposes a transparent, modular, and ethically bounded framework for preliminary research-integrity risk assessment.

## 2. Conceptual foundation

- Distinguish research-integrity risk from confirmed misconduct.
- Distinguish article-level concerns from author-level responsibility.
- Distinguish database evidence from official adjudication.
- Treat retraction, correction, expression of concern, and post-publication discussion as different evidence types.

## 3. Framework architecture

- Nine evidence modules:
  - M1 Figures/images
  - M2 Tables
  - M3 Statistics
  - M4 Raw data/supplementary material
  - M5 Methods/design
  - M6 Claims/conclusions
  - M7 External database records
  - M8 Author-history records
  - M9 Responsibility attribution
- Module scoring from 0 to 5.
- Total Risk Score using pilot expert-prior weights.
- C0–C7 classification structure.
- C4–C7 hard logic override rules.

## 4. Database integration

- Retraction Watch CSV loading.
- DOI search.
- Author-name search with identity caveat.
- Institution, journal, and publisher search.
- Keyword-based reason classification.
- Evidence table generation with boundary notes.
- Retraction Database web search as manual verification rather than stable programmatic source.

## 5. Benchmark and validation design

- Synthetic benchmark cases for logic testing.
- Full CSV loading smoke test.
- Test suite for scoring, database, and benchmark modules.
- Limitations of synthetic validation.
- Future need for formally curated real-case benchmarks.

## 6. Ethical safeguards

- No automatic fraud determination.
- No automatic author identity confirmation.
- No automatic responsibility assignment.
- No substitution for institutional, journal, or legal procedures.
- Required second-pass verification workflow.

## 7. Limitations

- Pilot expert-prior weights are not empirically optimal.
- Reason classification is keyword-based.
- Public database records may be incomplete or ambiguous.
- Author-name matching has false-positive risk.
- Synthetic benchmarks do not prove real-world performance.

## 8. Future work

- Expert Delphi weighting.
- Real-case benchmark set.
- Honest-error and clean-control article cohorts.
- Sensitivity analysis.
- Improved DOI and author normalization.
- Independent third-party review.

## 9. Conclusion

- The framework provides a transparent and reproducible structure for organizing research-integrity risk evidence.
- It should be used as a preliminary assessment and documentation system, not a final adjudication tool.
