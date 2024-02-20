from fastapi import Depends

from app.backend.auth.dependencies import get_current_user
from app.backend.users.models import User
from app.backend.vocabulary.services import VocabularyService


async def user_vocabularies_list(user: User = Depends(get_current_user)):
    vocabularies = await VocabularyService.get_all_user_vocabularies(user.id)
    return vocabularies