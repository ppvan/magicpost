import enum
from datetime import datetime
from typing import Optional

from pydantic import NonNegativeFloat, NonNegativeInt
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
    cod: NonNegativeInt
    additional_cod: NonNegativeInt
    # Delivery Fees
    weight: NonNegativeFloat
    base_fee: NonNegativeInt
    additional_fee: NonNegativeInt
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
