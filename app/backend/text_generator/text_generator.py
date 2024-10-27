from typing import Iterable

from . import prompts
from app.backend.gpt import GPT


class TextGenerator:
    def __init__(self, gpt: GPT, clean_answers: bool = True) -> None:
        self.gpt = gpt
        self._clean = clean_answers

    async def get_sentence_from_keyword(self, keyword: str) -> str | None:
        prompt = prompts.sentence_from_word.format(word=keyword)
        return await self.gpt.get_answer(prompt)

    async def get_sentence_from_two_keywords(
        self,
        primary_word: str,
        secondary_word: str,
    ) -> str | None:
        prompt = prompts.sentence_from_two_words.format(
            primary_word=primary_word, secondary_word=secondary_word
        )
        answer = await self.gpt.get_answer(prompt)
        return answer

    async def get_text_from_keywords(self, keywords: Iterable[str]) -> str | None:
        # TODO: add randomness to text length calculating
        prompt = prompts.text_from_words.format(
            text_length=len(keywords) // 4,
            keywords=", ".join(keywords),
        )

        answer = await self.gpt.get_answer(prompt)
        return answer

    def _clean_answer(self, answer: str) -> str | None:
        if not answer:
            return None

        answer = answer.strip()

        if not self._clean:
            return answer

        if ":" in answer:
            answer = answer.split(":")[1]

        if "." in answer:
            answer = answer.split(".")[0]

        return answer
