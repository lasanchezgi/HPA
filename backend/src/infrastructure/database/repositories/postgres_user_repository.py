from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.database.models.user_model import UserModel


class PostgresUserRepository(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, user: User) -> User:
        model = _to_model(user)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return _to_entity(model)

    async def find_by_id(self, user_id: UUID) -> User | None:
        result = await self._session.get(UserModel, user_id)
        return _to_entity(result) if result else None

    async def find_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def update(self, user: User) -> User:
        model = await self._session.get(UserModel, user.id)
        if model:
            model.username = user.username
            model.email = user.email
            model.hashed_password = user.hashed_password
            model.is_active = user.is_active
            await self._session.flush()
            await self._session.refresh(model)
        return _to_entity(model)  # type: ignore[arg-type]

    async def soft_delete(self, user_id: UUID) -> None:
        model = await self._session.get(UserModel, user_id)
        if model:
            model.is_active = False
            await self._session.flush()


def _to_model(user: User) -> UserModel:
    return UserModel(
        id=user.id,
        username=user.username,
        email=user.email,
        hashed_password=user.hashed_password,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


def _to_entity(model: UserModel) -> User:
    return User(
        id=model.id,
        username=model.username,
        email=model.email,
        hashed_password=model.hashed_password,
        is_active=model.is_active,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )
