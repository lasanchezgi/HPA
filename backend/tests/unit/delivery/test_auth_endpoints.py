from unittest.mock import AsyncMock
from uuid import uuid4

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from main import app
from src.application.dtos.auth_dtos import TokenDTO, UserDTO
from src.delivery.dependencies import get_login_use_case, get_register_use_case
from src.domain.exceptions import InvalidCredentialsError, UserAlreadyExistsError


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


async def test_register_returns_201_with_user_data(client):
    mock_use_case = AsyncMock()
    mock_use_case.execute.return_value = UserDTO(
        id=uuid4(), username="alice", email="alice@example.com", is_active=True
    )
    app.dependency_overrides[get_register_use_case] = lambda: mock_use_case

    response = await client.post(
        "/api/v1/auth/register",
        json={"username": "alice", "email": "alice@example.com", "password": "secret123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "alice"
    assert data["email"] == "alice@example.com"
    assert data["is_active"] is True


async def test_register_duplicate_email_returns_409(client):
    mock_use_case = AsyncMock()
    mock_use_case.execute.side_effect = UserAlreadyExistsError("alice@example.com")
    app.dependency_overrides[get_register_use_case] = lambda: mock_use_case

    response = await client.post(
        "/api/v1/auth/register",
        json={"username": "alice", "email": "alice@example.com", "password": "secret123"},
    )
    assert response.status_code == 409


async def test_login_returns_200_with_token(client):
    mock_use_case = AsyncMock()
    mock_use_case.execute.return_value = TokenDTO(
        access_token="fake.jwt.token", token_type="bearer"
    )
    app.dependency_overrides[get_login_use_case] = lambda: mock_use_case

    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "alice@example.com", "password": "secret123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["access_token"] == "fake.jwt.token"
    assert data["token_type"] == "bearer"


async def test_login_wrong_password_returns_401(client):
    mock_use_case = AsyncMock()
    mock_use_case.execute.side_effect = InvalidCredentialsError()
    app.dependency_overrides[get_login_use_case] = lambda: mock_use_case

    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "alice@example.com", "password": "wrongpass"},
    )
    assert response.status_code == 401


async def test_protected_endpoint_without_token_returns_401(client):
    response = await client.get("/api/v1/habits/")
    assert response.status_code in (401, 403)
