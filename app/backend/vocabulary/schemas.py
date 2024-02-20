from pydantic import BaseModel


class AuthorizationSchema(BaseModel):
    api_key: str