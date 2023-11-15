from app.db.dal import BaseDAL
from app.words.models import VocabularyBundle, WordPair


class VocabularyBundleDAL(BaseDAL):
    model = VocabularyBundle


class WordPairDAL(BaseDAL):
    model = WordPair