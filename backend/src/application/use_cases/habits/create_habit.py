from datetime import UTC, datetime
from uuid import uuid4

from src.application.dtos.habit_dtos import CreateHabitDTO, HabitDTO
from src.domain.entities.habit import Habit
from src.domain.exceptions import DuplicateHabitError
from src.domain.repositories.habit_repository import HabitRepository


class CreateHabitUseCase:
    def __init__(self, habit_repository: HabitRepository) -> None:
        self._repo = habit_repository

    async def execute(self, dto: CreateHabitDTO) -> HabitDTO:
        existing = await self._repo.find_active_by_user_id(dto.user_id)
        if any(h.habit_name == dto.habit_name for h in existing):
            raise DuplicateHabitError(dto.habit_name)

        now = datetime.now(UTC)
        habit = Habit(
            id=uuid4(),
            user_id=dto.user_id,
            habit_name=dto.habit_name,
            habit_description=dto.habit_description,
            frequency_id=dto.frequency_id,
            category_id=dto.category_id,
            habit_type_id=dto.habit_type_id,
            goal_target=dto.goal_target,
            habit_start_date=dto.habit_start_date,
            habit_end_date=dto.habit_end_date,
            is_active=True,
            created_at=now,
        )
        saved = await self._repo.save(habit)
        return _to_dto(saved)


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
