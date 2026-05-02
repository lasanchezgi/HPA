from fastapi import APIRouter, Depends

from src.application.use_cases.coach.chat_with_coach import ChatWithCoachDTO
from src.delivery.dependencies import (
    CurrentUser,
    get_coach_repository,
    get_coach_use_case,
)
from src.delivery.schemas.coach_schemas import (
    CoachChatRequest,
    CoachChatResponse,
    CoachHistoryResponse,
    CoachMessageSchema,
)

router = APIRouter(prefix="/coach", tags=["coach"])


@router.post("/chat", response_model=CoachChatResponse)
async def chat_with_coach(
    request: CoachChatRequest,
    current_user: CurrentUser,
    use_case=Depends(get_coach_use_case),
) -> CoachChatResponse:
    result = await use_case.execute(
        ChatWithCoachDTO(
            user_id=current_user.id,
            message=request.message,
        )
    )
    return CoachChatResponse(
        reply=result.reply,
        conversation_id=result.conversation_id,
    )


@router.get("/history", response_model=CoachHistoryResponse)
async def get_coach_history(
    current_user: CurrentUser,
    coach_repo=Depends(get_coach_repository),
) -> CoachHistoryResponse:
    conversation = await coach_repo.find_or_create_by_user_id(current_user.id)
    return CoachHistoryResponse(
        conversation_id=conversation.id,
        messages=[
            CoachMessageSchema(
                role=m.role,
                content=m.content,
                created_at=m.created_at.isoformat(),
            )
            for m in conversation.messages
        ],
    )
