from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_settings
from src.application.dtos.auth_dtos import UserDTO
from src.application.use_cases.auth.login_user import LoginUserUseCase
from src.application.use_cases.auth.register_user import RegisterUserUseCase
from src.application.use_cases.dashboard.get_dashboard_summary import (
    GetDashboardSummaryUseCase,
)
from src.application.use_cases.habits.create_habit import CreateHabitUseCase
from src.application.use_cases.habits.get_user_habits import GetUserHabitsUseCase
from src.application.use_cases.habits.log_completion import LogCompletionUseCase
from src.domain.exceptions import InvalidCredentialsError
from src.infrastructure.database.repositories.postgres_habit_log_repository import (
    PostgresHabitLogRepository,
)
from src.infrastructure.database.repositories.postgres_habit_repository import (
    PostgresHabitRepository,
)
from src.infrastructure.database.repositories.postgres_user_repository import (
    PostgresUserRepository,
)
from src.infrastructure.database.session import get_async_session
from src.infrastructure.security.jwt_handler import JWTHandler
from src.infrastructure.security.password_hasher import PasswordHasher

settings = get_settings()
_bearer = HTTPBearer()

_password_hasher = PasswordHasher()
_jwt_handler = JWTHandler(
    secret_key=settings.SECRET_KEY,
    algorithm=settings.ALGORITHM,
    expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_async_session():
        yield session


DbSession = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(_bearer)],
    db: DbSession,
) -> UserDTO:
    try:
        payload = _jwt_handler.decode_token(credentials.credentials)
        user_id: str = payload.get("sub", "")
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    repo = PostgresUserRepository(db)
    from uuid import UUID

    user = await repo.find_by_id(UUID(user_id))
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return UserDTO(id=user.id, username=user.username, email=user.email, is_active=user.is_active)


CurrentUser = Annotated[UserDTO, Depends(get_current_user)]


def get_register_use_case(db: DbSession) -> RegisterUserUseCase:
    return RegisterUserUseCase(PostgresUserRepository(db), _password_hasher)


def get_login_use_case(db: DbSession) -> LoginUserUseCase:
    return LoginUserUseCase(PostgresUserRepository(db), _password_hasher, _jwt_handler)


def get_create_habit_use_case(db: DbSession) -> CreateHabitUseCase:
    return CreateHabitUseCase(PostgresHabitRepository(db))


def get_user_habits_use_case(db: DbSession) -> GetUserHabitsUseCase:
    return GetUserHabitsUseCase(PostgresHabitRepository(db))


def get_log_completion_use_case(db: DbSession) -> LogCompletionUseCase:
    return LogCompletionUseCase(PostgresHabitRepository(db), PostgresHabitLogRepository(db))


def get_dashboard_use_case(db: DbSession) -> GetDashboardSummaryUseCase:
    return GetDashboardSummaryUseCase(PostgresHabitRepository(db), PostgresHabitLogRepository(db))
