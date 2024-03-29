from fastapi import Request, Response

from app.config import settings


class CookieManager:
    def __init__(self, cookie_name: str) -> None:
        self.cookie_name = cookie_name

    def set_cookie(self, response_obj: Response, token: str) -> Response:
        response_obj.set_cookie(
            self.cookie_name,
            token,
            httponly=True,
            samesite="lax",
            secure=not settings.DEBUG,
        )

        return response_obj

    def get_cookie(self, request: Request) -> str | None:
        token = request.cookies.get(self.cookie_name)

        if not token:
            return None
        return token

    def delete_cookie(self, response: Response) -> Response:
        response.delete_cookie(self.cookie_name)
        return response