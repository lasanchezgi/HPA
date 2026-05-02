"""Integration tests for PostgresHabitLogRepository."""
from datetime import UTC, date, datetime
from uuid import uuid4

import pytest

from src.domain.entities.habit_log import CompletionStatus, HabitLog
from src.infrastructure.database.models.habit_model import HabitModel
from src.infrastructure.database.models.user_model import UserModel
from src.infrastructure.database.repositories.postgres_habit_log_repository import (
    PostgresHabitLogRepository,
)


async def _seed_user_and_habit(session):
    user = UserModel(
        id=uuid4(),
        username=f"u_{uuid4().hex[:8]}",
        email=f"{uuid4().hex[:8]}@test.com",
        hashed_password="pw",
    )
    session.add(user)
    await session.flush()

    now = datetime.now(UTC)
    habit = HabitModel(
        id=uuid4(),
        user_id=user.id,
        habit_name="Test Habit",
        frequency_id=uuid4(),
        category_id=uuid4(),
        habit_start_date=now,
        is_active=True,
    )
    session.add(habit)
    await session.flush()
    return user, habit


def _make_log(habit_id, user_id, logged_at=None) -> HabitLog:
    return HabitLog(
        id=uuid4(),
        habit_id=habit_id,
        user_id=user_id,
        status=CompletionStatus.DONE,
        logged_at=logged_at or datetime.now(UTC),
    )


@pytest.mark.asyncio
async def test_save_log_and_find_by_habit_id(test_session):
    user, habit = await _seed_user_and_habit(test_session)
    repo = PostgresHabitLogRepository(test_session)

    log = _make_log(habit.id, user.id)
    await repo.save(log)

    results = await repo.find_by_habit_id(habit.id)
    assert len(results) == 1
    assert results[0].status == CompletionStatus.DONE


@pytest.mark.asyncio
async def test_find_by_habit_and_date_returns_log_if_exists(test_session):
    user, habit = await _seed_user_and_habit(test_session)
    repo = PostgresHabitLogRepository(test_session)

    today = datetime.now(UTC)
    log = _make_log(habit.id, user.id, logged_at=today)
    await repo.save(log)

    found = await repo.find_by_habit_and_date(habit.id, today.date())
    assert found is not None
    assert found.habit_id == habit.id


@pytest.mark.asyncio
async def test_find_by_habit_and_date_returns_none_if_not_exists(test_session):
    user, habit = await _seed_user_and_habit(test_session)
    repo = PostgresHabitLogRepository(test_session)

    result = await repo.find_by_habit_and_date(habit.id, date(2000, 1, 1))
    assert result is None


@pytest.mark.asyncio
async def test_duplicate_log_same_day_returns_existing(test_session):
    user, habit = await _seed_user_and_habit(test_session)
    repo = PostgresHabitLogRepository(test_session)

    today = datetime.now(UTC)
    log = _make_log(habit.id, user.id, logged_at=today)
    await repo.save(log)

    found = await repo.find_by_habit_and_date(habit.id, today.date())
    assert found is not None
    assert found.id == log.id
