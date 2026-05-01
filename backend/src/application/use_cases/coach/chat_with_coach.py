from dataclasses import dataclass
from uuid import UUID

from src.domain.repositories.coach_repository import CoachRepository
from src.domain.repositories.habit_repository import HabitRepository
from src.application.use_cases.dashboard.get_dashboard_summary import (
    GetDashboardSummaryUseCase,
)
from src.infrastructure.ai.openai_client import OpenAICoachClient
from src.infrastructure.ai.coach_prompts import build_system_prompt


@dataclass
class ChatWithCoachDTO:
    user_id: UUID
    message: str


@dataclass
class ChatWithCoachResultDTO:
    reply: str
    conversation_id: UUID


class ChatWithCoachUseCase:

    def __init__(
        self,
        coach_repo: CoachRepository,
        habit_repo: HabitRepository,
        dashboard_use_case: GetDashboardSummaryUseCase,
        openai_client: OpenAICoachClient,
    ) -> None:
        self.coach_repo = coach_repo
        self.habit_repo = habit_repo
        self.dashboard_use_case = dashboard_use_case
        self.openai_client = openai_client

    async def execute(self, dto: ChatWithCoachDTO) -> ChatWithCoachResultDTO:
        conversation = await self.coach_repo.find_or_create_by_user_id(dto.user_id)

        dashboard = await self.dashboard_use_case.execute(dto.user_id)
        habits = await self.habit_repo.find_active_by_user_id(dto.user_id)

        system_prompt = build_system_prompt(dashboard, habits)

        conversation.add_message("user", dto.message)

        messages_for_llm = [
            {"role": m.role, "content": m.content}
            for m in conversation.last_n_messages(10)
        ]

        reply = await self.openai_client.get_completion(
            system_prompt=system_prompt,
            messages=messages_for_llm,
        )

        conversation.add_message("assistant", reply)
        await self.coach_repo.save(conversation)

        return ChatWithCoachResultDTO(
            reply=reply,
            conversation_id=conversation.id,
        )
