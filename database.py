"""Database utilities for Research Integrity Risk Framework v1.1-prep.1.

This module provides lightweight Retraction Watch CSV integration:
loading, DOI/author/institution/journal/publisher search, reason keyword
classification, timelines, author-history summaries, and evidence-table export.

Boundary rule: these utilities organize database evidence. They do not confirm
misconduct, intent, author identity, or personal responsibility.
"""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

Record = Dict[str, str]

CORE_FIELDS: Tuple[str, ...] = (
    "Record ID",
    "Title",
    "Author",
    "Institution",
    "Journal",
    "Publisher",
    "Country",
    "ArticleType",
    "RetractionDate",
    "RetractionNature",
    "Reason",
    "RetractionDOI",
    "OriginalPaperDOI",
    "URLS",
)

REASON_KEYWORDS: Dict[str, Sequence[str]] = {
    "misconduct_or_integrity_concern": (
        "misconduct",
        "falsification",
        "fabrication",
        "fake",
        "paper mill",
        "third party",
        "investigation",
        "manipulation",
    ),
    "image_or_figure_concern": (
        "image",
        "figure",
        "western blot",
        "gel",
        "duplication",
        "duplicat",
        "reuse",
    ),
    "data_or_results_concern": (
        "data",
        "results",
        "conclusions",
        "raw data",
        "unreliable",
        "error in data",
    ),
    "statistical_or_methods_concern": (
        "statistical",
        "statistics",
        "method",
        "analysis",
        "randomization",
        "clinical trial",
    ),
    "peer_review_or_authorship_concern": (
        "peer review",
        "authorship",
        "author",
        "approval",
        "consent",
    ),
    "plagiarism_or_duplication": (
        "plagiarism",
        "plagiar",
        "duplicate publication",
        "duplication of article",
        "copyright",
    ),
    "ethical_or_approval_concern": (
        "irb",
        "ethics",
        "ethical",
        "approval",
        "consent",
        "animal",
        "human",
    ),
    "publisher_or_administrative_error": (
        "publisher error",
        "published in error",
        "withdrawn",
        "administrative",
    ),
    "honest_error_or_inconclusive": (
        "error",
        "mistake",
        "contamination",
        "unreliable",
        "unable to reproduce",
        "not reproducible",
    ),
}


def _clean_text(value: object) -> str:
    """Return a normalized single-line string for search and export."""
    if value is None:
        return ""
    return " ".join(str(value).replace("\ufeff", "").split())


def normalize_doi(value: str) -> str:
    """Normalize a DOI or DOI URL for case-insensitive matching."""
    text = _clean_text(value).lower()
    text = re.sub(r"^https?://(dx\.)?doi\.org/", "", text)
    text = text.replace("doi:", "").strip()
    return text.rstrip(".,; ")


def normalize_header(header: str) -> str:
    """Normalize CSV headers while preserving Retraction Watch field names."""
    return _clean_text(header)


def load_retraction_watch_csv(path: str | Path, max_rows: Optional[int] = None) -> List[Record]:
    """Load Retraction Watch CSV records into a list of dictionaries.

    Parameters
    ----------
    path:
        Path to the Retraction Watch CSV file.
    max_rows:
        Optional row limit for testing or previews.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    records: List[Record] = []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            return []
        fieldnames = [normalize_header(name) for name in reader.fieldnames]
        for raw_row in reader:
            row: Record = {}
            for original, normalized in zip(reader.fieldnames, fieldnames):
                if not normalized or normalized.startswith("Unnamed"):
                    continue
                row[normalized] = _clean_text(raw_row.get(original, ""))
            records.append(row)
            if max_rows is not None and len(records) >= max_rows:
                break
    return records


def search_records(records: Iterable[Record], field: str, query: str, limit: Optional[int] = None) -> List[Record]:
    """Search records by case-insensitive substring match in one field."""
    q = _clean_text(query).lower()
    if not q:
        return []
    results: List[Record] = []
    for row in records:
        value = _clean_text(row.get(field, "")).lower()
        if q in value:
            results.append(row)
            if limit is not None and len(results) >= limit:
                break
    return results


def search_by_doi(records: Iterable[Record], doi: str, limit: Optional[int] = None) -> List[Record]:
    """Search records by DOI across original-paper and retraction DOI fields."""
    q = normalize_doi(doi)
    if not q:
        return []
    results: List[Record] = []
    for row in records:
        dois = [
            normalize_doi(row.get("OriginalPaperDOI", "")),
            normalize_doi(row.get("RetractionDOI", "")),
        ]
        urls = _clean_text(row.get("URLS", "")).lower()
        if q in dois or q in urls:
            results.append(row)
            if limit is not None and len(results) >= limit:
                break
    return results


def search_by_author(records: Iterable[Record], author_query: str, limit: Optional[int] = None) -> List[Record]:
    """Search the Author field.

    Warning: name matching does not confirm same-author identity. Identity
    confirmation requires independent verification.
    """
    return search_records(records, "Author", author_query, limit=limit)



def _normalize_name(value: str) -> str:
    """Normalize author names for conservative exact-name matching."""
    return re.sub(r"\s+", " ", _clean_text(value).lower()).strip(" ,;.")


def search_by_author_exact(records: Iterable[Record], author_name: str, limit: Optional[int] = None) -> List[Record]:
    """Search for exact normalized author-name tokens inside the Author field.

    This is stricter than substring search but still does not confirm same-author
    identity. It only reduces obvious substring false positives.
    """
    target = _normalize_name(author_name)
    if not target:
        return []
    results: List[Record] = []
    for row in records:
        author_field = _clean_text(row.get("Author", ""))
        candidates = [
            _normalize_name(part)
            for part in re.split(r";|\|", author_field)
            if _normalize_name(part)
        ]
        if target in candidates or _normalize_name(author_field) == target:
            results.append(row)
            if limit is not None and len(results) >= limit:
                break
    return results


def evidence_level_from_record(row: Record) -> str:
    """Assign a conservative evidence level for database-derived records."""
    if _clean_text(row.get("RetractionDOI", "")) or _clean_text(row.get("OriginalPaperDOI", "")):
        return "database_record_with_doi"
    if _clean_text(row.get("URLS", "")):
        return "database_record_with_url"
    return "database_record_metadata_only"


def source_confidence_from_record(row: Record) -> str:
    """Describe source-confidence boundary for Retraction Watch-derived evidence."""
    if _clean_text(row.get("RetractionNature", "")) or _clean_text(row.get("Reason", "")):
        return "secondary_database_record; verify against official notice before adjudication"
    return "secondary_database_record; incomplete metadata; manual verification required"


def search_by_institution(records: Iterable[Record], institution_query: str, limit: Optional[int] = None) -> List[Record]:
    return search_records(records, "Institution", institution_query, limit=limit)


def search_by_journal(records: Iterable[Record], journal_query: str, limit: Optional[int] = None) -> List[Record]:
    return search_records(records, "Journal", journal_query, limit=limit)


def search_by_publisher(records: Iterable[Record], publisher_query: str, limit: Optional[int] = None) -> List[Record]:
    return search_records(records, "Publisher", publisher_query, limit=limit)


def classify_retraction_reason(reason: str) -> Dict[str, bool]:
    """Map a Retraction Watch Reason string to broad risk-signal categories.

    This is keyword-based and conservative. It is not a legal or institutional
    finding. A True value means the reason text contains a signal related to the
    category, not that misconduct is proven.
    """
    text = _clean_text(reason).lower()
    return {
        category: any(keyword in text for keyword in keywords)
        for category, keywords in REASON_KEYWORDS.items()
    }


def summarize_reason_categories(records: Iterable[Record]) -> Dict[str, int]:
    """Count keyword-based reason categories across records."""
    counts: Counter[str] = Counter()
    for row in records:
        classes = classify_retraction_reason(row.get("Reason", ""))
        for category, present in classes.items():
            if present:
                counts[category] += 1
    return dict(counts)


def retraction_timeline(records: Iterable[Record]) -> Dict[str, int]:
    """Return counts by retraction year using the RetractionDate field."""
    counts: Counter[str] = Counter()
    for row in records:
        date = _clean_text(row.get("RetractionDate", ""))
        match = re.search(r"(19|20)\d{2}", date)
        if match:
            counts[match.group(0)] += 1
        else:
            counts["unknown"] += 1
    return dict(sorted(counts.items()))


def top_values(records: Iterable[Record], field: str, n: int = 10) -> List[Tuple[str, int]]:
    """Return top non-empty values for a field."""
    counts: Counter[str] = Counter()
    for row in records:
        value = _clean_text(row.get(field, ""))
        if value:
            counts[value] += 1
    return counts.most_common(n)


def generate_author_history_summary(records: Sequence[Record], author_query: str) -> Dict[str, object]:
    """Generate a cautious author-name search summary.

    The returned summary deliberately uses `matched_name_records`, not
    `confirmed_author_records`, because name matching alone does not confirm
    identity.
    """
    matched = search_by_author(records, author_query)
    return {
        "query": author_query,
        "matched_name_records": len(matched),
        "identity_warning": "Name matching alone does not confirm same-author identity or responsibility.",
        "timeline": retraction_timeline(matched),
        "top_journals": top_values(matched, "Journal", n=10),
        "top_publishers": top_values(matched, "Publisher", n=10),
        "top_institutions": top_values(matched, "Institution", n=10),
        "top_countries": top_values(matched, "Country", n=10),
        "reason_categories": summarize_reason_categories(matched),
    }


def evidence_table_from_records(records: Iterable[Record], limit: Optional[int] = None) -> List[Record]:
    """Create a compact evidence table from records using core fields."""
    table: List[Record] = []
    for row in records:
        evidence_row = {field: _clean_text(row.get(field, "")) for field in CORE_FIELDS}
        reason_classes = classify_retraction_reason(evidence_row.get("Reason", ""))
        evidence_row["ReasonCategories"] = ";".join(
            category for category, present in reason_classes.items() if present
        )
        evidence_row["EvidenceLevel"] = evidence_level_from_record(row)
        evidence_row["SourceConfidence"] = source_confidence_from_record(row)
        evidence_row["BoundaryNote"] = (
            "Database evidence only; not a misconduct determination or identity confirmation."
        )
        table.append(evidence_row)
        if limit is not None and len(table) >= limit:
            break
    return table


def write_evidence_table_csv(records: Iterable[Record], output_path: str | Path, limit: Optional[int] = None) -> Path:
    """Write compact evidence table CSV and return output path."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    table = evidence_table_from_records(records, limit=limit)
    fieldnames = list(CORE_FIELDS) + ["ReasonCategories", "EvidenceLevel", "SourceConfidence", "BoundaryNote"]
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(table)
    return output_path
