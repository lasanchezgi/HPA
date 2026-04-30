"""Integration tests for PostgresHabitRepository.

These tests require a running PostgreSQL instance. See tests/integration/conftest.py.
Run with: make test-integration or set TEST_DATABASE_URL in the environment.
"""
from datetime import datetime, timezone
from uuid import uuid4

import pytest

from src.domain.entities.habit import Habit
from src.infrastructure.database.repositories.postgres_habit_repository import (
    PostgresHabitRepository,
)
from src.infrastructure.database.models.user_model import UserModel


async def _create_user(session) -> UserModel:
    user = UserModel(
        id=uuid4(),
        username=f"user_{uuid4().hex[:8]}",
        email=f"{uuid4().hex[:8]}@test.com",
        hashed_password="hashed",
    )
    session.add(user)
    await session.flush()
    return user


@pytest.mark.asyncio
async def test_save_and_find_by_id(test_session):
    user = await _create_user(test_session)
    repo = PostgresHabitRepository(test_session)
    habit = Habit(
        id=uuid4(),
        user_id=user.id,
        habit_name="Integration Test Habit",
        frequency_id=uuid4(),
        category_id=uuid4(),
        habit_start_date=datetime.now(timezone.utc),
        is_active=True,
        created_at=datetime.now(timezone.utc),
    )
    saved = await repo.save(habit)
    found = await repo.find_by_id(saved.id)

    assert found is not None
    assert found.habit_name == "Integration Test Habit"
    assert found.is_active is True


@pytest.mark.asyncio
async def test_find_all_by_user_id_returns_only_user_habits(test_session):
    user_a = await _create_user(test_session)
    user_b = await _create_user(test_session)
    repo = PostgresHabitRepository(test_session)

    habit_a = Habit(
        id=uuid4(),
        user_id=user_a.id,
        habit_name="User A Habit",
        frequency_id=uuid4(),
        category_id=uuid4(),
        habit_start_date=datetime.now(timezone.utc),
        is_active=True,
        created_at=datetime.now(timezone.utc),
    )
    habit_b = Habit(
        id=uuid4(),
        user_id=user_b.id,
        habit_name="User B Habit",
        frequency_id=uuid4(),
        category_id=uuid4(),
        habit_start_date=datetime.now(timezone.utc),
        is_active=True,
        created_at=datetime.now(timezone.utc),
    )
    await repo.save(habit_a)
    await repo.save(habit_b)

    results = await repo.find_all_by_user_id(user_a.id)
    assert all(h.user_id == user_a.id for h in results)
    assert any(h.habit_name == "User A Habit" for h in results)
    assert not any(h.habit_name == "User B Habit" for h in results)
