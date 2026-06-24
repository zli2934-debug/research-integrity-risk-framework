from pathlib import Path

from src.benchmark import load_benchmark_cases, run_benchmark, summarize_benchmark, write_benchmark_report_markdown


def test_benchmark_cases_all_pass(tmp_path):
    cases = load_benchmark_cases(Path("examples") / "benchmark_cases.csv")
    results = run_benchmark(cases)
    summary = summarize_benchmark(results)
    assert summary["total_cases"] == 8
    assert summary["failed_cases"] == 0
    assert summary["status"] == "PASS"


def test_benchmark_report_writes(tmp_path):
    cases = load_benchmark_cases(Path("examples") / "benchmark_cases.csv")
    results = run_benchmark(cases)
    out = write_benchmark_report_markdown(results, tmp_path / "benchmark_report.md")
    text = out.read_text(encoding="utf-8")
    assert "Benchmark Report" in text
    assert "SYN-C6-001" in text
    assert "PASS" in text
