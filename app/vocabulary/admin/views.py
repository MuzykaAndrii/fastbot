from starlette_admin.contrib.sqla.ext.pydantic import ModelView

from app.vocabulary.admin.schemas import LanguagePairAdminSchema, VocabularyAdminSchema
from app.vocabulary.models import LanguagePair, VocabularySet


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