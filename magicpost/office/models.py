from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship

from magicpost.hub.models import Hub
from magicpost.models import MyBaseModel


class Office(MyBaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    address: str
    phone: str
    zipcode: str
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    hub_id: int = Field(foreign_key="hub.id")
    hub: Hub = Relationship(back_populates="offices")
