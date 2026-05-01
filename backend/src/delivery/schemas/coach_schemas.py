from uuid import UUID

from pydantic import BaseModel, Field


class CoachChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)


class CoachChatResponse(BaseModel):
    reply: str
    conversation_id: UUID


class CoachMessageSchema(BaseModel):
    role: str
    content: str
    created_at: str


class CoachHistoryResponse(BaseModel):
    conversation_id: UUID
    messages: list[CoachMessageSchema]
