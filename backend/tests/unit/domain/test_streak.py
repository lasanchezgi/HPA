from datetime import date
from uuid import uuid4

import pytest

from src.domain.entities.streak import Streak


@pytest.fixture
def habit_id():
    return uuid4()


def test_first_completion_sets_streak_to_1(habit_id):
    streak = Streak(habit_id=habit_id, current_streak=0, best_streak=0, last_completed_date=None)
    updated = streak.update_after_completion(date(2024, 1, 1))

    assert updated.current_streak == 1
    assert updated.best_streak == 1
    assert updated.last_completed_date == date(2024, 1, 1)


def test_consecutive_day_increments_streak(habit_id):
    streak = Streak(
        habit_id=habit_id,
        current_streak=3,
        best_streak=5,
        last_completed_date=date(2024, 1, 1),
    )
    updated = streak.update_after_completion(date(2024, 1, 2))

    assert updated.current_streak == 4
    assert updated.best_streak == 5
    assert updated.last_completed_date == date(2024, 1, 2)


def test_skipped_day_resets_streak_to_1(habit_id):
    streak = Streak(
        habit_id=habit_id,
        current_streak=5,
        best_streak=5,
        last_completed_date=date(2024, 1, 1),
    )
    updated = streak.update_after_completion(date(2024, 1, 3))

    assert updated.current_streak == 1
    assert updated.best_streak == 5
    assert updated.last_completed_date == date(2024, 1, 3)


def test_best_streak_never_decreases(habit_id):
    streak = Streak(
        habit_id=habit_id,
        current_streak=4,
        best_streak=4,
        last_completed_date=date(2024, 1, 4),
    )
    updated = streak.update_after_completion(date(2024, 1, 5))

    assert updated.current_streak == 5
    assert updated.best_streak == 5

    reset = updated.update_after_completion(date(2024, 1, 10))
    assert reset.current_streak == 1
    assert reset.best_streak == 5


def test_same_day_completion_does_not_change_streak(habit_id):
    streak = Streak(
        habit_id=habit_id,
        current_streak=3,
        best_streak=3,
        last_completed_date=date(2024, 1, 1),
    )
    updated = streak.update_after_completion(date(2024, 1, 1))

    assert updated.current_streak == 3
    assert updated.best_streak == 3
