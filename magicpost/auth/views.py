from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from magicpost.auth.crud import create_user
from magicpost.auth.dependencies import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
)
from magicpost.auth.exceptions import InvalidUsernameOrPasswordException
from magicpost.auth.models import User
from magicpost.auth.schemas import UserCreate, UserRead
from magicpost.database import get_session

router = APIRouter(prefix="/auth", tags=["Auth"])

# TODO: Role validation and protection


@router.post("/signup", response_model=UserRead)
def signup(user: UserCreate, session: Session = Depends(get_session)):
    db_user = create_user(user=user, db=session)

    return db_user


@router.post("/token")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise InvalidUsernameOrPasswordException()
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me")
def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user
