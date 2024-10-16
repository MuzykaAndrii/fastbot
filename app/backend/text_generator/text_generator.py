from typing import Iterable

from . import prompts
from app.backend.gpt import GPT


class TextGenerator:
    def __init__(self, gpt: GPT) -> None:
        self.gpt = gpt

    async def get_sentence_from_keyword(self, keyword: str) -> str | None:
        prompt = prompts.sentence_from_word.format(word=keyword)
        return await self.gpt.get_answer(prompt)
    
    async def get_sentence_from_two_keywords(self, primary_word: str, secondary_word: str) -> str | None:
        prompt = prompts.sentence_from_two_words.format(primary_word=primary_word, secondary_word=secondary_word)
        return await self.gpt.get_answer(prompt)
    
    async def get_text_from_keywords(self, keywords: Iterable[str]) -> str | None:
        # TODO: add randomness to text length calculating
        prompt = prompts.text_from_words.format(
            text_length=len(keywords) // 4,
            keywords=", ".join(keywords),
        )

        return await self.gpt.get_answer(prompt)
