import enum
from datetime import datetime
from typing import Optional

from pydantic import Field as PydanticField
from sqlmodel import Field, SQLModel

from magicpost.models import PHONE_REGEX, MyBaseModel


class ItemType(str, enum.Enum):
    DOCUMENT = "document"
    GOODS = "goods"


class FailureType(str, enum.Enum):
    RETURN = "return"
    CANCEL = "cancel"
    CALL_SENDER = "call sender"


class ItemBase(MyBaseModel):
    sender_name: str = Field(min_length=1)
    sender_address: str = Field(min_length=1)
    # For some reason, sqlmodel regex does not validate, use pydantic instead
    sender_phone: str = PydanticField(pattern=PHONE_REGEX, min_length=1)
    sender_office_id: int = Field(foreign_key="office.id")

    # Receiver
    receiver_name: str = Field(min_length=1)
    receiver_address: str = Field(min_length=1)
    receiver_phone: str = PydanticField(pattern=PHONE_REGEX, min_length=1)
    receiver_office_id: int = Field(foreign_key="office.id")
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
