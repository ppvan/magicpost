from fastapi import Depends
from sqlmodel import Session

from magicpost.auth.dependencies import get_password_hash
from magicpost.auth.models import User
from magicpost.auth.schemas import UserCreate
from magicpost.database import get_session


def create_user(user: UserCreate, db: Session = Depends(get_session)):
    db_user = User.model_validate(user)
    db_user.hashed_password = get_password_hash(user.password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
