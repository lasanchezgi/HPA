from datetime import datetime, timezone
from uuid import uuid4

from src.application.dtos.auth_dtos import RegisterUserDTO, UserDTO
from src.domain.entities.user import User
from src.domain.exceptions import UserAlreadyExistsError
from src.domain.repositories.user_repository import UserRepository
from src.domain.value_objects.email import Email
from src.infrastructure.security.password_hasher import PasswordHasher


class RegisterUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ) -> None:
        self._repo = user_repository
        self._hasher = password_hasher

    async def execute(self, dto: RegisterUserDTO) -> UserDTO:
        Email(dto.email)  # validates format

        existing = await self._repo.find_by_email(dto.email)
        if existing:
            raise UserAlreadyExistsError(dto.email)

        now = datetime.now(timezone.utc)
        user = User(
            id=uuid4(),
            username=dto.username,
            email=dto.email,
            hashed_password=self._hasher.hash(dto.password),
            is_active=True,
            created_at=now,
            updated_at=now,
        )
        saved = await self._repo.save(user)
        return UserDTO(
            id=saved.id,
            username=saved.username,
            email=saved.email,
            is_active=saved.is_active,
        )
