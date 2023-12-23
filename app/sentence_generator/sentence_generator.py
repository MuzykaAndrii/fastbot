import random
from .providers import providers
from .prompts import Prompts
from .gpt import GPT


class SentenceGenerator:
    def __init__(self, gpt: GPT) -> None:
        self.gpt = gpt

    async def gen_from_keyword(self, keyword: str) -> str | None:
        prompt = Prompts.sentence_from_word.format(word=keyword)

        return await self.gpt.bulk_ask(prompt)


def formatter(sentence: str) -> str:
    sentence = sentence.split("\n")[-1]
    if ":" in sentence:
        return sentence.split(":")[-1]
    return sentence


async def generate_sentence_from_word(word: str) -> str | None:
    gpt = GPT(providers)
    sg = SentenceGenerator(gpt)
    sentences = await sg.gen_from_keyword(word)

    try:
        sentence = random.choice(sentences)
    except IndexError:
        return None
    else:
        return formatter(sentence)