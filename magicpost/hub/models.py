from typing import TYPE_CHECKING, List, Optional

from pydantic import ConfigDict
from sqlmodel import Field, Relationship

from magicpost.models import MyBaseModel

# This is only for editor support
if TYPE_CHECKING:
    from magicpost.office.models import Office


class HubBase(MyBaseModel):
    name: str
    address: str
    phone: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Bưu điện Chùa Láng",
                "phone": "098123543",
                "address": "23 Chùa Láng, Hà Nội",
            }
        }
    )


class Hub(HubBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    offices: List["Office"] = Relationship(back_populates="hub")


class HubCreate(HubBase):
    pass


class HubRead(HubBase):
    id: int


class HubUpdate(HubBase):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    zipcode: Optional[str] = None
