from fastapi import APIRouter, Depends, Query
from pydantic.types import List
from sqlmodel import Session

from magicpost.auth.dependencies import president_required
from magicpost.database import get_session
from magicpost.hub.crud import create_hub, delete_hub, read_hub, read_hubs, update_hub
from magicpost.hub.schemas import HubCreate, HubRead, HubUpdate

router = APIRouter(prefix="/api/v1/hubs", tags=["Hubs"])

protected_deps = [Depends(president_required)]


@router.post("/", response_model=HubRead, dependencies=protected_deps)
def create_a_hub(hub: HubCreate, db: Session = Depends(get_session)):
    return create_hub(hub=hub, db=db)


@router.get("/", response_model=List[HubRead])
def get_hubs(
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    db: Session = Depends(get_session),
):
    return read_hubs(offset=offset, limit=limit, db=db)


@router.get("/{hub_id}", response_model=HubRead)
def get_a_hub(hub_id: int, db: Session = Depends(get_session)):
    return read_hub(hub_id=hub_id, db=db)


@router.patch("/{hub_id}", response_model=HubRead, dependencies=protected_deps)
def update_a_hub(hub_id: int, hub: HubUpdate, db: Session = Depends(get_session)):
    return update_hub(hub_id=hub_id, hub=hub, db=db)


@router.delete("/{hub_id}", dependencies=protected_deps)
def delete_a_hub(hub_id: int, db: Session = Depends(get_session)):
    return delete_hub(hub_id=hub_id, db=db)
