from datetime import date, datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.habit_log import CompletionStatus, HabitLog
from src.domain.repositories.habit_log_repository import HabitLogRepository
from src.infrastructure.database.models.habit_log_model import (
    CompletionStatusEnum,
    HabitLogModel,
)


class PostgresHabitLogRepository(HabitLogRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, log: HabitLog) -> HabitLog:
        model = _to_model(log)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return _to_entity(model)

    async def find_by_id(self, log_id: UUID) -> HabitLog | None:
        result = await self._session.get(HabitLogModel, log_id)
        return _to_entity(result) if result else None

    async def find_by_habit_id(self, habit_id: UUID) -> list[HabitLog]:
        stmt = select(HabitLogModel).where(HabitLogModel.habit_id == habit_id)
        result = await self._session.execute(stmt)
        return [_to_entity(m) for m in result.scalars().all()]

    async def find_by_habit_and_date(
        self, habit_id: UUID, log_date: date
    ) -> HabitLog | None:
        stmt = select(HabitLogModel).where(
            HabitLogModel.habit_id == habit_id,
            func.date(HabitLogModel.logged_at) == log_date,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def count_completed_since(self, habit_id: UUID, since: date) -> int:
        stmt = select(func.count(HabitLogModel.id)).where(
            HabitLogModel.habit_id == habit_id,
            HabitLogModel.status == CompletionStatusEnum.DONE,
            func.date(HabitLogModel.logged_at) >= since,
        )
        result = await self._session.execute(stmt)
        return result.scalar_one()

    async def find_last_log_by_habit_ids(
        self, habit_ids: list[UUID]
    ) -> dict[UUID, datetime | None]:
        if not habit_ids:
            return {}
        stmt = (
            select(
                HabitLogModel.habit_id,
                func.max(HabitLogModel.logged_at).label("last_logged"),
            )
            .where(
                HabitLogModel.habit_id.in_(habit_ids),
                HabitLogModel.status == CompletionStatusEnum.DONE,
            )
            .group_by(HabitLogModel.habit_id)
        )
        result = await self._session.execute(stmt)
        return {row.habit_id: row.last_logged for row in result}


def _to_model(log: HabitLog) -> HabitLogModel:
    return HabitLogModel(
        id=log.id,
        habit_id=log.habit_id,
        user_id=log.user_id,
        status=CompletionStatusEnum(log.status.value),
        notes=log.notes,
        completion_value=log.completion_value,
        logged_at=log.logged_at,
    )


def _to_entity(model: HabitLogModel) -> HabitLog:
    return HabitLog(
        id=model.id,
        habit_id=model.habit_id,
        user_id=model.user_id,
        status=CompletionStatus(model.status.value),
        notes=model.notes,
        completion_value=model.completion_value,
        logged_at=model.logged_at,
    )
