import enum
from datetime import datetime
from typing import List, Optional

# For some reason, sqlmodel regex does not validate, use pydantic instead
from pydantic import Field as PydanticField
from sqlmodel import Field, Relationship, SQLModel

from magicpost.models import PHONE_REGEX, ZIPCODE_REGEX, MyBaseModel


class ItemType(str, enum.Enum):
    DOCUMENT = "document"
    GOODS = "goods"


class ItemStatus(str, enum.Enum):
    PENDING = "pending"
    ON_DELIVERY = "on delivery"
    SUCCESS = "success"
    FAILED = "failed"


class ItemPathState(str, enum.Enum):
    PENDDING = "pending"
    DONE = "done"


class ItemBase(MyBaseModel):
    sender_name: str = Field(min_length=1)
    sender_address: str = Field(min_length=1)
    sender_phone: str = PydanticField(pattern=PHONE_REGEX)
    sender_zipcode: str = PydanticField(pattern=ZIPCODE_REGEX)
    # Receiver
    receiver_name: str = Field(min_length=1)
    receiver_address: str = Field(min_length=1)
    receiver_phone: str = PydanticField(pattern=PHONE_REGEX, min_length=1)
    server_zipcode: str = Field(min_length=1)
    # Cash on delivery
    cod: int = Field(default=0, ge=0)
    # Delivery Fees
    weight: float = Field(default=0, ge=0)
    fee: int = Field(default=0, ge=0)

    type: ItemType
    status: ItemStatus = Field(default=ItemStatus.PENDING)
    notes: Optional[str] = Field(default="")


class Item(MyBaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sender_name: str
    sender_address: str
    sender_phone: str
    sender_zipcode: str
    # Receiver
    receiver_name: str
    receiver_address: str
    receiver_phone: str
    receiver_zipcode: str
    # Cash on delivery
    cod: int
    # Delivery Fees
    weight: float
    fee: int

    type: ItemType
    status: ItemStatus = Field(default=ItemStatus.PENDING)
    notes: Optional[str] = Field(default="")

    paths: List["ItemPath"] = Relationship(back_populates="item")

    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ItemPath(MyBaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="item.id")
    item: Item = Relationship(back_populates="paths")
    zipcode: str = Field(min_length=1)
    state: ItemPathState = Field(default=ItemPathState.PENDDING)
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ItemRead(ItemBase):
    id: int
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ItemUpdate(SQLModel):
    status: ItemStatus
