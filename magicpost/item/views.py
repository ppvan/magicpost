from typing import List

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from magicpost.database import get_session
from magicpost.item.crud import create_item, delete_item, read_item, read_items
from magicpost.item.models import ItemCreate, ItemRead

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("", response_model=List[ItemRead])
def get_items(
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    db: Session = Depends(get_session),
):
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
