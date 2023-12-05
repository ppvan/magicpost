from typing import Optional
import enum

from sqlmodel import Field, SQLModel
from datetime import datetime


class MyBaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ItemType(str, enum.Enum):
    DOCUMENT = "DOCUMENT"
    GOODS = "GOODS"


class FailureType(str, enum.Enum):
    RETURN = "RETURN"
    CANCEL = "CANCEL"
    CALL_SENDER = "CALL_SENDER"


class Item(MyBaseModel, table=True):
    # Sender
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
    additional_cod: int
    # Delivery Fees
    weight: float
    base_fee: int
    additional_fee: int
    type: ItemType
    notes: Optional[str] = Field(default="")


class OrderType(str, enum.Enum):
    SERVICE_TO_HUB = "SERVICE_TO_HUB"
    HUH_TO_HUB = "HUH_TO_HUB"
    HUH_TO_SERVICE = "HUH_TO_SERVICE"


class Order(MyBaseModel, table=True):
    Item_id: int
    state: str
    type: OrderType
    sender_zipcode: str
    receiver_zipcode: str


class ServiceOffice(MyBaseModel, table=True):
    name: str
    address: str
    phone: str
    zipcode: str


class HubOffice(MyBaseModel, table=True):
    name: str
    address: str
    phone: str
    zipcode: str


class Staff(MyBaseModel):
    name: str
    phone: str
    manage_by: int


class ServiceStaff(Staff, table=True):
    pass


class HubStaff(Staff, table=True):
    pass
