from app.backend.db.unitofwork import BaseUnitOfWork
from app.backend.users.dal import UserDAL
from app.backend.vocabulary.dal import LanguagePairDAL, VocabularySetDAL


class UnitOfWork(BaseUnitOfWork):
    def _init_repos(self) -> None:
        self.users = self._register_repo(UserDAL)
        self.vocabularies = self._register_repo(VocabularySetDAL)
        self.language_pairs = self._register_repo(LanguagePairDAL)