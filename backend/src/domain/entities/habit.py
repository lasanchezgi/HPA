from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID


@dataclass
class Habit:
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

    def is_due_today(self, current_date: date) -> bool:
        """Return True if this habit should be completed on current_date."""
        start = self.habit_start_date.date()
        if current_date < start:
            return False
        if self.habit_end_date and current_date > self.habit_end_date.date():
            return False
        return self.is_active
