from datetime import datetime, timezone
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.application.use_cases.dashboard.get_dashboard_summary import (
    GetDashboardSummaryUseCase,
)
from src.domain.entities.habit import Habit
from src.domain.entities.streak import Streak
from src.domain.repositories.habit_log_repository import HabitLogRepository
from src.domain.repositories.habit_repository import HabitRepository
from src.domain.repositories.streak_repository import StreakRepository


def _make_use_case(habit_repo, log_repo, streak_repo):
    return GetDashboardSummaryUseCase(habit_repo, log_repo, streak_repo)


def _make_habit(user_id, name="Test Habit"):
    return Habit(
        id=uuid4(),
        user_id=user_id,
        habit_name=name,
        frequency_id=uuid4(),
        category_id=uuid4(),
        habit_start_date=datetime.now(timezone.utc),
        is_active=True,
        created_at=datetime.now(timezone.utc),
    )


@pytest.mark.asyncio
async def test_dashboard_no_habits_returns_empty_summary():
    user_id = uuid4()
    habit_repo = AsyncMock(spec=HabitRepository)
    log_repo = AsyncMock(spec=HabitLogRepository)
    streak_repo = AsyncMock(spec=StreakRepository)

    habit_repo.find_active_by_user_id.return_value = []

    use_case = _make_use_case(habit_repo, log_repo, streak_repo)
    result = await use_case.execute(user_id)

    assert result.total_habits == 0
    assert result.active_streaks == 0
    assert result.best_streak_overall == 0
    assert result.habits_summary == []
    streak_repo.find_by_habit_ids.assert_not_called()


@pytest.mark.asyncio
async def test_dashboard_with_habits_and_streak():
    user_id = uuid4()
    habit_repo = AsyncMock(spec=HabitRepository)
    log_repo = AsyncMock(spec=HabitLogRepository)
    streak_repo = AsyncMock(spec=StreakRepository)

    habit = _make_habit(user_id, "Morning Run")
    habit_repo.find_active_by_user_id.return_value = [habit]

    streak = Streak(
        habit_id=habit.id,
        current_streak=5,
        best_streak=10,
        last_completed_date=datetime.now(timezone.utc).date(),
    )
    streak_repo.find_by_habit_ids.return_value = {habit.id: streak}
    log_repo.find_last_log_by_habit_ids.return_value = {habit.id: datetime.now(timezone.utc)}

    use_case = _make_use_case(habit_repo, log_repo, streak_repo)
    result = await use_case.execute(user_id)

    assert result.total_habits == 1
    assert result.active_streaks == 1
    assert result.best_streak_overall == 10
    assert len(result.habits_summary) == 1
    assert result.habits_summary[0].habit_name == "Morning Run"
    assert result.habits_summary[0].current_streak == 5


@pytest.mark.asyncio
async def test_dashboard_habit_without_streak_shows_zero():
    user_id = uuid4()
    habit_repo = AsyncMock(spec=HabitRepository)
    log_repo = AsyncMock(spec=HabitLogRepository)
    streak_repo = AsyncMock(spec=StreakRepository)

    habit = _make_habit(user_id, "No Streak Habit")
    habit_repo.find_active_by_user_id.return_value = [habit]

    # No streak for this habit
    streak_repo.find_by_habit_ids.return_value = {}
    log_repo.find_last_log_by_habit_ids.return_value = {}

    use_case = _make_use_case(habit_repo, log_repo, streak_repo)
    result = await use_case.execute(user_id)

    assert result.total_habits == 1
    assert result.active_streaks == 0
    assert result.best_streak_overall == 0
    assert result.habits_summary[0].current_streak == 0
    assert result.habits_summary[0].last_logged is None


@pytest.mark.asyncio
async def test_dashboard_multiple_habits_aggregates_correctly():
    user_id = uuid4()
    habit_repo = AsyncMock(spec=HabitRepository)
    log_repo = AsyncMock(spec=HabitLogRepository)
    streak_repo = AsyncMock(spec=StreakRepository)

    habit_a = _make_habit(user_id, "Habit A")
    habit_b = _make_habit(user_id, "Habit B")
    habit_repo.find_active_by_user_id.return_value = [habit_a, habit_b]

    streak_a = Streak(habit_id=habit_a.id, current_streak=3, best_streak=7, last_completed_date=None)
    streak_b = Streak(habit_id=habit_b.id, current_streak=0, best_streak=15, last_completed_date=None)
    streak_repo.find_by_habit_ids.return_value = {habit_a.id: streak_a, habit_b.id: streak_b}
    log_repo.find_last_log_by_habit_ids.return_value = {}

    use_case = _make_use_case(habit_repo, log_repo, streak_repo)
    result = await use_case.execute(user_id)

    assert result.total_habits == 2
    assert result.active_streaks == 1  # only habit_a has current_streak > 0
    assert result.best_streak_overall == 15  # max of 7 and 15
