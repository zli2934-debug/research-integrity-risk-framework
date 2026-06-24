# Release Checklist

**Current package version:** v1.0.0

Before any public release or preprint-associated repository release, complete this checklist.

## Required checks

- [ ] All tests pass with `python -m pytest`.
- [ ] No `__pycache__`, `.pytest_cache`, private data, raw Retraction Watch CSV, or personal notes are included in the release zip.
- [ ] README version matches `src.__version__`, `pyproject.toml`, and `CITATION.cff`.
- [ ] The release does not claim empirical validation unless real-case validation has been completed and audited.
- [ ] The release does not claim expert-validated optimal weights unless expert review has been completed and documented.
- [ ] All examples are synthetic or properly documented public cases.
- [ ] Author-name search is explicitly described as not identity confirmation.
- [ ] C5/C6 outputs require official wording and clear responsibility criteria.
- [ ] Manuscript citations have been verified before any manuscript submission.

## Release decision

Use one of four outcomes:

- `Verified`: ready for current release scope.
- `Needs Revision`: release after fixes.
- `Unsupported`: remove or cite unsupported claim.
- `Risky Claim`: revise to avoid over-attribution or misconduct adjudication.


## Runtime cache note

The release-readiness audit is intended for a clean package artifact. Running tests locally may generate `__pycache__` or `.pytest_cache` after the zip has been unpacked. These runtime-generated local cache files should be deleted before packaging and should not be interpreted as evidence that the original release artifact contained cache files.
