from .providers import providers
from .prompts import Prompts
from .gpt import GPT


class SentenceGenerator:
    def __init__(self, gpt: GPT) -> None:
        self.gpt = gpt

    async def gen_from_keyword(self, keyword: str) -> str | None:
        prompt = Prompts.sentence_from_word.format(word=keyword)

        return await self.gpt.retry_ask(prompt)


def formatter(sentence: str) -> str:
    return sentence.split("\n")[-1]


async def generate_sentence_from_word(word: str) -> str | None:
    gpt = GPT(providers)
    sg = SentenceGenerator(gpt)
    sentence = await sg.gen_from_keyword(word)

    if not sentence:
        return None
    
    return formatter(sentence)