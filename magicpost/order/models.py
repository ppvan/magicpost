import enum

from magicpost.models import MyBaseModel


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
