from sqlmodel import SQLModel

from magicpost.hub.models import HubRead
from magicpost.item.models import ItemRead
from magicpost.office.models import OfficeRead


class ItemPath(SQLModel):
    start_office: OfficeRead
    end_office: OfficeRead

    start_hub: HubRead
    end_hub: HubRead


class ItemDetail(SQLModel):
    item: ItemRead
    path: ItemPath
