from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

from magicpost.database import get_session
from magicpost.office.models import Office, OfficeCreate, OfficeUpdate


def create_office(office: OfficeCreate, db: Session = Depends(get_session)):
    db_office = Office.from_orm(office)
    db.add(db_office)
    db.commit()
    db.refresh(db_office)
    return db_office


def read_offices(offset: int = 0, limit: int = 20, db: Session = Depends(get_session)):
    offices = db.exec(select(Office).offset(offset).limit(limit)).all()
    return offices


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
