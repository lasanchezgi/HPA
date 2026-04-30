from datetime import date, datetime, timedelta, timezone
from uuid import UUID

from src.application.dtos.dashboard_dtos import (
    ConsistencyScoreData,
    DashboardSummaryDTO,
    HabitSummaryDTO,
)
from src.domain.entities.habit_log import CompletionStatus
from src.domain.entities.streak import Streak
from src.domain.repositories.habit_log_repository import HabitLogRepository
from src.domain.repositories.habit_repository import HabitRepository
from src.domain.value_objects.consistency_score import ConsistencyScore


class GetDashboardSummaryUseCase:
    def __init__(
        self,
        habit_repository: HabitRepository,
        habit_log_repository: HabitLogRepository,
    ) -> None:
        self._habits = habit_repository
        self._logs = habit_log_repository

    async def execute(self, user_id: UUID) -> DashboardSummaryDTO:
        habits = await self._habits.find_active_by_user_id(user_id)
        today = datetime.now(timezone.utc).date()

        habits_summary: list[HabitSummaryDTO] = []
        active_streaks = 0
        best_streak_overall = 0
        total_completed = 0
        total_days_sum = 0

        for habit in habits:
            logs = await self._logs.find_by_habit_id(habit.id)
            done_dates = sorted(
                {l.logged_at.date() for l in logs if l.status == CompletionStatus.DONE}
            )

            streak = _compute_streak(habit.id, done_dates)
            if streak.current_streak > 0:
                active_streaks += 1
            best_streak_overall = max(best_streak_overall, streak.best_streak)

            days_since_start = max((today - habit.habit_start_date.date()).days + 1, 1)
            score_obj = ConsistencyScore(
                completed_days=len(done_dates),
                total_days_since_start=days_since_start,
            )
            total_completed += len(done_dates)
            total_days_sum += days_since_start

            done_logs = [l for l in logs if l.status == CompletionStatus.DONE]
            last_logged: datetime | None = (
                max(done_logs, key=lambda l: l.logged_at).logged_at if done_logs else None
            )

            habits_summary.append(
                HabitSummaryDTO(
                    habit_id=habit.id,
                    habit_name=habit.habit_name,
                    current_streak=streak.current_streak,
                    last_logged=last_logged,
                )
            )

        overall_score = ConsistencyScore(
            completed_days=total_completed,
            total_days_since_start=max(total_days_sum, 1),
        )

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


def _compute_streak(habit_id: UUID, done_dates: list[date]) -> Streak:
    current = 0
    best = 0
    last_date = None

    for d in done_dates:
        if last_date is None or d == last_date + timedelta(days=1):
            current += 1
        else:
            current = 1
        best = max(best, current)
        last_date = d

    return Streak(
        habit_id=habit_id,
        current_streak=current,
        best_streak=best,
        last_completed_date=last_date,
    )
