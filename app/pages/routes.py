from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from app.shared.exceptions import UserIsNotOwnerOfVocabulary, VocabularyDoesNotExist

from app.users.models import User
from app.auth.dependencies import get_current_user
from app.vocabulary.services import VocabularyService
from .template_engine import engine as template_engine


router = APIRouter(
    prefix="/pages",
    tags=["Frontend"],
)

@router.get("/vocabulary/{vocabulary_id}/edit", response_class=HTMLResponse)
async def edit_vocabulary(
    request: Request,
    vocabulary_id: int,
    user: User = Depends(get_current_user)
):
    try:
        vocabulary = await VocabularyService.get_vocabulary(user.id, vocabulary_id)
    except VocabularyDoesNotExist:
        raise HTTPException(404, "Vocabulary does not exist")
    except UserIsNotOwnerOfVocabulary:
        raise HTTPException(403, "Permission denied")
    
    vocabularies = await VocabularyService.get_all_user_vocabularies(user.id)

    return template_engine.TemplateResponse(
        name="edit_vocabulary.html",
        context={"request": request, "current_vocabulary": vocabulary, "vocabularies": vocabularies},
    )