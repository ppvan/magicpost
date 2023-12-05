from sqlmodel import Field
from magicpost.models import MyBaseModel
from typing import Optional
import enum


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
