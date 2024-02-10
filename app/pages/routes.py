from fastapi import APIRouter, Request

from .template_engine import engine as template_engine


router = APIRouter(
    prefix="/pages",
    tags=["Frontend"],
)

@router.get("/dashboard")
def dashboard(request: Request):
    return template_engine.TemplateResponse(
        name="dashboard.html",
        context={"request": request},
    )