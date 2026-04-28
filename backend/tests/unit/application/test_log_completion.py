from datetime import datetime, timezone
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from backend.src.application.dtos.habit_dtos import LogCompletionDTO
from backend.src.application.use_cases.habits.log_completion import LogCompletionUseCase
from backend.src.domain.entities.habit import Habit
from backend.src.domain.entities.habit_log import CompletionStatus, HabitLog
from backend.src.domain.exceptions import HabitNotFoundError
from backend.src.domain.repositories.habit_log_repository import HabitLogRepository
from backend.src.domain.repositories.habit_repository import HabitRepository


@pytest.fixture
def user_id():
    return uuid4()


@pytest.fixture
def habit(user_id):
    return Habit(
        id=uuid4(),
        user_id=user_id,
        habit_name="Meditate",
        frequency_id=uuid4(),
        category_id=uuid4(),
        habit_start_date=datetime.now(timezone.utc),
        is_active=True,
        created_at=datetime.now(timezone.utc),
    )


@pytest.mark.asyncio
async def test_log_completion_returns_result_dto(habit, user_id):
    habit_repo = AsyncMock(spec=HabitRepository)
    log_repo = AsyncMock(spec=HabitLogRepository)

    habit_repo.find_by_id.return_value = habit
    log_repo.find_by_habit_id.return_value = []

    saved_log = HabitLog(
        id=uuid4(),
        habit_id=habit.id,
        user_id=user_id,
        status=CompletionStatus.DONE,
        logged_at=datetime.now(timezone.utc),
    )
    log_repo.save.return_value = saved_log

    use_case = LogCompletionUseCase(habit_repo, log_repo)
    dto = LogCompletionDTO(habit_id=habit.id, user_id=user_id, status=CompletionStatus.DONE)
    result = await use_case.execute(dto)

    assert result.current_streak == 1
    assert result.best_streak == 1
    assert result.status == CompletionStatus.DONE


@pytest.mark.asyncio
async def test_log_completion_raises_when_habit_not_found(user_id):
    habit_repo = AsyncMock(spec=HabitRepository)
    log_repo = AsyncMock(spec=HabitLogRepository)
    habit_repo.find_by_id.return_value = None

    use_case = LogCompletionUseCase(habit_repo, log_repo)
    dto = LogCompletionDTO(habit_id=uuid4(), user_id=user_id, status=CompletionStatus.DONE)

    with pytest.raises(HabitNotFoundError):
        await use_case.execute(dto)
