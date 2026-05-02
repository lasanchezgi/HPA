from openai import AsyncOpenAI

from config import Settings


class OpenAICoachClient:
    def __init__(self, settings: Settings) -> None:
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.max_tokens = settings.COACH_MAX_TOKENS
        self.temperature = settings.COACH_TEMPERATURE

    async def get_completion(
        self,
        system_prompt: str,
        messages: list[dict],
    ) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                *messages,
            ],
        )
        return response.choices[0].message.content or ""
