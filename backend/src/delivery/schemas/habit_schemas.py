from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel, Field

from src.domain.entities.habit_log import CompletionStatus


class CreateHabitRequest(BaseModel):
    habit_name: str = Field(min_length=1, max_length=200)
    habit_description: str | None = None
    frequency_code: str = Field(min_length=1, max_length=50)
    category_code: str = Field(min_length=1, max_length=50)
    habit_type_id: UUID | None = None
    goal_target: float | None = None
    habit_start_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    habit_end_date: datetime | None = None


class HabitResponse(BaseModel):
    id: UUID
    user_id: UUID
    habit_name: str
    habit_description: str | None
    frequency_id: UUID
    category_id: UUID
    habit_type_id: UUID | None
    goal_target: float | None
    habit_start_date: datetime
    habit_end_date: datetime | None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class LogCompletionRequest(BaseModel):
    status: CompletionStatus
    notes: str | None = None
    completion_value: float | None = None


class LogCompletionResponse(BaseModel):
    log_id: UUID
    habit_id: UUID
    status: CompletionStatus
    current_streak: int
    best_streak: int
    logged_at: datetime
