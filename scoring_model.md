# Scoring Model

## 1. Formula

```text
TRS = M1×0.18 + M2×0.08 + M3×0.15 + M4×0.18 + M5×0.08 + M6×0.07 + M7×0.12 + M8×0.09 + M9×0.05
```

Each module score ranges from 0 to 5. The total risk score also ranges from 0 to 5.

## 2. Weight Status

The current weighting scheme is a **pilot expert-prior model**. It is not claimed to be empirically optimal.

Weights are assigned based on:

1. **Evidentiary proximity**: modules closer to primary evidence receive higher weights.
2. **Verifiability**: modules with more directly testable evidence receive higher weights.
3. **Misclassification risk**: modules vulnerable to identity confusion or attribution error receive lower weights unless supported by official records.

## 3. Default Weights

| Module | Weight | Rationale |
|---|---:|---|
| M1 Figures/images | 0.18 | Primary evidence in biomedical articles; image duplication/manipulation can directly affect conclusions |
| M2 Tables | 0.08 | Useful for numerical consistency but often requires cross-checking |
| M3 Statistics | 0.15 | Tests whether reported significance is reproducible from reported data |
| M4 Raw data | 0.18 | Source data are central to verifying published claims |
| M5 Methods | 0.08 | Method flaws affect reliability but do not automatically imply fabrication |
| M6 Conclusions | 0.07 | Overclaim signals risk but does not alone imply misconduct |
| M7 External databases | 0.12 | Formal records matter but public databases are not adjudication by themselves |
| M8 Author history | 0.09 | Important for repeated-pattern analysis, but identity errors are possible |
| M9 Responsibility | 0.05 | Crucial for final attribution, but usually requires formal investigation |

## 4. Hard Logic Overrides

TRS is a risk score, not a final misconduct verdict. The following override rules must be applied after calculating TRS:

- **C4** if official correction/retraction/expression of concern exists but misconduct wording is absent or unclear.
- **C5** if official wording states fabrication, falsification, plagiarism, image manipulation, fake peer review, paper mill involvement, or research misconduct.
- **C6** if multiple formal records, confirmed same-author identity, repeated similar patterns, clear responsibility, and official misconduct-type wording are present.
- **C7** if official records indicate honest error, methodological flaw, publisher error, inability to reproduce, or inconclusive retraction, especially with author cooperation and no repeated pattern.

## 5. Future Calibration Plan

Future versions should validate and recalibrate weights using:

1. expert Delphi scoring;
2. confirmed-misconduct benchmark cases;
3. non-misconduct retraction benchmark cases;
4. clean control articles;
5. sensitivity analysis;
6. ablation analysis;
7. inter-rater reliability testing.

## 6. Scenario-Specific Weights

Future versions may include separate weight profiles for:

- biomedical experimental articles;
- clinical/epidemiological articles;
- author-history or repeated-pattern analysis;
- publisher-level or institution-level analysis.


## v0.2.1-alpha classification boundary update

TRS >= 4 is classified as `C3+ Very high manipulation risk; official-record review required`. TRS alone does not trigger C4, C5, or C6. C4-C7 require formal-record or non-misconduct/error wording flags.

C6 requires clear responsibility, not merely plausible responsibility. C7 should not override high TRS or high core-module abnormality in M1, M3, or M4.


## v0.7-alpha weight sensitivity note

The default weights are pilot expert-prior weights. v0.7-alpha introduces scenario-specific profiles and perturbation analysis in `src/sensitivity.py`. These profiles are for robustness testing only and should not be described as empirically optimized.
