from dataclasses import dataclass


@dataclass(frozen=True)
class ConsistencyScore:
    completed_days: int
    total_days_since_start: int

    def __post_init__(self) -> None:
        if self.total_days_since_start < 0 or self.completed_days < 0:
            raise ValueError("Days must be non-negative.")
        if self.completed_days > self.total_days_since_start:
            raise ValueError("completed_days cannot exceed total_days_since_start.")

    @property
    def value(self) -> float:
        if self.total_days_since_start == 0:
            return 0.0
        return round(self.completed_days / self.total_days_since_start * 100, 2)

    def label(self) -> str:
        score = self.value
        if score >= 90:
            return "Master"
        if score >= 70:
            return "Consistent"
        if score >= 40:
            return "Building"
        return "Beginner"
