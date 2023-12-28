from typing import Optional

from sqlmodel import Session, select

from magicpost.hub.models import Hub
from magicpost.item.exceptions import ItemNotFound, NoNextZipcodeFound
from magicpost.item.models import Item, ItemPath, ItemPathState, ItemStatus
from magicpost.item.schemas import ItemCreate, ItemUpdate, OrderCreate, OrderUpdate
from magicpost.office.exceptions import OfficeNotFound
from magicpost.office.models import Office
from magicpost.utils import find_next, is_valid_zipcode


def valid_item_id(db: Session, item_id: int):
    item = db.get(Item, item_id)
    if not item:
        raise ItemNotFound()

    if not all(
        [is_valid_zipcode(x) for x in (item.sender_zipcode, item.receiver_zipcode)]
    ):
        raise OfficeNotFound()

    return item


def read_item_detail(db: Session, item_id: int):
    pass


def create_item(db: Session, item: ItemCreate):
    db_item = Item.model_validate(item)
    item_path = ItemPath(
        item=db_item, state=ItemPathState.DONE, zipcode=item.sender_zipcode
    )
    db.add(db_item)
    db.add(item_path)
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
        db_item = db.get(Item, item.id)
        if order.status:
            db_item.status = order.status
        path = ItemPath(item=db_item, zipcode=order.zipcode)
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

    stmt = select(Item).filter_by(**filter_fields).offset(offset).limit(limit)

    return db.exec(stmt).all()


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


def read_items_at_zipcode(db: Session, zipcode: str):
    stmt = (
        select(Item)
        .join(ItemPath)
        .where(ItemPath.item_id == Item.id)
        .where(ItemPath.state == ItemPathState.DONE)
    )
    results = db.exec(stmt)

    return results.all()


def read_items_unconfirmed(db: Session, zipcode: str):
    if zipcode:
        stmt = (
            select(Item)
            .join(ItemPath)
            .where(ItemPath.item_id == Item.id)
            .where(ItemPath.zipcode == zipcode)
            .where(ItemPath.state == ItemPathState.PENDDING)
        )
    else:
        stmt = (
            select(Item)
            .join(ItemPath)
            .where(ItemPath.item_id == Item.id)
            .where(ItemPath.state == ItemPathState.PENDDING)
        )
    results = db.exec(stmt)

    return results.all()


def update_item_status(db: Session, item_id: int, item: ItemUpdate):
    db_item = valid_item_id(db, item_id)
    db_item.status = item.status
    db.add(db_item)
    db.commit()

    return db_item


def read_next_zipcode(db: Session, item_id: int, zipcode: str):
    db_item = valid_item_id(db, item_id)
    stmt1 = select(Office).where(Office.zipcode == db_item.sender_zipcode)
    office1: Office = db.exec(stmt1).one()
    hub1: Hub = office1.hub

    stmt2 = select(Office).where(Office.zipcode == db_item.receiver_zipcode)
    office2: Office = db.exec(stmt2).one()
    hub2: Hub = office2.hub

    if hub1 == hub2:
        zipcodes = [office1.zipcode, hub1.zipcode, office2.zipcode]
    else:
        zipcodes = [office1.zipcode, hub1.zipcode, hub2.zipcode, office2.zipcode]

    next_zipcode = find_next(zipcodes, zipcode)

    if next_zipcode:
        return next_zipcode
    else:
        raise NoNextZipcodeFound()
