"""Integration tests for PostgresHabitRepository.

These tests require a running PostgreSQL instance and use a real AsyncSession.
Run with: make test-integration or set TEST_DATABASE_URL in the environment.
"""
import os
from datetime import datetime, timezone
from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.src.domain.entities.habit import Habit
from backend.src.infrastructure.database.models.base import Base
from backend.src.infrastructure.database.models import (  # noqa: F401 — ensure metadata populated
    habit_log_model,
    habit_model,
    user_model,
)
from backend.src.infrastructure.database.repositories.postgres_habit_repository import (
    PostgresHabitRepository,
)

TEST_DB_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://habit_user:habit_pass@localhost:5432/habit_power_test",
)

pytestmark = pytest.mark.skipif(
    not os.getenv("TEST_DATABASE_URL"),
    reason="TEST_DATABASE_URL not set — skipping integration tests",
)


@pytest_asyncio.fixture(scope="module")
async def engine():
    eng = create_async_engine(TEST_DB_URL, echo=False)
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield eng
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await eng.dispose()


@pytest_asyncio.fixture
async def session(engine):
    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with factory() as s:
        yield s
        await s.rollback()


@pytest.mark.asyncio
async def test_save_and_find_habit(session):
    repo = PostgresHabitRepository(session)
    habit = Habit(
        id=uuid4(),
        user_id=uuid4(),
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
