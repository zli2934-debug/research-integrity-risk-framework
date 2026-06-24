# Database Integration: Retraction Watch CSV

## Purpose

This database integration layer was introduced before v0.6-alpha and is retained in the current package. It provides a lightweight Retraction Watch CSV integration layer. The goal is to organize external database evidence, not to automate misconduct findings.

## Supported Functions

The `src.database` module currently supports:

- CSV loading through `load_retraction_watch_csv()`;
- DOI search through `search_by_doi()`;
- author-name string search through `search_by_author()`;
- institution search through `search_by_institution()`;
- journal search through `search_by_journal()`;
- publisher search through `search_by_publisher()`;
- keyword-based reason classification through `classify_retraction_reason()`;
- retraction timeline generation through `retraction_timeline()`;
- cautious author-name history summaries through `generate_author_history_summary()`;
- compact evidence table export through `write_evidence_table_csv()`.

## Supported Fields

The expected Retraction Watch CSV fields include:

- `Record ID`
- `Title`
- `Subject`
- `Institution`
- `Journal`
- `Publisher`
- `Country`
- `Author`
- `URLS`
- `ArticleType`
- `RetractionDate`
- `RetractionDOI`
- `OriginalPaperDate`
- `OriginalPaperDOI`
- `RetractionNature`
- `Reason`
- `Notes`

The loader ignores empty or unnamed columns.

## Reason Classification

Reason classification is keyword-based and conservative. A positive category means that the database reason text contains a relevant signal. It does **not** prove misconduct, intent, or responsibility.

Current categories include:

- misconduct or integrity concern;
- image or figure concern;
- data or results concern;
- statistical or methods concern;
- peer review or authorship concern;
- plagiarism or duplication;
- ethical or approval concern;
- publisher or administrative error;
- honest error or inconclusive.

## Identity Boundary

Author-name search is not identity verification. The same string may refer to different people, and a matched record does not establish personal responsibility. Any person-level summary must be independently checked against institutional affiliations, ORCID, coauthors, time period, official notices, and article-level responsibility statements.

## Data-Use Boundary

This repository does not redistribute Retraction Watch data. Users should download the current dataset from official sources and follow applicable data-use terms. Retraction Database web search may require manual verification and should not be treated as a stable programmatic data source.
