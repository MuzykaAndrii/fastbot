from fastapi import Request, Response

from app.backend.components.config import app_settings


class FastAPICookieManager:
    def __init__(self, cookie_name: str) -> None:
        self.cookie_name = cookie_name

    def set_cookie(self, response_obj: Response, data: str) -> Response:
        response_obj.set_cookie(
            self.cookie_name,
            data,
            httponly=True,
            samesite="lax",
            secure=not app_settings.DEBUG,
        )

        return response_obj

    def get_cookie(self, request: Request) -> str | None:
        return request.cookies.get(self.cookie_name)


    def delete_cookie(self, response: Response) -> Response:
        response.delete_cookie(self.cookie_name)
        return response