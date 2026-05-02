from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID


class CompletionStatus(StrEnum):
    NOT_DONE = "not_done"
    PARTIAL = "partial"
    DONE = "done"


@dataclass
class HabitLog:
    id: UUID
    habit_id: UUID
    user_id: UUID
    status: CompletionStatus
    logged_at: datetime
    notes: str | None = None
    completion_value: float | None = None
