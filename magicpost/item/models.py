import enum
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from magicpost.models import MyBaseModel


class ItemType(str, enum.Enum):
    DOCUMENT = "DOCUMENT"
    GOODS = "GOODS"


class FailureType(str, enum.Enum):
    RETURN = "RETURN"
    CANCEL = "CANCEL"
    CALL_SENDER = "CALL_SENDER"


class ItemBase(MyBaseModel):
    sender_name: str
    sender_address: str
    sender_phone: str

    # Receiver
    receiver_name: str
    receiver_address: str
    receiver_phone: str
    # Cash on delivery
    cod: int
    additional_cod: int
    # Delivery Fees
    weight: float
    base_fee: int
    additional_fee: int
    type: ItemType
    notes: Optional[str] = Field(default="")


class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ItemCreate(ItemBase):
    pass


class ItemRead(ItemBase):
    id: int
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ItemUpdate(SQLModel):
    """Not sure if this is needed"""

    pass
