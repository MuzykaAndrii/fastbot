from .prompts import Prompts
from ..gpt.gpt import GPT


class SentenceGenerator:
    def __init__(self, gpt: GPT) -> None:
        self.gpt = gpt

    async def gen_from_keyword(self, keyword: str) -> str | None:
        prompt = Prompts.sentence_from_word.format(word=keyword)

        return await self.gpt.get_answer(prompt)


def formatter(sentence: str) -> str:
    sentence = sentence.split("\n")[-1]
    if ":" in sentence:
        return sentence.split(":")[-1]
    return sentence


async def generate_sentence_from_word(word: str) -> str | None:
    gpt = GPT.from_base_providers()
    sg = SentenceGenerator(gpt)
    sentence = await sg.gen_from_keyword(word)

    return sentence