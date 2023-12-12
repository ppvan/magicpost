from datetime import date, datetime

from sqlmodel import Field

from magicpost.auth.models import Role
from magicpost.models import PHONE_REGEX, MyBaseModel


class UserCreate(MyBaseModel):
    username: str = Field(min_length=1)
    password: str
    fullname: str = Field(min_length=1)
    birth: date
    phone: str = Field(regex=PHONE_REGEX)
    role: Role
    department_id: int = Field(gt=0)


class UserRead(MyBaseModel):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(min_length=1)
    hashed_password: str
    is_staff: bool = Field(default=False)
    fullname: str = Field(min_length=1)
    birth: date
    phone: str = Field(regex=PHONE_REGEX)
    role: Role

    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Token(MyBaseModel):
    access_token: str
    token_type: str


class TokenData(MyBaseModel):
    username: str | None = None
