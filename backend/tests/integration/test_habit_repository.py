"""Integration tests for PostgresHabitRepository.

These tests require a running PostgreSQL instance. See tests/integration/conftest.py.
Run with: make test-integration or set TEST_DATABASE_URL in the environment.
"""
from datetime import UTC, datetime
from uuid import uuid4

import pytest

from src.domain.entities.habit import Habit
from src.infrastructure.database.models.user_model import UserModel
from src.infrastructure.database.repositories.postgres_habit_repository import (
    PostgresHabitRepository,
)


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
        habit_start_date=datetime.now(UTC),
        is_active=True,
        created_at=datetime.now(UTC),
    )
    saved = await repo.save(habit)
    found = await repo.find_by_id(saved.id)

    assert found is not None
    assert found.habit_name == "Integration Test Habit"
    assert found.is_active is True


@pytest.mark.asyncio
async def test_update_habit_name_persists_change(test_session):
    user = await _create_user(test_session)
    repo = PostgresHabitRepository(test_session)
    habit = Habit(
        id=uuid4(),
        user_id=user.id,
        habit_name="Original Name",
        frequency_id=uuid4(),
        category_id=uuid4(),
        habit_start_date=datetime.now(UTC),
        is_active=True,
        created_at=datetime.now(UTC),
    )
    saved = await repo.save(habit)

    updated = Habit(
        id=saved.id,
        user_id=saved.user_id,
        habit_name="Updated Name",
        frequency_id=saved.frequency_id,
        category_id=saved.category_id,
        habit_start_date=saved.habit_start_date,
        is_active=saved.is_active,
        created_at=saved.created_at,
    )
    await repo.update(updated)
    found = await repo.find_by_id(saved.id)

    assert found is not None
    assert found.habit_name == "Updated Name"


@pytest.mark.asyncio
async def test_soft_delete_sets_is_active_false(test_session):
    user = await _create_user(test_session)
    repo = PostgresHabitRepository(test_session)
    habit = Habit(
        id=uuid4(),
        user_id=user.id,
        habit_name="To Be Deleted",
        frequency_id=uuid4(),
        category_id=uuid4(),
        habit_start_date=datetime.now(UTC),
        is_active=True,
        created_at=datetime.now(UTC),
    )
    saved = await repo.save(habit)
    await repo.soft_delete(saved.id)
    found = await repo.find_by_id(saved.id)

    assert found is not None
    assert found.is_active is False


@pytest.mark.asyncio
async def test_find_active_by_user_id_excludes_soft_deleted(test_session):
    user = await _create_user(test_session)
    repo = PostgresHabitRepository(test_session)

    active_habit = Habit(
        id=uuid4(),
        user_id=user.id,
        habit_name="Active Habit",
        frequency_id=uuid4(),
        category_id=uuid4(),
        habit_start_date=datetime.now(UTC),
        is_active=True,
        created_at=datetime.now(UTC),
    )
    deleted_habit = Habit(
        id=uuid4(),
        user_id=user.id,
        habit_name="Deleted Habit",
        frequency_id=uuid4(),
        category_id=uuid4(),
        habit_start_date=datetime.now(UTC),
        is_active=True,
        created_at=datetime.now(UTC),
    )
    await repo.save(active_habit)
    saved_deleted = await repo.save(deleted_habit)
    await repo.soft_delete(saved_deleted.id)

    active_results = await repo.find_active_by_user_id(user.id)
    names = [h.habit_name for h in active_results]
    assert "Active Habit" in names
    assert "Deleted Habit" not in names


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
        habit_start_date=datetime.now(UTC),
        is_active=True,
        created_at=datetime.now(UTC),
    )
    habit_b = Habit(
        id=uuid4(),
        user_id=user_b.id,
        habit_name="User B Habit",
        frequency_id=uuid4(),
        category_id=uuid4(),
        habit_start_date=datetime.now(UTC),
        is_active=True,
        created_at=datetime.now(UTC),
    )
    await repo.save(habit_a)
    await repo.save(habit_b)

    results = await repo.find_all_by_user_id(user_a.id)
    assert all(h.user_id == user_a.id for h in results)
    assert any(h.habit_name == "User A Habit" for h in results)
    assert not any(h.habit_name == "User B Habit" for h in results)
