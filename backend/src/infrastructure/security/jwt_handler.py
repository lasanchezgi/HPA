from datetime import UTC, datetime, timedelta
from typing import Any

from jose import JWTError, jwt

from src.domain.exceptions import InvalidCredentialsError


class JWTHandler:
    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        expire_minutes: int = 30,
    ) -> None:
        self._secret = secret_key
        self._algorithm = algorithm
        self._expire_minutes = expire_minutes

    def create_access_token(
        self, subject: str, extra: dict[str, Any] | None = None
    ) -> str:
        expire = datetime.now(UTC) + timedelta(minutes=self._expire_minutes)
        payload: dict[str, Any] = {"sub": subject, "exp": expire}
        if extra:
            payload.update(extra)
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)

    def decode_token(self, token: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(token, self._secret, algorithms=[self._algorithm])
            return payload
        except JWTError as exc:
            raise InvalidCredentialsError() from exc
