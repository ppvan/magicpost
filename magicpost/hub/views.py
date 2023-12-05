from fastapi import APIRouter, Depends, Query
from pydantic.types import List
from sqlmodel import Session

from magicpost.database import get_session
from magicpost.hub.crud import create_hub, delete_hub, read_hub, read_hubs, update_hub
from magicpost.hub.models import HubCreate, HubRead, HubUpdate

router = APIRouter()


@router.post("/hubs/", response_model=HubRead)
def create_a_hub(hub: HubCreate, db: Session = Depends(get_session)):
    return create_hub(hub=hub, db=db)


@router.get("/hubs/", response_model=List[HubRead])
def get_hubs(
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    db: Session = Depends(get_session),
):
    return read_hubs(offset=offset, limit=limit, db=db)


@router.get("/hubs/{hub_id}", response_model=HubRead)
def get_a_hub(hub_id: int, db: Session = Depends(get_session)):
    return read_hub(hub_id=hub_id, db=db)


@router.patch("/hubs/{hub_id}", response_model=HubRead)
def update_a_hub(hub_id: int, hub: HubUpdate, db: Session = Depends(get_session)):
    return update_hub(hub_id=hub_id, hub=hub, db=db)


@router.delete("/{hub_id}")
def delete_a_hub(hub_id: int, db: Session = Depends(get_session)):
    return delete_hub(hub_id=hub_id, db=db)
