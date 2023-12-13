from sqlmodel import Session

from magicpost.item.exceptions import ItemNotFound
from magicpost.item.models import Item, ItemCreate
from magicpost.item.schemas import ItemDetail, ItemPath
from magicpost.office.exceptions import OfficeNotFound
from magicpost.office.models import Office


def valid_item_id(db: Session, item_id: int):
    item = db.get(Item, item_id)
    if not item:
        raise ItemNotFound()

    sender_office = db.get(Office, item.sender_office_id)
    receiver_office = db.get(Office, item.receiver_office_id)

    if not sender_office or not receiver_office:
        raise OfficeNotFound()

    return item


def read_item_detail(db: Session, item_id: int):
    item = db.get(Item, item_id)
    if not item:
        raise ItemNotFound()

    sender_office = db.get(Office, item.sender_office_id)
    receiver_office = db.get(Office, item.receiver_office_id)

    if not sender_office or not receiver_office:
        raise OfficeNotFound()

    path = ItemPath(
        start_office=sender_office,
        end_office=receiver_office,
        start_hub=sender_office.hub,
        end_hub=receiver_office.hub,
    )

    return ItemDetail(item=item, path=path)


def create_item(db: Session, item: ItemCreate):
    db_item = Item.model_validate(item)

    sender_office = db.get(Office, db_item.sender_office_id)
    receiver_office = db.get(Office, db_item.receiver_office_id)

    if not sender_office or not receiver_office:
        raise OfficeNotFound()

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def read_items(db: Session, offset: int = 0, limit: int = 100):
    return db.query(Item).offset(offset).limit(limit).all()


def read_item(db: Session, item_id: int):
    item = db.get(Item, item_id)
    if not item:
        raise ItemNotFound()
    return item


def delete_item(db: Session, item_id: int):
    item = db.get(Item, item_id)
    if not item:
        raise ItemNotFound()

    db.delete(item)
    db.commit()

    return {"ok": True}
