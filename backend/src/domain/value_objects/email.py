import re
from dataclasses import dataclass

from src.domain.exceptions import InvalidEmailError

_EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        if not _EMAIL_REGEX.match(self.value):
            raise InvalidEmailError(self.value)

    def __str__(self) -> str:
        return self.value
