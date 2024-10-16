from app.backend.components.unitofwork import UnitOfWork
from app.backend.vocabulary.exceptions import NoActiveVocabulariesError
from app.backend.vocabulary.models import LanguagePair


class LanguagePairService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow
    

    async def get_random_lang_pair_from_every_active_vocabulary(self) -> list[LanguagePair]:
        async with self._uow(persistent=False) as uow:
            random_lang_pairs = await uow.language_pairs.get_one_random_language_pair_from_each_active_vocabulary()

        if not random_lang_pairs:
            raise NoActiveVocabulariesError

        return random_lang_pairs
    

    async def get_random_lang_pair_from_random_inactive_users_vocabulary(self, users_ids: list[int]) -> list[LanguagePair]:
        async with self._uow(persistent=False) as uow:
            random_lang_pairs = await uow.language_pairs.get_one_random_language_pairs_from_random_inactive_users_vocabulary(users_ids)

        return random_lang_pairs
    

    async def get_language_pairs_for_notifications(self) -> tuple[list[LanguagePair], list[LanguagePair]]:
        async with self._uow(persistent=False):
            primary_lps = await self.get_random_lang_pair_from_every_active_vocabulary()
            secondary_lps = await self.get_random_lang_pair_from_random_inactive_users_vocabulary(
                [lp.vocabulary.owner_id for lp in primary_lps]
            )

        return primary_lps, secondary_lps