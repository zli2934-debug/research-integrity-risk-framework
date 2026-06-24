# Database Fields and Mapping

## Retraction Watch CSV Fields

Recommended fields from the Retraction Watch/Crossref CSV include:

- Record ID
- Title
- Subject
- Institution
- Journal
- Publisher
- Country
- Author
- URLS
- ArticleType
- RetractionDate
- RetractionDOI
- RetractionPubMedID
- OriginalPaperDate
- OriginalPaperDOI
- OriginalPaperPubMedID
- RetractionNature
- Reason
- Paywalled
- Notes

## Suggested Mapping

| Field | Use in model |
|---|---|
| Title / OriginalPaperDOI | Article identity |
| Author | Author-history matching; requires disambiguation |
| Institution / Country | Institutional context, not personal proof |
| Journal / Publisher | Publisher-pattern analysis |
| RetractionDate / OriginalPaperDate | Time-to-retraction analysis |
| RetractionNature | C4 status detection |
| Reason | C5/C7 wording extraction |
| Notes / URLS | Evidence source tracing |

## Data Use Notice

Do not redistribute stale database copies inside this repository. Users should obtain current data from official sources and comply with applicable terms.


## v0.4 Utility Mapping

- DOI search checks `OriginalPaperDOI`, `RetractionDOI`, and DOI-like strings in `URLS`.
- Author search uses the `Author` field as a text field and does not confirm identity.
- Institution, journal, and publisher searches use substring matching.
- Reason classification is keyword-based and should be reviewed manually.
- Evidence tables export core bibliographic, retraction, reason, and boundary-note fields.
