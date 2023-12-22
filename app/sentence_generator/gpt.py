import asyncio
from contextlib import suppress

from g4f import ChatCompletion, debug, models
from g4f.Provider import BaseProvider


debug.logging = True
debug.version_check = False


class GPT:
    def __init__(self, providers: list[BaseProvider]) -> None:
        self.providers = providers

    async def ask_gpt(self, provider, prompt: str) -> str | None:
        with suppress(Exception):
            return await ChatCompletion.create_async(
                model=models.default,
                messages=[{"role": "user", "content": prompt}],
                provider=provider,
            )
        
        return None

    async def retry_ask(self, prompt: str) -> str | None:
        for provider in self.providers:
            gpt_answer = await self.ask_gpt(provider, prompt)

            if gpt_answer:
                return gpt_answer
        
        return None
    
    async def bulk_ask(self, prompt: str) -> list[str | None]:
        calls = [self.ask_gpt(provider, prompt) for provider in self.providers]
        packed_calls = await asyncio.gather(*calls)
        return self._filter_bulk_answers(packed_calls)

    def _filter_bulk_answers(self, bulk_answers: list[str | None]) -> list[str]:
        valid_responses = list(filter(lambda x: x is not None and x != "", bulk_answers))
        return valid_responses

