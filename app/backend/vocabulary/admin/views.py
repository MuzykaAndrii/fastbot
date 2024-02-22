from typing import Any
from contextlib import suppress

from starlette.requests import Request
from starlette_admin.contrib.sqla.ext.pydantic import ModelView
from app.shared.exceptions import VocabularyIsAlreadyActive

from app.backend.vocabulary.admin.schemas import LanguagePairAdminSchema, VocabularyAdminSchema
from app.backend.vocabulary.models import LanguagePair, VocabularySet
from app.backend.vocabulary.services import VocabularyService


class VocabularyAdminView(ModelView):
    def __init__(self, *args, **kwargs):
        model = VocabularySet
        pydantic_model = VocabularyAdminSchema
        icon = "fa-regular fa-folder"
        name = "Vocabulary"
        label = "Vocabularies"

        super().__init__(model, pydantic_model, icon, name, label)

    fields = [
        VocabularySet.id,
        VocabularySet.name,
        VocabularySet.created_at,
        VocabularySet.owner,
        VocabularySet.is_active,
        VocabularySet.language_pairs,
    ]

    async def before_edit(self, request: Request, data: dict, vocabulary: VocabularySet) -> None:
        await self._disable_user_active_vocabulary_if_given_ought_be_enabled(vocabulary)
    

    async def before_create(self, request: Request, data: dict, vocabulary: VocabularySet) -> None:
        await self._disable_user_active_vocabulary_if_given_ought_be_enabled(vocabulary)


    async def _disable_user_active_vocabulary_if_given_ought_be_enabled(self, vocabulary: VocabularySet) -> None:
        if vocabulary.is_active:
            await VocabularyService.disable_user_active_vocabulary(vocabulary.owner_id)


class LanguagePairAdminView(ModelView):
    def __init__(self, *args, **kwargs):
        model = LanguagePair
        pydantic_model = LanguagePairAdminSchema
        icon = "fa-regular fa-folder"
        name = "Language pair"
        label = "Language pairs"

        super().__init__(model, pydantic_model, icon, name, label)
    
    fields = [
        LanguagePair.id,
        LanguagePair.vocabulary,
        LanguagePair.word,
        LanguagePair.translation,
    ]