from fastapi import APIRouter, Request


router = APIRouter(prefix="/bot", tags=['bot'])

@router.post('/')
async def test(request: Request):
    print(await request.json())
    return ""