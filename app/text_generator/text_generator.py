from typing import Iterable
from .prompts import Prompts
from app.gpt.gpt import GPT


class TextGenerator:
    def __init__(self, gpt: GPT) -> None:
        self.gpt = gpt

    async def get_sentence_from_keyword(self, keyword: str, format: bool = True) -> str | None:
        prompt = Prompts.sentence_from_word.format(word=keyword)
        sentence = await self.gpt.get_answer(prompt)
        
        if format:
            return self._format_answer(sentence)
        else:
            return sentence
    
    async def get_text_from_keywords(self, *keywords) -> str | None:
        prompt = Prompts.text_from_words.format(
            text_length=round(len(keywords)/2),
            keywords=", ".join(keywords),
        )
        text = await self.gpt.get_answer(prompt)
        return text

    def _format_answer(sentence: str) -> str:
        sentence = sentence.split("\n")[-1]
        if ":" in sentence:
            return sentence.split(":")[-1]
        return sentence


async def generate_sentence_from_word(word: str) -> str | None:
    gpt = GPT.from_base_providers()
    tg = TextGenerator(gpt)
    sentence = await tg.get_sentence_from_keyword(word)

    return sentence

async def generate_text_from_words(words: Iterable[str]) -> str:
    gpt = GPT.from_base_providers()
    tg = TextGenerator(gpt)
    text = await tg.get_text_from_keywords(*words)

    return text