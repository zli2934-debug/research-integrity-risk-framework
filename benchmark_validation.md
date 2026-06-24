# Benchmark and Validation Plan

Component introduced: v0.4-alpha; current package version: v1.0.0

## Purpose

The v0.4-alpha benchmark layer, retained in v1.0.0, adds a benchmark layer to test whether the framework's rule logic behaves as expected across synthetic and, later, officially documented cases. This is a validation workflow for implementation logic, not a claim that the model is empirically optimal.

## Benchmark Categories

The benchmark should include at minimum:

1. Clean controls expected to classify as C0.
2. Serious concern cases without formal records expected to classify as C2 or C3.
3. Very high scoring cases without official records expected to classify as C3+, not C5.
4. Formal correction/retraction cases expected to classify as C4 unless official misconduct wording exists.
5. Official misconduct wording cases expected to classify as C5.
6. Repeated confirmed pattern cases expected to classify as C6 only when identity, repeated pattern, clear responsibility, multiple formal records, and official misconduct wording are all present.
7. Non-misconduct/error wording cases expected to classify as C7 only when high TRS and high core-module abnormalities are absent.

## Required Audit Checks

Each benchmark run should check:

- TRS calculation.
- C0-C3+ threshold behavior.
- C4-C7 hard-logic override behavior.
- C7 high-risk blocking behavior.
- C6 identity and responsibility requirements.
- Whether reason keyword classification produces plausible but not overclaimed categories.
- Whether author-name matching warnings are preserved.

## EvidenceLevel and SourceConfidence

The retained benchmark/database layer includes database evidence metadata:

- `EvidenceLevel`: a conservative description of what kind of database record is available.
- `SourceConfidence`: a boundary statement emphasizing that Retraction Watch-derived evidence should be checked against official notices before adjudication.

These fields do not measure truth or guilt. They describe evidence handling.

## Release Boundary

A benchmark pass means the implementation follows expected rule logic for provided cases. It does not prove that the framework can replace formal institutional investigation, peer review, image-integrity review, or expert statistical audit.
