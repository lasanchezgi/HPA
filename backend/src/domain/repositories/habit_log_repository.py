from abc import ABC, abstractmethod
from datetime import date
from uuid import UUID

from src.domain.entities.habit_log import HabitLog


class HabitLogRepository(ABC):
    @abstractmethod
    async def save(self, log: HabitLog) -> HabitLog: ...

    @abstractmethod
    async def find_by_id(self, log_id: UUID) -> HabitLog | None: ...

    @abstractmethod
    async def find_by_habit_id(self, habit_id: UUID) -> list[HabitLog]: ...

    @abstractmethod
    async def find_by_habit_and_date(
        self, habit_id: UUID, log_date: date
    ) -> HabitLog | None: ...

    @abstractmethod
    async def count_completed_since(self, habit_id: UUID, since: date) -> int: ...
