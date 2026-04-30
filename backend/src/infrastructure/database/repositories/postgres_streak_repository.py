import uuid
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.streak import Streak
from src.domain.repositories.streak_repository import StreakRepository
from src.infrastructure.database.models.streak_model import StreakModel


class PostgresStreakRepository(StreakRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_habit_id(self, habit_id: UUID) -> Streak | None:
        stmt = select(StreakModel).where(StreakModel.habit_id == habit_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def find_by_habit_ids(self, habit_ids: list[UUID]) -> dict[UUID, Streak]:
        if not habit_ids:
            return {}
        stmt = select(StreakModel).where(StreakModel.habit_id.in_(habit_ids))
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return {model.habit_id: _to_entity(model) for model in models}

    async def save_or_update(self, streak: Streak) -> Streak:
        stmt = (
            pg_insert(StreakModel)
            .values(
                id=streak.id if streak.id else uuid.uuid4(),
                habit_id=streak.habit_id,
                current_streak=streak.current_streak,
                best_streak=streak.best_streak,
                last_completed_date=streak.last_completed_date,
            )
            .on_conflict_do_update(
                index_elements=["habit_id"],
                set_={
                    "current_streak": streak.current_streak,
                    "best_streak": streak.best_streak,
                    "last_completed_date": streak.last_completed_date,
                },
            )
            .returning(StreakModel)
        )
        result = await self._session.execute(stmt)
        await self._session.flush()
        model = result.scalar_one()
        return _to_entity(model)


def _to_entity(model: StreakModel) -> Streak:
    return Streak(
        id=model.id,
        habit_id=model.habit_id,
        current_streak=model.current_streak,
        best_streak=model.best_streak,
        last_completed_date=model.last_completed_date,
    )
