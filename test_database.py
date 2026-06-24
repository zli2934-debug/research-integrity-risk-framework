from pathlib import Path

from src.database import (
    classify_retraction_reason,
    evidence_table_from_records,
    generate_author_history_summary,
    load_retraction_watch_csv,
    retraction_timeline,
    search_by_author,
    search_by_doi,
    search_by_institution,
    search_by_journal,
    search_by_publisher,
    summarize_reason_categories,
    write_evidence_table_csv,
)


def make_fixture(tmp_path: Path) -> Path:
    csv_path = tmp_path / "rw_fixture.csv"
    csv_path.write_text(
        "Record ID,Title,Author,Institution,Journal,Publisher,Country,ArticleType,RetractionDate,RetractionNature,Reason,RetractionDOI,OriginalPaperDOI,URLS\n"
        "1,Paper A,Smith J; Wang X,University A,Journal One,Publisher A,USA,Research Article,2021-05-01,Retraction,Image duplication; Data concerns,10.1000/retract.a,10.1000/original.a,https://doi.org/10.1000/original.a\n"
        "2,Paper B,Wang X,Hospital B,Journal Two,Publisher B,China,Research Article,2022-06-02,Correction,Publisher error; honest error,10.1000/retract.b,10.1000/original.b,\n"
        "3,Paper C,Garcia M,University C,Journal One,Publisher A,Spain,Review,2022-07-03,Expression of Concern,Peer review concerns; Third party involvement,,10.1000/original.c,\n",
        encoding="utf-8",
    )
    return csv_path


def test_load_retraction_watch_csv(tmp_path):
    records = load_retraction_watch_csv(make_fixture(tmp_path))
    assert len(records) == 3
    assert records[0]["Title"] == "Paper A"
    assert records[0]["OriginalPaperDOI"] == "10.1000/original.a"


def test_search_by_doi_matches_original_and_url(tmp_path):
    records = load_retraction_watch_csv(make_fixture(tmp_path))
    assert search_by_doi(records, "https://doi.org/10.1000/original.a")[0]["Record ID"] == "1"
    assert search_by_doi(records, "10.1000/retract.b")[0]["Record ID"] == "2"


def test_search_by_author_is_name_string_only(tmp_path):
    records = load_retraction_watch_csv(make_fixture(tmp_path))
    matches = search_by_author(records, "Wang X")
    assert len(matches) == 2


def test_search_by_institution_journal_publisher(tmp_path):
    records = load_retraction_watch_csv(make_fixture(tmp_path))
    assert len(search_by_institution(records, "University")) == 2
    assert len(search_by_journal(records, "Journal One")) == 2
    assert len(search_by_publisher(records, "Publisher A")) == 2


def test_classify_retraction_reason_keyword_categories():
    result = classify_retraction_reason("Image duplication; Data concerns; Peer review concerns")
    assert result["image_or_figure_concern"] is True
    assert result["data_or_results_concern"] is True
    assert result["peer_review_or_authorship_concern"] is True


def test_summarize_reason_categories_and_timeline(tmp_path):
    records = load_retraction_watch_csv(make_fixture(tmp_path))
    categories = summarize_reason_categories(records)
    timeline = retraction_timeline(records)
    assert categories["image_or_figure_concern"] == 1
    assert categories["publisher_or_administrative_error"] == 1
    assert timeline["2022"] == 2


def test_author_history_summary_has_identity_warning(tmp_path):
    records = load_retraction_watch_csv(make_fixture(tmp_path))
    summary = generate_author_history_summary(records, "Wang X")
    assert summary["matched_name_records"] == 2
    assert "does not confirm" in summary["identity_warning"]


def test_evidence_table_and_write_csv(tmp_path):
    records = load_retraction_watch_csv(make_fixture(tmp_path))
    table = evidence_table_from_records(records, limit=1)
    assert len(table) == 1
    assert "ReasonCategories" in table[0]
    assert "Database evidence only" in table[0]["BoundaryNote"]

    output = tmp_path / "evidence.csv"
    write_evidence_table_csv(records, output, limit=2)
    assert output.exists()
    assert "BoundaryNote" in output.read_text(encoding="utf-8")



def test_evidence_table_includes_evidence_level_and_source_confidence():
    records = [
        {
            "Record ID": "1",
            "Title": "Example",
            "Reason": "Concerns about data and results",
            "OriginalPaperDOI": "10.1000/example",
            "RetractionNature": "Retraction",
        }
    ]
    table = evidence_table_from_records(records)
    assert table[0]["EvidenceLevel"] == "database_record_with_doi"
    assert "secondary_database_record" in table[0]["SourceConfidence"]


def test_search_by_author_exact_reduces_substring_false_positive():
    from src.database import search_by_author_exact

    records = [
        {"Author": "Li, Zihao; Wang, A"},
        {"Author": "Liu, Zihaoming; Chen, B"},
    ]
    results = search_by_author_exact(records, "Li, Zihao")
    assert len(results) == 1
    assert results[0]["Author"].startswith("Li, Zihao")
