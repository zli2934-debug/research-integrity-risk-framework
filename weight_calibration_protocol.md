# Weight Calibration Protocol

**Component introduced:** v1.0.0  
**Current package version:** v1.0.0

## Status

The framework currently uses pilot expert-prior weights. v0.8 adds a protocol for expert-informed calibration, but it does not claim calibrated optimal weights.

## Calibration inputs

- expert weight survey responses;
- semi-structured interview feedback;
- synthetic benchmark performance;
- curated real-case validation results;
- sensitivity analysis outputs;
- disagreement metrics.

## Calibration steps

1. Collect initial expert weights.
2. Normalize all weight vectors to sum to 1.
3. Aggregate mean and median weights.
4. Identify high-disagreement modules.
5. Run sensitivity analysis using expert-derived profiles.
6. Compare results against synthetic and curated real-case benchmarks.
7. Conduct a Delphi-style feedback round if feasible.
8. Document all changes and limitations.

## Output

The output should be a proposed weight profile, not a claim of final truth. The report should describe:

- number and category of experts;
- aggregation method;
- disagreement metrics;
- changed modules;
- rationale for changes;
- remaining uncertainties.

## Required disclaimer

Expert-informed calibration improves transparency and face validity. It does not by itself prove predictive validity, misconduct detection accuracy, or empirical optimality.
