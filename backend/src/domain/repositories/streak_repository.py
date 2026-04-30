from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.streak import Streak


class StreakRepository(ABC):
    @abstractmethod
    async def find_by_habit_id(self, habit_id: UUID) -> Streak | None: ...

    @abstractmethod
    async def find_by_habit_ids(self, habit_ids: list[UUID]) -> dict[UUID, Streak]:
        """Returns {habit_id: Streak} for all given ids. Habits without a streak are absent."""
        ...

    @abstractmethod
    async def save_or_update(self, streak: Streak) -> Streak:
        """Upsert: creates if not exists, updates if exists."""
        ...
