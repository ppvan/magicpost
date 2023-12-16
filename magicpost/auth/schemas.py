from datetime import date, datetime

from pydantic import BaseModel, Field, PositiveInt

from magicpost.auth.models import Role
from magicpost.models import PHONE_REGEX


class UserCreate(BaseModel):
    username: str = Field(min_length=1)
    password: str
    fullname: str = Field(min_length=1)
    birth: date
    phone: str = Field(pattern=PHONE_REGEX, min_length=1, max_length=10)
    role: Role
    department_id: int = Field(gt=0)


class UserRead(BaseModel):
    id: PositiveInt
    username: str = Field(min_length=1)
    hashed_password: str
    is_staff: bool = Field(default=False)
    fullname: str = Field(min_length=1)
    birth: date
    phone: str = Field(pattern=PHONE_REGEX, min_length=1, max_length=10)
    role: Role

    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
