from pathlib import Path

from src.project_audit import (
    EXPECTED_FILES,
    verify_expected_files,
    find_cache_artifacts,
    find_private_data_artifacts,
    release_readiness_summary,
)


def _make_minimal_repo(root: Path) -> None:
    for rel in EXPECTED_FILES:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("placeholder", encoding="utf-8")


def test_verify_expected_files_on_repo_root():
    root = Path(__file__).resolve().parents[1]
    result = verify_expected_files(root)
    assert result["status"] == "PASS"
    assert result["missing_count"] == 0


def test_cache_artifact_detection_on_clean_and_dirty_tmp_repo(tmp_path):
    _make_minimal_repo(tmp_path)
    assert find_cache_artifacts(tmp_path) == []
    (tmp_path / "src" / "__pycache__").mkdir(parents=True)
    assert find_cache_artifacts(tmp_path) == ["src/__pycache__"]


def test_private_data_detection(tmp_path):
    _make_minimal_repo(tmp_path)
    assert find_private_data_artifacts(tmp_path) == []
    (tmp_path / "data").mkdir(exist_ok=True)
    (tmp_path / "data" / "retraction_watch.csv").write_text("private raw data", encoding="utf-8")
    assert find_private_data_artifacts(tmp_path) == ["data/retraction_watch.csv"]


def test_release_readiness_summary_has_boundary_note(tmp_path):
    _make_minimal_repo(tmp_path)
    result = release_readiness_summary(tmp_path)
    assert result["release_readiness"] == "PASS"
    assert "does not imply empirical validation" in result["boundary_note"]
