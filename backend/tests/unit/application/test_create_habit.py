from datetime import datetime, timezone
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from backend.src.application.dtos.habit_dtos import CreateHabitDTO, HabitDTO
from backend.src.application.use_cases.habits.create_habit import CreateHabitUseCase
from backend.src.domain.entities.habit import Habit
from backend.src.domain.exceptions import DuplicateHabitError


@pytest.fixture
def create_habit_dto():
    return CreateHabitDTO(
        user_id=uuid4(),
        habit_name="Morning Run",
        frequency_id=uuid4(),
        category_id=uuid4(),
        habit_start_date=datetime.now(timezone.utc),
    )


@pytest.mark.asyncio
async def test_create_habit_saves_and_returns_dto(mock_habit_repository, create_habit_dto):
    now = datetime.now(timezone.utc)
    saved_habit = Habit(
        id=uuid4(),
        user_id=create_habit_dto.user_id,
        habit_name=create_habit_dto.habit_name,
        frequency_id=create_habit_dto.frequency_id,
        category_id=create_habit_dto.category_id,
        habit_start_date=create_habit_dto.habit_start_date,
        is_active=True,
        created_at=now,
    )
    mock_habit_repository.find_active_by_user_id.return_value = []
    mock_habit_repository.save.return_value = saved_habit

    use_case = CreateHabitUseCase(mock_habit_repository)
    result = await use_case.execute(create_habit_dto)

    assert isinstance(result, HabitDTO)
    assert result.habit_name == "Morning Run"
    assert result.is_active is True
    mock_habit_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_create_habit_raises_if_duplicate_name(mock_habit_repository, create_habit_dto):
    existing = Habit(
        id=uuid4(),
        user_id=create_habit_dto.user_id,
        habit_name="Morning Run",
        frequency_id=uuid4(),
        category_id=uuid4(),
        habit_start_date=datetime.now(timezone.utc),
        is_active=True,
        created_at=datetime.now(timezone.utc),
    )
    mock_habit_repository.find_active_by_user_id.return_value = [existing]

    use_case = CreateHabitUseCase(mock_habit_repository)

    with pytest.raises(DuplicateHabitError):
        await use_case.execute(create_habit_dto)

    mock_habit_repository.save.assert_not_called()
