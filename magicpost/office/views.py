from fastapi import APIRouter, Depends, Query
from pydantic.types import List
from sqlmodel import Session

from magicpost.auth.dependencies import president_required
from magicpost.database import get_session
from magicpost.office.crud import (
    create_office,
    delete_office,
    read_office,
    read_offices,
    update_office,
)
from magicpost.office.models import OfficeCreate, OfficeRead, OfficeUpdate

router = APIRouter(prefix="/offices", tags=["Offices"])
president_required_deps = [Depends(president_required)]


@router.post("/", response_model=OfficeRead, dependencies=president_required_deps)
def create_an_office(office: OfficeCreate, db: Session = Depends(get_session)):
    return create_office(office=office, db=db)


@router.get("/", response_model=List[OfficeRead])
def get_offices(
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    db: Session = Depends(get_session),
):
    return read_offices(offset=offset, limit=limit, db=db)


@router.get("/{office_id}", response_model=OfficeRead)
def get_a_office(office_id: int, db: Session = Depends(get_session)):
    return read_office(office_id=office_id, db=db)


@router.patch(
    "/{office_id}", response_model=OfficeRead, dependencies=president_required_deps
)
def update_a_office(
    office_id: int, hub: OfficeUpdate, db: Session = Depends(get_session)
):
    return update_office(office_id=office_id, hub=hub, db=db)


@router.delete("/{office_id}", dependencies=president_required_deps)
def delete_a_office(office_id: int, db: Session = Depends(get_session)):
    return delete_office(office_id=office_id, db=db)
