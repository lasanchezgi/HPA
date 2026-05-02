import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.coach_conversation import CoachConversation, CoachMessage
from src.domain.repositories.coach_repository import CoachRepository
from src.infrastructure.database.models.coach_model import CoachConversationModel


class PostgresCoachRepository(CoachRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_or_create_by_user_id(self, user_id: uuid.UUID) -> CoachConversation:
        stmt = select(CoachConversationModel).where(
            CoachConversationModel.user_id == user_id
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            conversation = CoachConversation.new(user_id)
            new_model = CoachConversationModel(
                id=conversation.id,
                user_id=user_id,
                messages=[],
            )
            self.session.add(new_model)
            await self.session.commit()
            return conversation

        return self._to_entity(model)

    async def save(self, conversation: CoachConversation) -> CoachConversation:
        serialized_messages = [
            {
                "role": m.role,
                "content": m.content,
                "created_at": m.created_at.isoformat(),
            }
            for m in conversation.messages
        ]
        stmt = (
            pg_insert(CoachConversationModel)
            .values(
                id=conversation.id,
                user_id=conversation.user_id,
                messages=serialized_messages,
            )
            .on_conflict_do_update(
                index_elements=["user_id"],
                set_={"messages": serialized_messages},
            )
            .returning(CoachConversationModel)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return self._to_entity(result.scalar_one())

    def _to_entity(self, model: CoachConversationModel) -> CoachConversation:
        messages = [
            CoachMessage(
                role=m["role"],
                content=m["content"],
                created_at=datetime.fromisoformat(m["created_at"]),
            )
            for m in (model.messages or [])
        ]
        return CoachConversation(
            id=model.id,
            user_id=model.user_id,
            messages=messages,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
