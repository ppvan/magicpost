import enum
from datetime import datetime

from sqlmodel import Field, Relationship

from magicpost.hub.models import Hub
from magicpost.models import MyBaseModel
from magicpost.office.models import Office


class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


class OrderType(str, enum.Enum):
    OFFICE2HUB = "OFFICE2HUB"
    HUB2HUB = "HUB2HUB"
    HUB2OFFICE = "HUB2OFFICE"


class OrderBase(MyBaseModel):
    status: OrderStatus = Field(default=OrderStatus.PENDING)


class Order(OrderBase):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Hub2HubOrder(Order, table=True):
    """Order from Hub to Hub"""

    sender_id: int = Field(foreign_key="hub.id")
    receiver_id: int = Field(foreign_key="hub.id")

    sender: Hub = Relationship()
    receiver: Hub = Relationship()


class Hub2HubOrderCreate(OrderBase):
    sender_id: int = Field(foreign_key="hub.id")
    receiver_id: int = Field(foreign_key="hub.id")


# /hub2hub-orders/?sender_id=1
# /orders/?type=hub2hub
# {
#     "id": 1,
#     "type": "hub2hub",
#     "sender_id": 1,
#     "receiver_id": 2
# }
# class Office2HubOrder(Order, table=True):
#     """Order going from Office to Hub"""

#     sender_id: int = Field(foreign_key="office.id")
#     receiver_id: int = Field(foreign_key="hub.id")

#     sender: Office = Relationship(back_populates="orders")
#     receiver: Hub = Relationship(back_populates="orders")


# class Hub2OfficeOrder(Order, table=True):
#     """Order going from Hub to Office"""

#     sender_id: int = Field(foreign_key="hub.id")
#     receiver_id: int = Field(foreign_key="office.id")

#     sender: Hub = Relationship(back_populates="orders")
#     receiver: Office = Relationship(back_populates="orders")


# class Hub2HubOrderCreate(OrderBase):
#     sender_id: int = Field(foreign_key="hub.id")
#     receiver_id: int = Field(foreign_key="hub.id")


# class Office2HubOrderCreate(OrderBase):
#     sender_id: int = Field(foreign_key="office.id")
#     receiver_id: int = Field(foreign_key="hub.id")


# class Hub2OfficeOrderCreate(OrderBase):
#     sender_id: int = Field(foreign_key="hub.id")
#     receiver_id: int = Field(foreign_key="office.id")


class OrderUpdate(MyBaseModel):
    status: OrderStatus
