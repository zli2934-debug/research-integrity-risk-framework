import csv
from pathlib import Path

import pytest

from src.simulated_expert import (
    literature_informed_simulated_profile,
    validate_simulated_expert_row,
    simulated_panel_summary,
)
from src.expert_review import mean_weight_profile, compare_delphi_rounds

ROOT = Path(__file__).resolve().parents[1]


def _read_csv(rel):
    with open(ROOT / rel, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def test_literature_informed_profile_sums_to_one():
    profile = literature_informed_simulated_profile()
    assert round(sum(profile.values()), 6) == 1.0
    assert profile['M4'] >= 0.16


def test_simulated_panel_rows_have_required_safeguards():
    rows = _read_csv('examples/literature_informed_simulated_expert_panel.csv')
    assert len(rows) == 10
    for row in rows:
        validate_simulated_expert_row(row)
        assert row['UseForCalibration'] == 'No'
        assert row['UseForPublicationResult'] == 'No'
        assert row['UseForWorkflowTesting'] == 'Yes'


def test_simulated_panel_summary_counts_modes():
    rows = _read_csv('examples/literature_informed_simulated_expert_panel.csv')
    summary = simulated_panel_summary(rows)
    assert summary['n_simulated_experts'] == 10
    assert 'In-person mock interview' in summary['by_interview_mode']
    assert 'workflow rehearsal only' in summary['safeguard']


def test_simulated_rows_reject_calibration_use():
    row = _read_csv('examples/literature_informed_simulated_expert_panel.csv')[0]
    row = dict(row)
    row['UseForCalibration'] = 'Yes'
    with pytest.raises(ValueError):
        validate_simulated_expert_row(row)


def test_delphi_simulation_rounds_are_comparable():
    r1 = _read_csv('examples/literature_informed_simulated_delphi_round_1.csv')
    r2 = _read_csv('examples/literature_informed_simulated_delphi_round_2.csv')
    result = compare_delphi_rounds(r1, r2)
    assert result['l1_profile_shift'] >= 0
    assert round(sum(result['round2_mean_profile'].values()), 6) == 1.0
