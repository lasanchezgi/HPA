from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.application.use_cases.auth.change_password import ChangePasswordUseCase
from src.application.use_cases.auth.login_user import LoginUserUseCase
from src.application.use_cases.auth.register_user import RegisterUserUseCase
from src.application.use_cases.auth.update_profile import UpdateProfileUseCase
from src.application.dtos.auth_dtos import ChangePasswordDTO, LoginUserDTO, RegisterUserDTO, UpdateProfileDTO
from src.delivery.dependencies import (
    CurrentUser,
    get_change_password_use_case,
    get_login_use_case,
    get_register_use_case,
    get_update_profile_use_case,
)
from src.delivery.schemas.auth_schemas import (
    ChangePasswordRequest,
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UpdateProfileRequest,
    UserResponse,
)
from src.domain.exceptions import InvalidCredentialsError

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


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: CurrentUser) -> UserResponse:
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active,
    )


@router.patch("/me", response_model=UserResponse)
async def update_profile(
    body: UpdateProfileRequest,
    current_user: CurrentUser,
    use_case: Annotated[UpdateProfileUseCase, Depends(get_update_profile_use_case)],
) -> UserResponse:
    dto = UpdateProfileDTO(user_id=current_user.id, username=body.username)
    user = await use_case.execute(dto)
    return UserResponse(id=user.id, username=user.username, email=user.email, is_active=user.is_active)


@router.patch("/me/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    body: ChangePasswordRequest,
    current_user: CurrentUser,
    use_case: Annotated[ChangePasswordUseCase, Depends(get_change_password_use_case)],
) -> None:
    dto = ChangePasswordDTO(
        user_id=current_user.id,
        current_password=body.current_password,
        new_password=body.new_password,
    )
    try:
        await use_case.execute(dto)
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña actual es incorrecta",
        )
