from pydantic import (
    BaseModel,
    Field,
    EmailStr,
)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=5, max_length=30)


class ApiKeyAuthorizationSchema(BaseModel):
    api_key: str