from datetime import date

from fastapi import Depends
from sqlmodel import Session, select

from magicpost.auth.dependencies import get_password_hash
from magicpost.auth.models import Role, User
from magicpost.auth.schemas import UserCreate
from magicpost.database import get_session


def create_user(user: UserCreate, db: Session = Depends(get_session)):
    db_user = User.model_validate(user)
    db_user.hashed_password = get_password_hash(user.password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def create_super_user(db: Session):
    user = User(
        username="admin",
        role=Role.ADMIN,
        fullname="admin",
        birth=date(2000, 1, 1),
        phone="0123456789",  # TODO: Change to project owner phone
        department_id=1,
    )
    user.hashed_password = get_password_hash("admin")  # TODO load from env

    statement = select(User).where(User.username == user.username)
    db_user = db.exec(statement).one_or_none()

    if not db_user:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    return db_user
