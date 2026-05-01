from src.application.dtos.habit_dtos import UpdateHabitDTO
from src.domain.entities.habit import Habit
from src.domain.exceptions import HabitNotFoundError
from src.domain.repositories.habit_repository import HabitRepository


class UpdateHabitUseCase:
    def __init__(self, habit_repo: HabitRepository) -> None:
        self._habit_repo = habit_repo

    async def execute(self, dto: UpdateHabitDTO) -> Habit:
        habit = await self._habit_repo.find_by_id(dto.habit_id)
        if not habit or habit.user_id != dto.user_id:
            raise HabitNotFoundError(dto.habit_id)

        updated = Habit(
            id=habit.id,
            user_id=habit.user_id,
            habit_name=dto.habit_name if dto.habit_name is not None else habit.habit_name,
            habit_description=dto.habit_description if dto.habit_description is not None else habit.habit_description,
            frequency_id=dto.frequency_id if dto.frequency_id is not None else habit.frequency_id,
            category_id=dto.category_id if dto.category_id is not None else habit.category_id,
            habit_type_id=habit.habit_type_id,
            goal_target=dto.goal_target if dto.goal_target is not None else habit.goal_target,
            habit_start_date=habit.habit_start_date,
            habit_end_date=dto.habit_end_date if dto.habit_end_date is not None else habit.habit_end_date,
            is_active=habit.is_active,
            created_at=habit.created_at,
        )
        return await self._habit_repo.update(updated)
