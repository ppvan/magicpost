from typing import Optional

from sqlmodel import Session, select

from magicpost.item.exceptions import ItemNotFound
from magicpost.item.models import Item, ItemPath, ItemPathState, ItemStatus
from magicpost.item.schemas import ItemCreate, OrderCreate, OrderUpdate
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
    pass


def create_item(db: Session, item: ItemCreate):
    db_item = Item.model_validate(item)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def read_items_stats(db: Session, zipcode: str = None):
    if not zipcode:
        return {"count": db.query(Item).count()}
        pass

    pass


def move_items(db: Session, order: OrderCreate):
    """Tạo đơn chuyển hàng đến zipcode xác định"""
    db_items = []

    for item in order.items:
        if order.status:
            item.status = order.status
        db_item = Item.model_validate(item)
        path = ItemPath(db_item, order.zipcode)
        db.add(db_item)
        db.add(path)
        db_items.append(db_item)

    db.commit()

    return db_items


def confirm_items(db: Session, order: OrderUpdate):
    for item in order.items:
        db_item = valid_item_id(db, item.id)

        stmt = select(ItemPath).filter_by(
            item_id=db_item.id, zipcode=order.zipcode, state=ItemPathState.PENDDING
        )
        path = db.exec(stmt).one()
        path.state = ItemPathState.DONE

        db.add(path)

    db.commit()

    return {"ok": True}


def read_items(
    db: Session,
    status: Optional[ItemStatus] = None,
    sender_zipcode: Optional[str] = None,
    receiver_zipcode: Optional[str] = None,
    offset: int = 0,
    limit: int = 100,
):
    filter_fields = {}
    if status:
        filter_fields["status"] = status
    if sender_zipcode:
        filter_fields["sender_zipcode"] = sender_zipcode
    if receiver_zipcode:
        filter_fields["receiver_zipcode"] = receiver_zipcode

    stmt = select(Item).filter_by(**filter_fields)

    return db.exec(stmt).offset(offset).limit(limit).all()


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


def read_item_paths(db: Session, item_id: int):
    stmt = (
        select(ItemPath)
        .where(ItemPath.item_id == item_id)
        .order_by(ItemPath.updated_at.desc())
    )
    return db.exec(stmt).all()
