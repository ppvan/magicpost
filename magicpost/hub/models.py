from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from pydantic import ConfigDict
from sqlmodel import Field, Relationship

from magicpost.models import PHONE_REGEX, MyBaseModel

# This is only for editor support
if TYPE_CHECKING:
    from magicpost.office.models import Office


class HubBase(MyBaseModel):
    name: str = Field(min_length=1)
    address: str = Field(min_length=1)
    phone: str = Field(regex=PHONE_REGEX)

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
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default_factory=datetime.utcnow)

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
