from fastapi import APIRouter, Depends, Query
from pydantic.types import List
from sqlmodel import Session

from magicpost.database import get_session
from magicpost.order.crud import (
    create_hub2hub_order,
    delete_hub2hub_order,
    read_hub2hub_order,
    update_hub2hub_order,
)
from magicpost.order.exceptions import OrderNotFound
from magicpost.order.models import (
    Hub2HubOrder,
    OrderCreate,
    OrderRead,
    OrderType,
    OrderUpdate,
)

router = APIRouter(prefix="/orders", tags=["Order"])


@router.post("/", response_model=OrderRead)
def create_an_order(
    order: OrderCreate, type: OrderType, db: Session = Depends(get_session)
):
    match type:
        case OrderType.HUB2HUB:
            return create_hub2hub_order(order=order, db=db)
        case _:
            raise NotImplementedError

    return create_hub2hub_order(order=order, db=db)


@router.patch("/", response_model=OrderRead)
def update_order(
    order_id: int,
    type: OrderType,
    order: OrderUpdate,
    db: Session = Depends(get_session),
):
    order_to_update = None
    match type:
        case OrderType.HUB2HUB:
            order_to_update = db.get(Hub2HubOrder, order_id)
        case _:
            raise NotImplementedError

    if not order_to_update:
        raise OrderNotFound()

    order_data = order.dict(exclude_unset=True)
    for key, value in order_data.items():
        setattr(order_to_update, key, value)

    db.add(order_to_update)
    db.commit()
    db.refresh(order_to_update)
    return order_to_update
