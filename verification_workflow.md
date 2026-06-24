# Independent Verification Workflow

## Purpose

All framework outputs should undergo a second-pass verification step before they are treated as release-ready. This workflow is an internal audit layer, not an external institutional investigation.

The goal is to reduce source errors, formal-logic mistakes, arithmetic errors, classification overreach, and ethical misuse.

## Two-Pass Workflow

```text
Pass 1: Draft construction
        ↓
Pass 2: Independent verification / audit
        ↓
Pass 3: Revision
        ↓
Pass 4: Release candidate
```

## Audit Domains

### 1. Source Verification

Check whether each factual claim is supported by an appropriate source.

Labels:

- `Verified`
- `Partially verified`
- `Needs citation`
- `Unsupported`
- `Conflicting evidence`

### 2. Formal Logic Audit

Reject invalid reasoning patterns such as:

- Retraction → fraud
- PubPeer comment → confirmed misconduct
- Multiple retractions → serial fraudster
- Same name → same author
- High TRS → confirmed misconduct
- Database record → author intent

Allowed reasoning:

- Data anomaly → risk signal
- Multiple independent anomalies → serious concern
- Official misconduct wording → confirmed misconduct
- Multiple formal records + confirmed identity + repeated pattern + clear responsibility → repeated misconduct pattern

### 3. Quantitative Audit

Check:

- module scores are 0–5
- weights sum to 1.00
- TRS calculations are reproducible
- examples match code output
- tests pass
- hard-logic overrides are triggered only under allowed conditions

### 4. Classification Boundary Audit

Verify that the output does not overclaim.

C5 requires official misconduct-type wording.
C6 requires multiple formal records, confirmed same-author identity, repeated pattern, and clear responsibility.
C7 must not automatically override high TRS or high core evidence risk.

### 5. Ethics and Misuse Audit

Check for:

- personal accusation beyond official records
- same-name author misattribution
- treating coauthors as equally responsible without evidence
- national or institutional stigmatization
- missing uncertainty language
- missing disclaimer that the framework is not an adjudication system

## Release Decision

| Decision | Meaning |
|---|---|
| Verified | Ready for release within stated scope |
| Needs Revision | Problems found; revise before release |
| Unsupported | Evidence is insufficient |
| Risky Claim | Ethical, legal, or overclaim risk; rewrite required |

## Required Release Note

Every release should state whether it has passed internal second-pass verification and list unresolved limitations.
