from src.application.dtos.auth_dtos import ChangePasswordDTO
from src.domain.exceptions import InvalidCredentialsError
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.security.password_hasher import PasswordHasher


class ChangePasswordUseCase:
    def __init__(
        self, user_repo: UserRepository, password_hasher: PasswordHasher
    ) -> None:
        self._user_repo = user_repo
        self._password_hasher = password_hasher

    async def execute(self, dto: ChangePasswordDTO) -> None:
        user = await self._user_repo.find_by_id(dto.user_id)
        if not user or not user.is_active:
            raise InvalidCredentialsError()

        if not self._password_hasher.verify(dto.current_password, user.hashed_password):
            raise InvalidCredentialsError()

        user.hashed_password = self._password_hasher.hash(dto.new_password)
        await self._user_repo.update(user)
