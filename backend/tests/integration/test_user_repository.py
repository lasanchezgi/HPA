"""Integration tests for PostgresUserRepository."""
from datetime import datetime, timezone
from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError

from src.domain.entities.user import User
from src.infrastructure.database.repositories.postgres_user_repository import (
    PostgresUserRepository,
)


def _make_user(**overrides) -> User:
    now = datetime.now(timezone.utc)
    defaults = dict(
        id=uuid4(),
        username=f"user_{uuid4().hex[:8]}",
        email=f"{uuid4().hex[:8]}@test.com",
        hashed_password="hashed_pw",
        is_active=True,
        created_at=now,
        updated_at=now,
    )
    defaults.update(overrides)
    return User(**defaults)


@pytest.mark.asyncio
async def test_save_user_and_find_by_id(test_session):
    repo = PostgresUserRepository(test_session)
    user = _make_user(email="alice@test.com", username="alice")
    saved = await repo.save(user)
    found = await repo.find_by_id(saved.id)

    assert found is not None
    assert found.email == "alice@test.com"
    assert found.hashed_password == "hashed_pw"


@pytest.mark.asyncio
async def test_find_by_email_returns_user(test_session):
    repo = PostgresUserRepository(test_session)
    user = _make_user()
    await repo.save(user)

    found = await repo.find_by_email(user.email)
    assert found is not None
    assert found.id == user.id


@pytest.mark.asyncio
async def test_find_by_email_returns_none_if_not_exists(test_session):
    repo = PostgresUserRepository(test_session)
    result = await repo.find_by_email("ghost@nowhere.com")
    assert result is None


@pytest.mark.asyncio
async def test_duplicate_email_raises_integrity_error(test_session):
    repo = PostgresUserRepository(test_session)
    email = f"{uuid4().hex[:8]}@test.com"
    user1 = _make_user(email=email, username=f"u_{uuid4().hex[:8]}")
    user2 = _make_user(email=email, username=f"u_{uuid4().hex[:8]}")

    await repo.save(user1)
    with pytest.raises(IntegrityError):
        await repo.save(user2)
    await test_session.rollback()
