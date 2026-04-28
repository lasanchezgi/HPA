class HabitPowerException(Exception):
    """Base exception for all habit-power-app errors."""


class DomainException(HabitPowerException):
    """Raised when a domain rule is violated."""


class ApplicationException(HabitPowerException):
    """Raised when an application use case fails."""


class HabitNotFoundError(DomainException):
    def __init__(self, habit_id: str) -> None:
        super().__init__(f"Habit '{habit_id}' not found.")
        self.habit_id = habit_id


class UserNotFoundError(DomainException):
    def __init__(self, user_id: str) -> None:
        super().__init__(f"User '{user_id}' not found.")
        self.user_id = user_id


class UserAlreadyExistsError(DomainException):
    def __init__(self, email: str) -> None:
        super().__init__(f"User with email '{email}' already exists.")
        self.email = email


class InvalidCredentialsError(DomainException):
    def __init__(self) -> None:
        super().__init__("Invalid credentials provided.")


class DuplicateHabitError(DomainException):
    def __init__(self, habit_name: str) -> None:
        super().__init__(f"Active habit '{habit_name}' already exists for this user.")
        self.habit_name = habit_name


class StreakCalculationError(DomainException):
    def __init__(self, reason: str) -> None:
        super().__init__(f"Streak calculation failed: {reason}")


class InvalidEmailError(DomainException):
    def __init__(self, email: str) -> None:
        super().__init__(f"Invalid email format: '{email}'")
        self.email = email
