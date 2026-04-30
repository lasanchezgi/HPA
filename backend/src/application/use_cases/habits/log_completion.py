from datetime import datetime, timezone
from uuid import uuid4

from src.application.dtos.habit_dtos import LogCompletionDTO, LogCompletionResultDTO
from src.domain.entities.habit_log import CompletionStatus, HabitLog
from src.domain.entities.streak import Streak
from src.domain.exceptions import DuplicateLogError, HabitNotFoundError
from src.domain.repositories.habit_log_repository import HabitLogRepository
from src.domain.repositories.habit_repository import HabitRepository
from src.domain.repositories.streak_repository import StreakRepository


class LogCompletionUseCase:
    def __init__(
        self,
        habit_repository: HabitRepository,
        habit_log_repository: HabitLogRepository,
        streak_repository: StreakRepository,
    ) -> None:
        self._habits = habit_repository
        self._logs = habit_log_repository
        self._streaks = streak_repository

    async def execute(self, dto: LogCompletionDTO) -> LogCompletionResultDTO:
        habit = await self._habits.find_by_id(dto.habit_id)
        if not habit or habit.user_id != dto.user_id:
            raise HabitNotFoundError(str(dto.habit_id))

        now = datetime.now(timezone.utc)
        existing = await self._logs.find_by_habit_and_date(dto.habit_id, now.date())
        if existing is not None:
            raise DuplicateLogError(str(dto.habit_id))

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

        streak = await self._streaks.find_by_habit_id(dto.habit_id)
        if streak is None:
            streak = Streak(
                habit_id=dto.habit_id,
                current_streak=0,
                best_streak=0,
                last_completed_date=None,
            )

        if dto.status == CompletionStatus.DONE:
            streak = streak.update_after_completion(now.date())

        persisted = await self._streaks.save_or_update(streak)

        return LogCompletionResultDTO(
            log_id=saved_log.id,
            habit_id=dto.habit_id,
            status=dto.status,
            current_streak=persisted.current_streak,
            best_streak=persisted.best_streak,
            logged_at=saved_log.logged_at,
        )
