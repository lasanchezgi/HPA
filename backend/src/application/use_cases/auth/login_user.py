from src.application.dtos.auth_dtos import LoginUserDTO, TokenDTO
from src.domain.exceptions import InvalidCredentialsError
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.security.jwt_handler import JWTHandler
from src.infrastructure.security.password_hasher import PasswordHasher


class LoginUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        jwt_handler: JWTHandler,
    ) -> None:
        self._repo = user_repository
        self._hasher = password_hasher
        self._jwt = jwt_handler

    async def execute(self, dto: LoginUserDTO) -> TokenDTO:
        user = await self._repo.find_by_email(dto.email)
        if not user or not self._hasher.verify(dto.password, user.hashed_password):
            raise InvalidCredentialsError()

        token = self._jwt.create_access_token(
            subject=str(user.id), extra={"email": user.email}
        )
        return TokenDTO(access_token=token)
