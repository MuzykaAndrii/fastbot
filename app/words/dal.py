from app.db.dal import BaseDAL
from app.words.models import VocabularySet, LanguagePair


class VocabularySetDAL(BaseDAL):
    model = VocabularySet


class LanguagePairDAL(BaseDAL):
    model = LanguagePair