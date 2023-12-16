from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from pydantic import ConfigDict
from sqlmodel import Field, Relationship

from magicpost.models import MyBaseModel

# This is only for editor support
if TYPE_CHECKING:
    from magicpost.office.models import Office


class Hub(MyBaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str
    address: str
    phone: str
    zipcode: str
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    offices: List["Office"] = Relationship(back_populates="hub")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Bưu điện Chùa Láng",
                "phone": "098123543",
                "zipcode": "10000",
                "address": "23 Chùa Láng, Hà Nội",
            }
        }
    )
