from uuid import UUID

from src.domain.exceptions import HabitNotFoundError
from src.domain.repositories.habit_repository import HabitRepository


class ArchiveHabitUseCase:
    def __init__(self, habit_repo: HabitRepository) -> None:
        self._habits = habit_repo

    async def execute(self, habit_id: UUID, user_id: UUID) -> None:
        habit = await self._habits.find_by_id(habit_id)
        if not habit or habit.user_id != user_id:
            raise HabitNotFoundError(str(habit_id))
        await self._habits.soft_delete(habit_id)
