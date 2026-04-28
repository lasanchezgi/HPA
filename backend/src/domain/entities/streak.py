from dataclasses import dataclass
from datetime import date, timedelta
from uuid import UUID


@dataclass
class Streak:
    habit_id: UUID
    current_streak: int
    best_streak: int
    last_completed_date: date | None

    def update_after_completion(self, completion_date: date) -> "Streak":
        """Return a new Streak reflecting the given completion_date."""
        if self.last_completed_date is None:
            new_current = 1
        elif completion_date == self.last_completed_date + timedelta(days=1):
            new_current = self.current_streak + 1
        elif completion_date == self.last_completed_date:
            # Same day — idempotent, no change
            return Streak(
                habit_id=self.habit_id,
                current_streak=self.current_streak,
                best_streak=self.best_streak,
                last_completed_date=self.last_completed_date,
            )
        else:
            # Gap detected — reset streak
            new_current = 1

        new_best = max(self.best_streak, new_current)
        return Streak(
            habit_id=self.habit_id,
            current_streak=new_current,
            best_streak=new_best,
            last_completed_date=completion_date,
        )
