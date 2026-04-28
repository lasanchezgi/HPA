from datetime import datetime, timezone
from uuid import UUID, uuid4

from src.application.dtos.habit_dtos import LogCompletionDTO, LogCompletionResultDTO
from src.domain.entities.habit_log import CompletionStatus, HabitLog
from src.domain.entities.streak import Streak
from src.domain.exceptions import HabitNotFoundError
from src.domain.repositories.habit_log_repository import HabitLogRepository
from src.domain.repositories.habit_repository import HabitRepository


class LogCompletionUseCase:
    def __init__(
        self,
        habit_repository: HabitRepository,
        habit_log_repository: HabitLogRepository,
    ) -> None:
        self._habits = habit_repository
        self._logs = habit_log_repository

    async def execute(self, dto: LogCompletionDTO) -> LogCompletionResultDTO:
        habit = await self._habits.find_by_id(dto.habit_id)
        if not habit or habit.user_id != dto.user_id:
            raise HabitNotFoundError(str(dto.habit_id))

        now = datetime.now(timezone.utc)
        log = HabitLog(
            id=uuid4(),
            habit_id=dto.habit_id,
            user_id=dto.user_id,
            status=dto.status,
            notes=dto.notes,
            completion_value=dto.completion_value,
            logged_at=now,
        )
        saved_log = await self._logs.save(log)

        streak = await self._build_streak(dto.habit_id)
        if dto.status == CompletionStatus.DONE:
            streak = streak.update_after_completion(now.date())

        return LogCompletionResultDTO(
            log_id=saved_log.id,
            habit_id=dto.habit_id,
            status=dto.status,
            current_streak=streak.current_streak,
            best_streak=streak.best_streak,
        )

    async def _build_streak(self, habit_id: UUID) -> Streak:
        logs = await self._logs.find_by_habit_id(habit_id)
        done_dates = sorted(
            {l.logged_at.date() for l in logs if l.status == CompletionStatus.DONE}
        )

        current = 0
        best = 0
        last_date = None

        from datetime import timedelta

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
