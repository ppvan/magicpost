from typing import Optional

from sqlmodel import Field, SQLModel

from magicpost.models import MyBaseModel


class OfficeBase(SQLModel, table=True):
    name: str
    address: str
    phone: str


class ServiceOffice(MyBaseModel, OfficeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Điểm tập kết Cầu Giấy",
                "phone": "098123543",
                "address": "Cầu Giấy, Hà Nội",
            }
        }


class ServiceOfficeCreate(OfficeBase):
    pass


class ServiceOfficeUpdate(SQLModel):
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
