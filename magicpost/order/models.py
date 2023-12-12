import enum
from datetime import datetime

from sqlmodel import Field, Relationship

from magicpost.hub.models import Hub
from magicpost.models import MyBaseModel
from magicpost.office.models import Office

# from magicpost.office.models import Office


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"


class OrderType(str, enum.Enum):
    OFFICE2HUB = "office2hub"
    HUB2HUB = "hub2hub"
    HUB2OFFICE = "hub2office"


class OrderBase(MyBaseModel):
    status: OrderStatus = Field(default=OrderStatus.PENDING)


class Order(OrderBase):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # items: List["Item"] = Relationship(back_populates="order")


class Hub2HubOrder(Order, table=True):
    """Order from Hub to Hub"""

    sender_id: int = Field(foreign_key="hub.id")
    receiver_id: int = Field(foreign_key="hub.id")

    sender: Hub = Relationship(
        sa_relationship_kwargs=dict(foreign_keys="[Hub2HubOrder.sender_id]")
    )
    receiver: Hub = Relationship(
        sa_relationship_kwargs=dict(foreign_keys="[Hub2HubOrder.receiver_id]")
    )


class Office2HubOrder(Order, table=True):
    """Order from Office to Hub"""

    sender_id: int = Field(foreign_key="office.id")
    receiver_id: int = Field(foreign_key="hub.id")

    sender: Office = Relationship(
        sa_relationship_kwargs=dict(foreign_keys="[Office2HubOrder.sender_id]")
    )
    receiver: Hub = Relationship(
        sa_relationship_kwargs=dict(foreign_keys="[Office2HubOrder.receiver_id]")
    )


class Hub2OfficeOrder(Order, table=True):
    """Order from Hub to Office"""

    sender_id: int = Field(foreign_key="hub.id")
    receiver_id: int = Field(foreign_key="office.id")

    sender: Hub = Relationship(
        sa_relationship_kwargs=dict(foreign_keys="[Hub2OfficeOrder.sender_id]")
    )
    receiver: Office = Relationship(
        sa_relationship_kwargs=dict(foreign_keys="[Hub2OfficeOrder.receiver_id]")
    )


class OrderRead(OrderBase):
    id: int
    sender_id: int
    receiver_id: int
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # items: Optional[List["ItemRead"]]


class OrderCreate(OrderBase):
    sender_id: int
    receiver_id: int


# /hub2hub-orders/?sender_id=1
# /orders/?type=hub2hub
# {
#     "id": 1,
#     "type": "hub2hub",
#     "sender_id": 1,
#     "receiver_id": 2,
#     "status": "pending",
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
