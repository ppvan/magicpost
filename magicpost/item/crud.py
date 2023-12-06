from sqlmodel import Session

from magicpost.item.exceptions import ItemNotFound
from magicpost.item.models import Item, ItemCreate


def valid_item_id(db: Session, item_id: int):
    item = db.get(Item, item_id)
    if not item:
        raise ItemNotFound()
    return item


def create_item(db: Session, item: ItemCreate):
    db_item = Item(**item.model_dump())
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
