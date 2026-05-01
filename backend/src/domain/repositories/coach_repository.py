from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.coach_conversation import CoachConversation


class CoachRepository(ABC):

    @abstractmethod
    async def find_or_create_by_user_id(self, user_id: UUID) -> CoachConversation:
        ...

    @abstractmethod
    async def save(self, conversation: CoachConversation) -> CoachConversation:
        ...
