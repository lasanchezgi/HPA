from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.application.dtos.habit_dtos import CreateHabitDTO
from src.domain.entities.user import User
from src.domain.repositories.habit_repository import HabitRepository


@pytest.fixture
def mock_habit_repository() -> AsyncMock:
    mock = AsyncMock(spec=HabitRepository)
    mock.find_active_by_user_id.return_value = []
    return mock


@pytest.fixture
def sample_user() -> User:
    now = datetime.now(UTC)
    return User(
        id=uuid4(),
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_pw",
        is_active=True,
        created_at=now,
        updated_at=now,
    )


@pytest.fixture
def sample_habit_dto() -> CreateHabitDTO:
    return CreateHabitDTO(
        user_id=uuid4(),
        habit_name="Morning Run",
        frequency_id=uuid4(),
        category_id=uuid4(),
        habit_start_date=datetime.now(UTC),
    )
