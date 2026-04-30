from datetime import datetime, timezone
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.application.dtos.habit_dtos import LogCompletionDTO
from src.application.use_cases.habits.log_completion import LogCompletionUseCase
from src.domain.entities.habit import Habit
from src.domain.entities.habit_log import CompletionStatus, HabitLog
from src.domain.exceptions import DuplicateLogError, HabitNotFoundError
from src.domain.repositories.habit_log_repository import HabitLogRepository
from src.domain.repositories.habit_repository import HabitRepository


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
async def test_log_completion_creates_log_and_updates_streak(habit, user_id):
    habit_repo = AsyncMock(spec=HabitRepository)
    log_repo = AsyncMock(spec=HabitLogRepository)

    habit_repo.find_by_id.return_value = habit
    log_repo.find_by_habit_and_date.return_value = None
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
    assert result.logged_at is not None
    log_repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_duplicate_log_same_day_raises_error(habit, user_id):
    habit_repo = AsyncMock(spec=HabitRepository)
    log_repo = AsyncMock(spec=HabitLogRepository)

    habit_repo.find_by_id.return_value = habit
    existing_log = HabitLog(
        id=uuid4(),
        habit_id=habit.id,
        user_id=user_id,
        status=CompletionStatus.DONE,
        logged_at=datetime.now(timezone.utc),
    )
    log_repo.find_by_habit_and_date.return_value = existing_log

    use_case = LogCompletionUseCase(habit_repo, log_repo)
    dto = LogCompletionDTO(habit_id=habit.id, user_id=user_id, status=CompletionStatus.DONE)

    with pytest.raises(DuplicateLogError):
        await use_case.execute(dto)

    log_repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_log_completion_raises_when_habit_not_found(user_id):
    habit_repo = AsyncMock(spec=HabitRepository)
    log_repo = AsyncMock(spec=HabitLogRepository)
    habit_repo.find_by_id.return_value = None

    use_case = LogCompletionUseCase(habit_repo, log_repo)
    dto = LogCompletionDTO(habit_id=uuid4(), user_id=user_id, status=CompletionStatus.DONE)

    with pytest.raises(HabitNotFoundError):
        await use_case.execute(dto)
