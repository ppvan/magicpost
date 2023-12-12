import enum
from datetime import date
from typing import Optional

from sqlmodel import Field

from magicpost.models import MyBaseModel


class Role(str, enum.Enum):
    ADMIN = "admin"
    PRESIDENT = "president"
    HUB_MANAGER = "hub_manager"
    OFFICE_MANAGER = "office_manager"
    HUB_STAFF = "hub_staff"
    OFFICE_STAFF = "office_staff"


class User(MyBaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(min_length=1, sa_column_kwargs={"unique": True})
    hashed_password: str = Field(default=None)
    is_staff: bool = Field(default=False)
    fullname: str = Field(min_length=1)
    birth: date
    phone: str = Field(min_length=1)
    role: Role
    managed_by: Optional[int] = Field(default=None, foreign_key="user.id")
    department_id: int = Field(foreign_key="department.id")
