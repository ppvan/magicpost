from typing import Optional

from fastapi import Depends, HTTPException, status
from sqlmodel import Session, or_, select

from magicpost.auth.models import Role, User
from magicpost.database import get_session
from magicpost.hub.exceptions import HubNotFound
from magicpost.hub.models import Hub
from magicpost.item.models import Item, ItemStatus
from magicpost.office.models import Office
from magicpost.office.schemas import OfficeCreate, OfficeRead, OfficeUpdate


def create_office(office: OfficeCreate, db: Session = Depends(get_session)):
    hub = db.get(Hub, office.hub_id)
    if not hub:
        raise HubNotFound()

    db_office = Office.model_validate(office)
    db_office.hub = hub
    db.add(db_office)
    db.commit()
    db.refresh(db_office)
    return db_office


def read_offices(offset: int = 0, limit: int = 20, db: Session = Depends(get_session)):
    stmt = (
        select(Office, User)
        .where(Office.id == User.office_id)
        .where(User.role == Role.OFFICE_MANAGER)
        .offset(offset)
        .limit(limit)
    )

    r_offices = []

    for office, user in db.exec(stmt):
        r_office = OfficeRead.model_validate(office.model_dump(exclude={"hub"}))
        r_office.manager = user.username if user else None
        r_offices.append(r_office)

    return r_offices


def read_office(office_id: int, db: Session = Depends(get_session)):
    office = db.get(Office, office_id)
    if not office:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ServiceOffice not found with id: {office_id}",
        )
    return office


def update_office(
    office_id: int, office: OfficeUpdate, db: Session = Depends(get_session)
):
    office_to_update = db.get(Office, office_id)
    if not office_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Office not found with id: {office_id}",
        )

    team_data = office.dict(exclude_unset=True)
    for key, value in team_data.items():
        setattr(office_to_update, key, value)

    db.add(office_to_update)
    db.commit()
    db.refresh(office_to_update)
    return office_to_update


def delete_office(office_id: int, db: Session = Depends(get_session)):
    office = db.get(Office, office_id)
    if not office:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ServiceOffice not found with id: {office_id}",
        )

    db.delete(office)
    db.commit()
    return {"ok": True}


def read_office_items(office_id: int, status: Optional[ItemStatus], db: Session):
    office = db.get(Office, office_id)
    if not office:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Office not found with id: {office_id}",
        )

    if status:
        stmt = select(Item).filter_by(status=status)
    else:
        stmt = select(Item)

    stmt = stmt.filter(
        or_(
            Item.sender_zipcode == office.zipcode,
            Item.receiver_zipcode == office.zipcode,
        )
    )

    return db.exec(stmt)
