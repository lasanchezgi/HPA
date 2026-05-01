from dataclasses import dataclass
from uuid import UUID


@dataclass
class CoachMessageDTO:
    role: str
    content: str
    created_at: str


@dataclass
class CoachHistoryDTO:
    conversation_id: UUID
    messages: list[CoachMessageDTO]
