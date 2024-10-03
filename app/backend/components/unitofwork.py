from app.backend.db.unitofwork import BaseUnitOfWork
from app.backend.users.dal import UserDAL
from app.backend.vocabulary.dal import LanguagePairDAL, VocabularySetDAL


class UnitOfWork(BaseUnitOfWork):
    def init_repos(self) -> None:
        self.users = self.register_repo(UserDAL)
        self.vocabularies = self.register_repo(VocabularySetDAL)
        self.language_pairs = self.register_repo(LanguagePairDAL)