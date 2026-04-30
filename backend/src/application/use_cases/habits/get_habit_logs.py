from uuid import UUID

from src.application.dtos.habit_dtos import HabitLogDTO
from src.domain.exceptions import HabitNotFoundError
from src.domain.repositories.habit_log_repository import HabitLogRepository
from src.domain.repositories.habit_repository import HabitRepository


class GetHabitLogsUseCase:
    def __init__(
        self,
        habit_repo: HabitRepository,
        log_repo: HabitLogRepository,
    ) -> None:
        self._habits = habit_repo
        self._logs = log_repo

    async def execute(self, habit_id: UUID, user_id: UUID) -> list[HabitLogDTO]:
        habit = await self._habits.find_by_id(habit_id)
        if not habit or habit.user_id != user_id:
            raise HabitNotFoundError(habit_id)
        logs = await self._logs.find_by_habit_id(habit_id)
        return [HabitLogDTO.from_entity(log) for log in logs]
