import enum
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from magicpost.models import PHONE_REGEX, MyBaseModel


class ItemType(str, enum.Enum):
    DOCUMENT = "DOCUMENT"
    GOODS = "GOODS"


class FailureType(str, enum.Enum):
    RETURN = "RETURN"
    CANCEL = "CANCEL"
    CALL_SENDER = "CALL_SENDER"


class ItemBase(MyBaseModel):
    sender_name: str = Field(min_length=1)
    sender_address: str = Field(min_length=1)
    sender_phone: str = Field(regex=PHONE_REGEX)

    # Receiver
    receiver_name: str = Field(min_length=1)
    receiver_address: str = Field(min_length=1)
    receiver_phone: str = Field(regex=PHONE_REGEX)
    # Cash on delivery
    cod: int = Field(default=0, ge=0)
    additional_cod: int = Field(default=0, ge=0)
    # Delivery Fees
    weight: float = Field(default=0, ge=0)
    base_fee: int = Field(default=0, ge=0)
    additional_fee: int = Field(default=0, ge=0)
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
