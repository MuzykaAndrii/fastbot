from typing import Iterable

from . import prompts
from app.backend.gpt import GPT


class TextGenerator:
    def __init__(self, gpt: GPT) -> None:
        self.gpt = gpt

    async def get_sentence_from_keyword(self, keyword: str, format: bool = True) -> str | None:
        prompt = prompts.sentence_from_word.format(word=keyword)
        sentence = await self.gpt.get_answer(prompt)
        
        if format and sentence is not None:
            return self._format_answer(sentence)
        else:
            return sentence
    
    async def get_sentence_from_two_keywords(
        self,
        primary_word: str,
        secondary_word: str,
        format: bool = True
    ) -> str | None:
        prompt = prompts.sentence_from_two_words.format(primary_word=primary_word, secondary_word=secondary_word)
        sentence = await self.gpt.get_answer(prompt)
        
        if format and sentence is not None:
            return self._format_answer(sentence)
        else:
            return sentence
    
    async def get_text_from_keywords(self, keywords: Iterable[str]) -> str | None:
        # TODO: add randomness to text length calculating
        prompt = prompts.text_from_words.format(
            text_length=len(keywords) // 4,
            keywords=", ".join(keywords),
        )
        text = await self.gpt.get_answer(prompt)
        return text

    def _format_answer(self, sentence: str) -> str:
        sentence = sentence.split("\n")[-1]
        if ":" in sentence:
            return sentence.split(":")[-1]
        return sentence
