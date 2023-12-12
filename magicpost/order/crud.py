from fastapi import Depends
from sqlmodel import Session

from magicpost.database import get_session
from magicpost.hub.models import Hub
from magicpost.office.models import Office
from magicpost.order.exceptions import OrderNotFound
from magicpost.order.models import (
    Hub2HubOrder,
    Hub2OfficeOrder,
    Office2HubOrder,
    OrderCreate,
    OrderUpdate,
)


def create_hub2hub_order(order: OrderCreate, db: Session = Depends(get_session)):
    db_order = Hub2HubOrder.model_validate(order)

    sender = db.get(Hub, order.sender_id)
    receiver = db.get(Hub, order.receiver_id)

    if not sender or not receiver:
        raise OrderNotFound()

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return db_order


def create_office2hub_order(order: OrderCreate, db: Session = Depends(get_session)):
    db_order = Office2HubOrder.model_validate(order)

    sender = db.get(Office, order.sender_id)
    receiver = db.get(Hub, order.receiver_id)

    if not sender or not receiver:
        raise OrderNotFound()

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return db_order


def create_hub2office_order(order: OrderCreate, db: Session = Depends(get_session)):
    db_order = Hub2OfficeOrder.model_validate(order)

    sender = db.get(Hub, order.sender_id)
    receiver = db.get(Office, order.receiver_id)

    if not sender or not receiver:
        raise OrderNotFound()

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return db_order


def read_hub2hub_order(order_id: int, db: Session = Depends(get_session)):
    order = db.get(Hub2HubOrder, order_id)
    if not order:
        raise OrderNotFound()
    return order


def update_hub2hub_order(
    order_id: int, order: OrderUpdate, db: Session = Depends(get_session)
):
    order_to_update = db.get(Hub2HubOrder, order_id)
    if not order_to_update:
        raise OrderNotFound()

    order_data = order.dict(exclude_unset=True)
    for key, value in order_data.items():
        setattr(order_to_update, key, value)

    db.add(order_to_update)
    db.commit()
    db.refresh(order_to_update)
    return order_to_update


def delete_hub2hub_order(order_id: int, db: Session = Depends(get_session)):
    order = db.get(Hub2HubOrder, order_id)
    if not order:
        raise OrderNotFound()

    db.delete(order)
    db.commit()
    return {"ok": True}
