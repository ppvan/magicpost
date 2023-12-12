from fastapi import APIRouter, Depends
from sqlmodel import Session

from magicpost.database import get_session
from magicpost.order.crud import create_hub2hub_order, update_hub2hub_order
from magicpost.order.models import OrderCreate, OrderRead, OrderUpdate

router = APIRouter(prefix="/orders", tags=["Order"])


@router.post("/", response_model=OrderRead)
def create_an_order(order: OrderCreate, db: Session = Depends(get_session)):
    return create_hub2hub_order(order=order, db=db)


@router.patch("/{order_id}", response_model=OrderRead)
def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_session)):
    return update_hub2hub_order(order_id=order_id, order=order, db=db)
