# SOP: Data and Statistical Analysis for Research Integrity Risk Assessment

## 1. Purpose

This SOP establishes a structured, reproducible workflow for assessing whether a scholarly article shows risks of fabrication, falsification, image manipulation, statistical inconsistency, unsupported claims, paper-mill involvement, compromised peer review, or repeated research-integrity concerns.

The SOP does **not** determine guilt or intent. Confirmed misconduct requires official notices, original data, journal investigation, institutional review, funder findings, or equivalent formal records.

## 2. Scope

Applicable to empirical research papers, especially biomedical, biomedical engineering, tissue engineering, biomaterials, cell-study, animal-study, preclinical, clinical, epidemiological, and molecular-biology articles.

## 3. Definitions

- **Anomaly:** an observed irregularity in figures, tables, statistics, raw data, methods, conclusions, or external records.
- **Concern:** an anomaly that remains relevant after considering benign explanations.
- **Manipulation risk:** a concern that suggests possible deliberate or non-deliberate alteration of figures, data, or analysis.
- **Confirmed misconduct:** a formal classification based on official wording such as fabrication, falsification, plagiarism, image manipulation, fake peer review, research misconduct, or equivalent terms.
- **Repeated misconduct pattern:** multiple formally supported records involving a confirmed same author or group, repeated similar problems, and insufficient benign explanations.

## 4. Formal Logic Foundation

Do not infer fraud directly from anomaly.

Invalid inference:

```text
Observed anomaly -> fraud
```

Valid inference:

```text
Observed anomaly
+ independent verification
+ insufficient benign explanation
+ database or official record
= research-integrity concern
```

Confirmed misconduct requires an additional condition:

```text
Official notice or institutional/funder finding explicitly states misconduct-type wording.
```

## 5. Article Decomposition

A paper should be decomposed into nine modules before judgment:

| Module | Name | Main target |
|---|---|---|
| M1 | Figures/images | duplication, rotation, cropping, mirroring, splicing, manipulation |
| M2 | Tables | impossible values, inconsistent n, duplicated rows, non-integer percentages |
| M3 | Statistics | p values, SD/SEM, sample size, tests, confidence intervals |
| M4 | Raw data | source data, repositories, uncropped blots, supplementary files |
| M5 | Methods | controls, ethics, replicates, randomization, blinding |
| M6 | Conclusions | overclaim, unsupported translation, causal overreach |
| M7 | External databases | retraction, correction, PubPeer, Crossref, PubMed, journal notices |
| M8 | Author history | repeated records, same-author confirmation, repeated patterns |
| M9 | Responsibility | contribution, corresponding author, formal attribution |

## 6. Module-Level Analysis

### M1 Figures/images

Check for complete duplication, cropped duplication, rotation, mirroring, contrast-adjusted reuse, background reuse, spliced blots/gels, and whether representative images support quantification.

### M2 Tables

Check sample-size consistency, non-integer percentages, duplicated rows, impossible values, inconsistent covariates, and mismatch between main tables and supplementary tables.

### M3 Statistics

Recalculate p values when possible, distinguish SD from SEM, check degrees of freedom, verify n, check multiple-comparison correction, and identify implausible p-value clustering or over-perfect results.

### M4 Raw data

Check whether raw/source data exist, whether source data reproduce published figures, whether uncropped blots are available, whether data repositories are accessible, and whether core data are missing or contradicted.

### M5 Methods

Check controls, randomization, blinding, ethics approval, biological vs technical replicates, batch effects, and whether methods are sufficient to reproduce the experiment.

### M6 Conclusions

Check whether claims exceed evidence: cell-only evidence presented as clinical translation, small animal studies described as clinical-ready, correlation presented as causation, or short-term data used for long-term safety claims.

### M7 External databases

Check Retraction Watch/Crossref, Retraction Database, PubPeer, PubMed, journal notices, Crossmark status, and institutional/funder announcements. External records are important but cannot alone determine intent unless official wording is explicit.

### M8 Author history

Check repeated formal records, same-author identity, ORCID, affiliation, research area, email, coauthor network, repeated reasons, and time patterns. Avoid same-name misattribution.

### M9 Responsibility

Check author contribution statements, corresponding author role, data curator, statistician, lab leadership, and whether official records assign responsibility. Paper-level risk is not the same as person-level responsibility.

## 7. Module Scoring

Each module is scored from 0 to 5:

| Score | Meaning |
|---:|---|
| 0 | No visible concern |
| 1 | Minor inconsistency |
| 2 | Clear concern |
| 3 | Serious anomaly |
| 4 | Strong manipulation risk |
| 5 | Officially confirmed issue |

## 8. Weighting Model

The current weights are pilot expert-prior weights:

| Module | Weight |
|---|---:|
| M1 Figures/images | 0.18 |
| M2 Tables | 0.08 |
| M3 Statistics | 0.15 |
| M4 Raw data | 0.18 |
| M5 Methods | 0.08 |
| M6 Conclusions | 0.07 |
| M7 External databases | 0.12 |
| M8 Author history | 0.09 |
| M9 Responsibility | 0.05 |

```text
TRS = M1×0.18 + M2×0.08 + M3×0.15 + M4×0.18 + M5×0.08 + M6×0.07 + M7×0.12 + M8×0.09 + M9×0.05
```

The weights are not yet empirically validated. They should be recalibrated through expert review, benchmark cases, sensitivity analysis, and empirical validation.

## 9. Preliminary TRS Categories

| TRS | Preliminary category |
|---:|---|
| 0.0–0.9 | C0 No visible concern |
| 1.0–1.9 | C1 Minor concern |
| 2.0–2.9 | C2 Serious concern |
| 3.0–3.9 | C3 Strong manipulation risk |
| 4.0–5.0 | Very high concern; official-record review required |

TRS alone cannot produce C5 confirmed misconduct or C6 repeated misconduct pattern.

## 10. Hard Logic Overrides

### C4 Formal correction or retraction
Use C4 if there is an official correction, retraction, expression of concern, withdrawal, or removal, but the wording does not explicitly establish misconduct.

### C5 Confirmed misconduct
Use C5 only if official records explicitly state misconduct-type wording, including fabrication, falsification, plagiarism, image manipulation, fake peer review, compromised peer review, paper mill involvement, research misconduct, or equivalent terms.

### C6 Repeated misconduct pattern
Use C6 only if all are satisfied:

1. same-author identity is confirmed;
2. multiple formal records exist;
3. similar reasons or anomaly patterns repeat;
4. responsibility or role is plausibly linked;
5. benign explanations such as same-name confusion, publisher error, isolated coauthorship, or honest error are insufficient.

### C7 Possible non-intentional error or inconclusive retraction
Use C7 when official records point to honest error, calculation error, methodological flaw, publisher error, inability to reproduce, or inconclusive findings, especially when authors cooperated and no repeated pattern is found.

## 11. Intent Assessment

Database fields cannot directly reveal intent. Intent is inferred only cautiously from combinations of evidence:

- stronger intentionality signals: official wording of fabrication/falsification/manipulation, raw data contradicting published results, repeated similar issues, fake peer review, paper-mill wording, responsibility attribution;
- non-intentional or inconclusive signals: honest error wording, author-initiated correction, publisher error, methodological limitation, no repeated pattern, raw data provided.

## 12. Report Writing

Recommended wording:

```text
Based on available evidence, this article shows [minor/serious/strong] research-integrity concerns involving [modules]. This assessment does not by itself prove intentional misconduct. Formal confirmation requires original data, author explanation, journal review, and/or institutional investigation.
```

Avoid language such as “this author is fraudulent” unless formal records explicitly support that classification and responsibility attribution.

## 13. Limitations

- Public databases are incomplete.
- Retraction notices may be vague.
- Same-name author matching can be wrong.
- TRS weights are pilot expert-prior values.
- Image analysis may require specialized tools and raw images.
- Intent cannot be read directly from data.
- The framework is decision support, not adjudication.
