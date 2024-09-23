import random
import logging

import asyncio
from g4f import models, debug
from g4f.Provider import BaseProvider
from g4f.client import AsyncClient


debug.logging = False
debug.version_check = False 
log = logging.getLogger("backend.gpt")


class GPT:
    def __init__(self, providers: list[BaseProvider]) -> None:
        self.providers = providers
    
    @classmethod
    def from_base_providers(cls):
        from .providers import providers
        return cls(providers)

    async def manual_ask(self, provider: BaseProvider, prompt: str) -> str | None:
        try:
            response = await AsyncClient(provider).chat.completions.create(
                model=models.default,
                messages=[{"role": "user", "content": prompt}],
            )
            answer = response.choices[0].message.content
            log.debug(f"{provider.__name__} answer: {answer}")
            return answer
        except Exception:
            log.debug(f"{provider.__name__} does not responded")
        
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
            log.warning("No one gpt provider not responded.")
            return None
        else:
            log.info(f"GPT responded: {answer}")
            return answer

