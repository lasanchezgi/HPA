from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class HabitSummaryDTO:
    habit_id: UUID
    habit_name: str
    current_streak: int
    consistency_score: float
    consistency_label: str


@dataclass
class DashboardSummaryDTO:
    total_habits: int
    active_streaks: int
    best_streak_overall: int
    consistency_score: float
    consistency_label: str
    total_gems: int
    habits_summary: list[HabitSummaryDTO] = field(default_factory=list)
