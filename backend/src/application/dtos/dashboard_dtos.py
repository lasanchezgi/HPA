from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass
class ConsistencyScoreData:
    value: float
    label: str


@dataclass
class HabitSummaryDTO:
    habit_id: UUID
    habit_name: str
    current_streak: int
    last_logged: datetime | None


@dataclass
class DashboardSummaryDTO:
    total_habits: int
    active_streaks: int
    best_streak_overall: int
    consistency_score: ConsistencyScoreData
    total_gems: int
    habits_summary: list[HabitSummaryDTO] = field(default_factory=list)
