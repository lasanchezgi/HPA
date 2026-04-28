from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.habit import Habit
from src.domain.repositories.habit_repository import HabitRepository
from src.infrastructure.database.models.habit_model import HabitModel


class PostgresHabitRepository(HabitRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, habit: Habit) -> Habit:
        model = _to_model(habit)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return _to_entity(model)

    async def find_by_id(self, habit_id: UUID) -> Habit | None:
        result = await self._session.get(HabitModel, habit_id)
        return _to_entity(result) if result else None

    async def find_all_by_user_id(self, user_id: UUID) -> list[Habit]:
        stmt = select(HabitModel).where(HabitModel.user_id == user_id)
        result = await self._session.execute(stmt)
        return [_to_entity(m) for m in result.scalars().all()]

    async def find_active_by_user_id(self, user_id: UUID) -> list[Habit]:
        stmt = select(HabitModel).where(
            HabitModel.user_id == user_id,
            HabitModel.is_active.is_(True),
        )
        result = await self._session.execute(stmt)
        return [_to_entity(m) for m in result.scalars().all()]

    async def update(self, habit: Habit) -> Habit:
        model = await self._session.get(HabitModel, habit.id)
        if model:
            model.habit_name = habit.habit_name
            model.habit_description = habit.habit_description
            model.frequency_id = habit.frequency_id
            model.category_id = habit.category_id
            model.habit_type_id = habit.habit_type_id
            model.goal_target = habit.goal_target
            model.habit_start_date = habit.habit_start_date
            model.habit_end_date = habit.habit_end_date
            model.is_active = habit.is_active
            await self._session.flush()
            await self._session.refresh(model)
        return _to_entity(model)  # type: ignore[arg-type]

    async def soft_delete(self, habit_id: UUID) -> None:
        model = await self._session.get(HabitModel, habit_id)
        if model:
            model.is_active = False
            await self._session.flush()


def _to_model(habit: Habit) -> HabitModel:
    return HabitModel(
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


def _to_entity(model: HabitModel) -> Habit:
    return Habit(
        id=model.id,
        user_id=model.user_id,
        habit_name=model.habit_name,
        habit_description=model.habit_description,
        frequency_id=model.frequency_id,
        category_id=model.category_id,
        habit_type_id=model.habit_type_id,
        goal_target=model.goal_target,
        habit_start_date=model.habit_start_date,
        habit_end_date=model.habit_end_date,
        is_active=model.is_active,
        created_at=model.created_at,
    )
