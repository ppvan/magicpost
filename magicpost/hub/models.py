from typing import Optional

from sqlmodel import Field, SQLModel

from magicpost.models import MyBaseModel


class HubBase(SQLModel):
    name: str
    address: str
    phone: str

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Bưu điện Chùa Láng",
                "phone": "098123543",
                "address": "23 Chùa Láng, Hà Nội",
            }
        }


class Hub(MyBaseModel, HubBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class HubCreate(HubBase):
    pass


class HubRead(MyBaseModel, HubBase):
    id: int


class HubUpdate(HubBase):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    zipcode: Optional[str] = None
