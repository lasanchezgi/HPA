from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class CoachMessage:
    role: str  # 'user' | 'assistant'
    content: str
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class CoachConversation:
    id: UUID
    user_id: UUID
    messages: list[CoachMessage]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def new(cls, user_id: UUID) -> "CoachConversation":
        now = datetime.utcnow()
        return cls(
            id=uuid4(),
            user_id=user_id,
            messages=[],
            created_at=now,
            updated_at=now,
        )

    def add_message(self, role: str, content: str) -> None:
        self.messages.append(CoachMessage(role=role, content=content))
        self.updated_at = datetime.utcnow()

    def last_n_messages(self, n: int = 10) -> list[CoachMessage]:
        return self.messages[-n:]
