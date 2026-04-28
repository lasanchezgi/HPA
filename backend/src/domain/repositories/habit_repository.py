from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.habit import Habit


class HabitRepository(ABC):
    @abstractmethod
    async def save(self, habit: Habit) -> Habit: ...

    @abstractmethod
    async def find_by_id(self, habit_id: UUID) -> Habit | None: ...

    @abstractmethod
    async def find_all_by_user_id(self, user_id: UUID) -> list[Habit]: ...

    @abstractmethod
    async def find_active_by_user_id(self, user_id: UUID) -> list[Habit]: ...

    @abstractmethod
    async def update(self, habit: Habit) -> Habit: ...

    @abstractmethod
    async def soft_delete(self, habit_id: UUID) -> None: ...
