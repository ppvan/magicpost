from datetime import datetime
from typing import Optional

from pydantic import ConfigDict
from sqlmodel import Field, Relationship, SQLModel

from magicpost.hub.models import Hub
from magicpost.models import PHONE_REGEX, MyBaseModel


class OfficeBase(MyBaseModel):
    name: str = Field(min_length=1)
    address: str = Field(min_length=1)
    phone: str = Field(regex=PHONE_REGEX)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Điểm tập kết Cầu Giấy",
                "phone": "098123543",
                "address": "Cầu Giấy, Hà Nội",
                "hub_id": 1,
            }
        }
    )


class Office(OfficeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    hub_id: int = Field(foreign_key="hub.id")
    hub: Hub = Relationship(back_populates="offices")


class OfficeCreate(OfficeBase):
    hub_id: int = Field(foreign_key="hub.id")
    pass


class OfficeRead(OfficeBase):
    id: int
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class OfficeUpdate(SQLModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None


# class Staff(MyBaseModel):
#     name: str
#     phone: str
#     manage_by: int


# class ServiceStaff(Staff, table=True):
#     pass


# class HubStaff(Staff, table=True):
#     pass
