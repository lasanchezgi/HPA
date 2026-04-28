from dataclasses import dataclass
from uuid import UUID


@dataclass
class RegisterUserDTO:
    username: str
    email: str
    password: str


@dataclass
class LoginUserDTO:
    email: str
    password: str


@dataclass
class UserDTO:
    id: UUID
    username: str
    email: str
    is_active: bool


@dataclass
class TokenDTO:
    access_token: str
    token_type: str = "bearer"
