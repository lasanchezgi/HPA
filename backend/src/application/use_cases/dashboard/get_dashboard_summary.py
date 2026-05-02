from datetime import UTC, datetime
from uuid import UUID

from src.application.dtos.dashboard_dtos import (
    ConsistencyScoreData,
    DashboardSummaryDTO,
    HabitSummaryDTO,
)
from src.domain.entities.streak import Streak
from src.domain.repositories.habit_log_repository import HabitLogRepository
from src.domain.repositories.habit_repository import HabitRepository
from src.domain.repositories.streak_repository import StreakRepository
from src.domain.value_objects.consistency_score import ConsistencyScore


class GetDashboardSummaryUseCase:
    def __init__(
        self,
        habit_repository: HabitRepository,
        habit_log_repository: HabitLogRepository,
        streak_repository: StreakRepository,
    ) -> None:
        self._habits = habit_repository
        self._logs = habit_log_repository
        self._streaks = streak_repository

    async def execute(self, user_id: UUID) -> DashboardSummaryDTO:
        habits = await self._habits.find_active_by_user_id(user_id)
        today = datetime.now(UTC).date()

        if not habits:
            return DashboardSummaryDTO(
                total_habits=0,
                active_streaks=0,
                best_streak_overall=0,
                consistency_score=ConsistencyScoreData(value=0.0, label="Beginner"),
                total_gems=0,
                habits_summary=[],
            )

        habit_ids = [h.id for h in habits]

        # 1 query for all streaks
        streaks_by_habit = await self._streaks.find_by_habit_ids(habit_ids)

        # 1 query for last completed log per habit
        last_logs = await self._logs.find_last_log_by_habit_ids(habit_ids)

        active_streaks = sum(
            1 for s in streaks_by_habit.values() if s.current_streak > 0
        )
        best_streak_overall = max(
            (s.best_streak for s in streaks_by_habit.values()), default=0
        )

        total_completed = sum(s.current_streak for s in streaks_by_habit.values())
        total_days_sum = sum(
            max((today - h.habit_start_date.date()).days + 1, 1) for h in habits
        )

        overall_score = ConsistencyScore(
            completed_days=min(total_completed, total_days_sum),
            total_days_since_start=max(total_days_sum, 1),
        )

        _empty = _empty_streak
        habits_summary = [
            HabitSummaryDTO(
                habit_id=h.id,
                habit_name=h.habit_name,
                current_streak=streaks_by_habit.get(h.id, _empty(h.id)).current_streak,
                last_logged=last_logs.get(h.id),
            )
            for h in habits
        ]

        return DashboardSummaryDTO(
            total_habits=len(habits),
            active_streaks=active_streaks,
            best_streak_overall=best_streak_overall,
            consistency_score=ConsistencyScoreData(
                value=overall_score.value,
                label=overall_score.label(),
            ),
            total_gems=0,
            habits_summary=habits_summary,
        )


def _empty_streak(habit_id: UUID) -> Streak:
    return Streak(
        habit_id=habit_id, current_streak=0, best_streak=0, last_completed_date=None
    )
