# Introduction Draft

Research integrity assessment requires careful separation between observable risk signals and formal determinations of misconduct. Public records such as retraction notices, correction notices, database entries, and post-publication discussions can provide useful evidence, but they are often heterogeneous, incomplete, and difficult to interpret without a standardized workflow. In particular, a retraction does not necessarily imply intentional misconduct, a database name match does not necessarily confirm author identity, and a post-publication concern does not necessarily establish responsibility.

The challenge is especially important in biomedical and experimental research, where published conclusions may rely on multiple evidence layers: images, quantitative tables, statistical tests, raw data, experimental methods, and translational claims. A concern in one layer may be minor or explainable; convergent concerns across multiple layers may require more careful review. At the same time, ethical safeguards are necessary to prevent overinterpretation, public accusation, and identity-based error.

This manuscript introduces the Research Integrity Risk Framework, an open-source, alpha-stage framework designed to organize article-level and database-level research-integrity evidence. The framework uses nine evidence modules, a 0–5 module scoring scheme, a weighted Total Risk Score, formal logic rules, hard classification overrides, and a second-pass verification workflow. The purpose is not to determine guilt or intent, but to provide a transparent, reproducible, and bounded method for preliminary research-integrity risk assessment.

The framework is implemented as a rule-based Python toolkit and documentation package. It includes Retraction Watch CSV integration for evidence organization, while explicitly distinguishing database records from formal adjudication. The current version also includes synthetic benchmark cases to test rule implementation. These benchmarks demonstrate that the implementation follows the intended logic, but they do not constitute empirical validation of the model weights or real-world predictive performance.

The contribution of this work is therefore methodological. It proposes a structured approach for converting heterogeneous research-integrity signals into a transparent audit trail, while preserving clear boundaries between risk assessment, evidence organization, and formal misconduct determination.

## Citation note

This draft intentionally avoids unsourced numerical background claims. Before submission, the introduction should be expanded with verified citations to the research-integrity, retraction, meta-research, and publication ethics literature.
