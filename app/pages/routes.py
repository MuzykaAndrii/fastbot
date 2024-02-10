from fastapi import APIRouter, Depends, Request

from app.users.models import User
from app.auth.dependencies import get_current_user
from .template_engine import engine as template_engine


router = APIRouter(
    prefix="/pages",
    tags=["Frontend"],
)

@router.get("/dashboard/{vocabulary_id}")
async def dashboard(
    request: Request,
    vocabulary_id: int,
    user: User = Depends(get_current_user)
):

    return template_engine.TemplateResponse(
        name="dashboard.html",
        context={"request": request},
    )