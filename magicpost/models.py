import enum
from datetime import date

from sqlmodel import Field, SQLModel


class MyBaseModel(SQLModel):
    pass


PHONE_REGEX = r"^(03|05|07|08|09|01[2|6|8|9])+([0-9]{8})$"


class Department(MyBaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(min_length=1)
    address: str = Field(min_length=1)
    phone: str = Field(regex=PHONE_REGEX)
    manager_id: int = Field(foreign_key="user.id")
