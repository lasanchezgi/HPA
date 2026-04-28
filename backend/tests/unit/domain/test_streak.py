from datetime import date
from uuid import uuid4

import pytest

from backend.src.domain.entities.streak import Streak


@pytest.fixture
def habit_id():
    return uuid4()


def test_streak_handles_first_completion(habit_id):
    streak = Streak(habit_id=habit_id, current_streak=0, best_streak=0, last_completed_date=None)
    updated = streak.update_after_completion(date(2024, 1, 1))

    assert updated.current_streak == 1
    assert updated.best_streak == 1
    assert updated.last_completed_date == date(2024, 1, 1)


def test_streak_increments_on_consecutive_day(habit_id):
    streak = Streak(
        habit_id=habit_id,
        current_streak=3,
        best_streak=5,
        last_completed_date=date(2024, 1, 1),
    )
    updated = streak.update_after_completion(date(2024, 1, 2))

    assert updated.current_streak == 4
    assert updated.best_streak == 5  # not beaten yet
    assert updated.last_completed_date == date(2024, 1, 2)


def test_streak_resets_when_day_skipped(habit_id):
    streak = Streak(
        habit_id=habit_id,
        current_streak=5,
        best_streak=5,
        last_completed_date=date(2024, 1, 1),
    )
    updated = streak.update_after_completion(date(2024, 1, 3))  # skipped Jan 2

    assert updated.current_streak == 1
    assert updated.best_streak == 5  # best preserved
    assert updated.last_completed_date == date(2024, 1, 3)


def test_streak_updates_best_streak(habit_id):
    streak = Streak(
        habit_id=habit_id,
        current_streak=4,
        best_streak=4,
        last_completed_date=date(2024, 1, 4),
    )
    updated = streak.update_after_completion(date(2024, 1, 5))

    assert updated.current_streak == 5
    assert updated.best_streak == 5


def test_streak_same_day_is_idempotent(habit_id):
    streak = Streak(
        habit_id=habit_id,
        current_streak=3,
        best_streak=3,
        last_completed_date=date(2024, 1, 1),
    )
    updated = streak.update_after_completion(date(2024, 1, 1))

    assert updated.current_streak == 3
    assert updated.best_streak == 3
