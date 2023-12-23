from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)


class UserCreateAdminSchema(BaseModel):
    username: str | None = Field(min_length=5, max_length=30)
    email: EmailStr
    password: str = Field(default=None, min_length=8, max_length=30)
    is_superuser: bool = False