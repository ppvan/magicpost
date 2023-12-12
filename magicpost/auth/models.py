from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str = Field(min_length=1)
    full_name: str = Field(min_length=1)
    disabled: bool


class UserCreate(UserBase):
    pass


class UserAuth(UserBase):
    pass


class User(UserBase):
    hashed_password: str


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str | None = None
