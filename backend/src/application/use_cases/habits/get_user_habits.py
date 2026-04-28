from uuid import UUID

from src.application.dtos.habit_dtos import HabitDTO
from src.domain.entities.habit import Habit
from src.domain.repositories.habit_repository import HabitRepository


class GetUserHabitsUseCase:
    def __init__(self, habit_repository: HabitRepository) -> None:
        self._repo = habit_repository

    async def execute(self, user_id: UUID, active_only: bool = False) -> list[HabitDTO]:
        if active_only:
            habits = await self._repo.find_active_by_user_id(user_id)
        else:
            habits = await self._repo.find_all_by_user_id(user_id)
        return [_to_dto(h) for h in habits]


def _to_dto(habit: Habit) -> HabitDTO:
    return HabitDTO(
        id=habit.id,
        user_id=habit.user_id,
        habit_name=habit.habit_name,
        habit_description=habit.habit_description,
        frequency_id=habit.frequency_id,
        category_id=habit.category_id,
        habit_type_id=habit.habit_type_id,
        goal_target=habit.goal_target,
        habit_start_date=habit.habit_start_date,
        habit_end_date=habit.habit_end_date,
        is_active=habit.is_active,
        created_at=habit.created_at,
    )
