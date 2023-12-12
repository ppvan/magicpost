from fastapi import APIRouter, Depends
from sqlmodel import Session

from magicpost.database import get_session
from magicpost.order.crud import create_hub2hub_order, update_hub2hub_order
from magicpost.order.models import OrderCreate, OrderRead, OrderUpdate

hub2hub_order = APIRouter(prefix="/hub-to-hub", tags=["Hub to Hub"])
office2hub_order = APIRouter(prefix="/office-to-hub", tags=["Office to Hub"])
hub2office_order = APIRouter(prefix="/hub-to-office", tags=["Hub to Office"])

router = APIRouter(prefix="/orders", tags=["Order"])
router.include_router(hub2hub_order)
router.include_router(office2hub_order)
router.include_router(hub2office_order)


@hub2hub_order.post("/", response_model=OrderRead)
def create_an_order(order: OrderCreate, db: Session = Depends(get_session)):
    return create_hub2hub_order(order=order, db=db)


@hub2hub_order.patch("/{order_id}", response_model=OrderRead)
def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_session)):
    return update_hub2hub_order(order_id=order_id, order=order, db=db)
