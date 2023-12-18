from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from magicpost.database import get_session
from magicpost.item.crud import (
    confirm_items,
    create_item,
    delete_item,
    move_items,
    read_item,
    read_item_paths,
    read_items,
)
from magicpost.item.models import ItemStatus
from magicpost.item.schemas import (
    ItemCreate,
    ItemPathRead,
    ItemRead,
    OrderCreate,
    OrderUpdate,
)

router = APIRouter(prefix="/api/v1/items", tags=["Items"])


@router.get("", response_model=List[ItemRead])
def get_items(
    status: Optional[ItemStatus] = None,
    sender_zipcode: Optional[str] = None,
    receiver_zipcode: Optional[str] = None,
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    db: Session = Depends(get_session),
):
    """Trả về tất cả đơn hàng, có thể page offset và limit, lọc để thống kê."""

    return read_items(db=db, offset=offset, limit=limit)


@router.post("/", response_model=ItemRead)
def create_a_item(
    item: ItemCreate,
    db: Session = Depends(get_session),
):
    return create_item(db=db, item=item)


@router.get("/{item_id}", response_model=ItemRead)
def get_a_item(item_id: int, db: Session = Depends(get_session)):
    return read_item(db=db, item_id=item_id)


@router.delete("/{item_id}")
def delete_a_item(item_id: int, db: Session = Depends(get_session)):
    return delete_item(db=db, item_id=item_id)


@router.get("{item_id}/paths", response_model=List[ItemPathRead])
def get_items_path(item_id: str, db: Session = Depends(get_session)):
    """Tiến trình hiện tại của đơn hàng, sắp xếp theo thời gian"""
    return read_item_paths(db=db, item_id=item_id)


@router.post("/move")
def move_items_to_another_department(
    order: OrderCreate, db: Session = Depends(get_session)
):
    """Chuyển các đơn hàng đến zipcode xác định, có thể là hub hoặc office"""

    return move_items(db=db, order=order)


@router.post("/confirm")
def confirm_items_arrived(order: OrderUpdate, db: Session = Depends(get_session)):
    """Xác nhận các đơn hàng đã đến nơi"""
    return confirm_items(db=db, order=order)
