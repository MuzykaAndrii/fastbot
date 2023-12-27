import asyncio
from contextlib import suppress
import random

from g4f import ChatCompletion, debug, models
from g4f.Provider import BaseProvider


debug.logging = False
debug.version_check = False


class GPT:
    def __init__(self, providers: list[BaseProvider]) -> None:
        self.providers = providers

    async def manual_ask(self, provider, prompt: str) -> str | None:
        with suppress(Exception):
            return await ChatCompletion.create_async(
                model=models.default,
                messages=[{"role": "user", "content": prompt}],
                provider=provider,
            )
        
        return None
    
    async def get_answers(self, prompt: str) -> list[str]:
        calls = [self.manual_ask(provider, prompt) for provider in self.providers]
        answers = await asyncio.gather(*calls)
        valid_answers = self._filter_answers(answers)
        return valid_answers
    
    async def get_answer(self, prompt: str) -> str | None:
        answers = await self.get_answers(prompt)
        return self._fetch_random_answer(answers)


    def _filter_answers(self, bulk_answers: list[str | None]) -> list[str]:
        valid_responses = list(filter(lambda x: x is not None and x != "", bulk_answers))
        return valid_responses

    def _fetch_random_answer(self, answers: list[str]) -> str | None:
        try:
            answer = random.choice(answers)
        except IndexError:
            return None
        else:
            return answer

