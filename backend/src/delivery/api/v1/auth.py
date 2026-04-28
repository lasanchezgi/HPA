from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.application.use_cases.auth.login_user import LoginUserUseCase
from src.application.use_cases.auth.register_user import RegisterUserUseCase
from src.application.dtos.auth_dtos import LoginUserDTO, RegisterUserDTO
from src.delivery.dependencies import get_login_use_case, get_register_use_case
from src.delivery.schemas.auth_schemas import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    body: RegisterRequest,
    use_case: Annotated[RegisterUserUseCase, Depends(get_register_use_case)],
) -> UserResponse:
    dto = RegisterUserDTO(
        username=body.username,
        email=body.email,
        password=body.password,
    )
    user = await use_case.execute(dto)
    return UserResponse(id=user.id, username=user.username, email=user.email, is_active=user.is_active)


@router.post("/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    use_case: Annotated[LoginUserUseCase, Depends(get_login_use_case)],
) -> TokenResponse:
    dto = LoginUserDTO(email=body.email, password=body.password)
    token = await use_case.execute(dto)
    return TokenResponse(access_token=token.access_token, token_type=token.token_type)
