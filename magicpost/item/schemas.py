from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, NonNegativeFloat, NonNegativeInt

from magicpost.item.models import ItemStatus, ItemType
from magicpost.models import PHONE_REGEX, ZIPCODE_REGEX


class ItemCreate(BaseModel):
    """This is a pydantic model(schemas), not to confuse with SQLModel."""

    sender_name: str = Field(min_length=1)
    sender_address: str = Field(min_length=1)
    sender_phone: str = Field(pattern=PHONE_REGEX, min_length=1, max_length=10)
    sender_zipcode: str = Field(pattern=ZIPCODE_REGEX, min_length=1, max_length=5)
    # Receiver
    receiver_name: str = Field(min_length=1)
    receiver_address: str = Field(min_length=1)
    receiver_phone: str = Field(pattern=PHONE_REGEX, min_length=1, max_length=10)
    receiver_zipcode: str = Field(min_length=1)
    # Cash on delivery
    cod: NonNegativeInt
    # Delivery Fees
    weight: NonNegativeFloat
    fee: NonNegativeInt

    type: ItemType
    status: ItemStatus = Field(default=ItemStatus.PENDING)
    notes: Optional[str] = Field(default="")


class ItemRead(BaseModel):
    id: int
    sender_name: str = Field(min_length=1)
    sender_address: str = Field(min_length=1)
    sender_phone: str = Field(pattern=PHONE_REGEX, min_length=1, max_length=10)
    sender_zipcode: str = Field(pattern=ZIPCODE_REGEX, min_length=1, max_length=5)
    # Receiver
    receiver_name: str = Field(min_length=1)
    receiver_address: str = Field(min_length=1)
    receiver_phone: str = Field(pattern=PHONE_REGEX, min_length=1, max_length=10)
    receiver_zipcode: str = Field(min_length=1)
    # Cash on delivery
    cod: int = NonNegativeInt
    # Delivery Fees
    weight: float = NonNegativeFloat
    fee: int = NonNegativeInt

    type: ItemType
    status: ItemStatus = Field(default=ItemStatus.PENDING)
    notes: Optional[str] = Field(default="")
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class OrderCreate(BaseModel):
    """Use to move items between hub and office"""

    status: Optional[ItemStatus] = Field(default=ItemStatus.ON_DELIVERY)
    items: List[ItemRead]
    zipcode: str = Field(pattern=ZIPCODE_REGEX, min_length=1, max_length=5)


class OrderUpdate(BaseModel):
    items: List[ItemRead]
    zipcode: str = Field(pattern=ZIPCODE_REGEX, min_length=1, max_length=5)
