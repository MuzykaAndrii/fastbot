from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from app.shared.exceptions import UserIsNotOwnerOfVocabulary, VocabularyDoesNotExist, VocabularyIsAlreadyActive

from app.users.models import User
from app.auth.dependencies import get_current_user
from app.vocabulary.services import VocabularyService
from .template_engine import engine as template_engine


router = APIRouter(
    prefix="/pages",
    tags=["Frontend"],
)


@router.get("/vocabulary/{vocabulary_id}/activate", response_class=RedirectResponse)
async def activate_vocabulary(
    request: Request,
    vocabulary_id: int,
    user: User = Depends(get_current_user),
):
    try:
        vocabulary = await VocabularyService.disable_active_vocabulary_and_enable_given(user.id, vocabulary_id)
    except VocabularyDoesNotExist:
        raise HTTPException(404, "Vocabulary does not exist")
    except UserIsNotOwnerOfVocabulary:
        raise HTTPException(403, "Permission denied")
    except VocabularyIsAlreadyActive:
        pass
    
    return RedirectResponse(request.url_for("edit_vocabulary", vocabulary_id=vocabulary.id))



@router.get("/vocabulary/{vocabulary_id}/disable", response_class=RedirectResponse)
async def disable_vocabulary(
    request: Request,
    vocabulary_id: int,
    user: User = Depends(get_current_user),
):  
    vocabulary = await VocabularyService.disable_vocabulary(vocabulary_id)
    
    return RedirectResponse(request.url_for("edit_vocabulary", vocabulary_id=vocabulary.id))


@router.get("/vocabulary/{vocabulary_id}/edit", response_class=HTMLResponse)
async def edit_vocabulary(
    request: Request,
    vocabulary_id: int,
    user: User = Depends(get_current_user),
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