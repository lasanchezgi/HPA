from datetime import date, datetime, timezone, timedelta
from uuid import uuid4

import pytest

from backend.src.domain.entities.habit import Habit


@pytest.fixture
def base_habit():
    return Habit(
        id=uuid4(),
        user_id=uuid4(),
        habit_name="Read 30 minutes",
        frequency_id=uuid4(),
        category_id=uuid4(),
        habit_start_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
        is_active=True,
        created_at=datetime.now(timezone.utc),
    )


def test_habit_is_due_on_start_date(base_habit):
    assert base_habit.is_due_today(date(2024, 1, 1)) is True


def test_habit_is_due_after_start_date(base_habit):
    assert base_habit.is_due_today(date(2024, 6, 15)) is True


def test_habit_is_not_due_before_start_date(base_habit):
    assert base_habit.is_due_today(date(2023, 12, 31)) is False


def test_inactive_habit_is_not_due(base_habit):
    base_habit.is_active = False
    assert base_habit.is_due_today(date(2024, 6, 15)) is False


def test_habit_is_not_due_after_end_date(base_habit):
    base_habit.habit_end_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
    assert base_habit.is_due_today(date(2024, 3, 2)) is False


def test_habit_is_due_on_end_date(base_habit):
    base_habit.habit_end_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
    assert base_habit.is_due_today(date(2024, 3, 1)) is True
