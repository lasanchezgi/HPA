from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from src.domain.entities.habit_log import CompletionStatus


@dataclass
class CreateHabitDTO:
    user_id: UUID
    habit_name: str
    frequency_id: UUID
    category_id: UUID
    habit_start_date: datetime
    habit_description: str | None = None
    habit_type_id: UUID | None = None
    goal_target: float | None = None
    habit_end_date: datetime | None = None


@dataclass
class HabitDTO:
    id: UUID
    user_id: UUID
    habit_name: str
    frequency_id: UUID
    category_id: UUID
    habit_start_date: datetime
    is_active: bool
    created_at: datetime
    habit_description: str | None = None
    habit_type_id: UUID | None = None
    goal_target: float | None = None
    habit_end_date: datetime | None = None


@dataclass
class LogCompletionDTO:
    habit_id: UUID
    user_id: UUID
    status: CompletionStatus
    notes: str | None = None
    completion_value: float | None = None


@dataclass
class LogCompletionResultDTO:
    log_id: UUID
    habit_id: UUID
    status: CompletionStatus
    current_streak: int
    best_streak: int
