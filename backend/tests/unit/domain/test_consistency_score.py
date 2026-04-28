import pytest

from backend.src.domain.value_objects.consistency_score import ConsistencyScore


def test_perfect_consistency_returns_100():
    score = ConsistencyScore(completed_days=30, total_days_since_start=30)
    assert score.value == 100.0


def test_zero_days_returns_zero_score():
    score = ConsistencyScore(completed_days=0, total_days_since_start=0)
    assert score.value == 0.0


def test_consistency_label_master_above_90():
    score = ConsistencyScore(completed_days=91, total_days_since_start=100)
    assert score.label() == "Master"


def test_consistency_label_consistent_between_70_and_90():
    score = ConsistencyScore(completed_days=75, total_days_since_start=100)
    assert score.label() == "Consistent"


def test_consistency_label_building_between_40_and_70():
    score = ConsistencyScore(completed_days=50, total_days_since_start=100)
    assert score.label() == "Building"


def test_consistency_label_beginner_below_40():
    score = ConsistencyScore(completed_days=20, total_days_since_start=100)
    assert score.label() == "Beginner"


def test_partial_completion_calculates_correctly():
    score = ConsistencyScore(completed_days=15, total_days_since_start=30)
    assert score.value == 50.0


def test_invalid_completed_days_raises():
    with pytest.raises(ValueError):
        ConsistencyScore(completed_days=31, total_days_since_start=30)
