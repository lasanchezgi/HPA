from src.application.dtos.auth_dtos import UpdateProfileDTO, UserDTO
from src.domain.exceptions import InvalidCredentialsError
from src.domain.repositories.user_repository import UserRepository


class UpdateProfileUseCase:
    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

    async def execute(self, dto: UpdateProfileDTO) -> UserDTO:
        user = await self._user_repo.find_by_id(dto.user_id)
        if not user or not user.is_active:
            raise InvalidCredentialsError()

        user.username = dto.username
        updated = await self._user_repo.update(user)
        return UserDTO(
            id=updated.id,
            username=updated.username,
            email=updated.email,
            is_active=updated.is_active,
        )
