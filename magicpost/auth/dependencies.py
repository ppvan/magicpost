from datetime import datetime, timedelta
from typing import Annotated, Tuple

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session

from magicpost.auth.exceptions import (
    AuthorizationException,
    InactiveUserException,
    InvalidCredentialsException,
)
from magicpost.auth.models import Role, User
from magicpost.auth.schemas import TokenData
from magicpost.database import get_session

# TODO: Change this
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(session: Session, username: str):
    return session.query(User).filter(User.username == username).one()


def authenticate_user(
    session: Annotated[Session, Depends(get_session)], username: str, password: str
):
    user = get_user(session, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def parse_jwt_data(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = InvalidCredentialsException()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

        return token_data
    except JWTError:
        raise credentials_exception


def get_current_user(
    token_data: Annotated[TokenData, Depends(parse_jwt_data)],
    session: Annotated[Session, Depends(get_session)],
):
    user = get_user(session, username=token_data.username)
    if user is None:
        raise InvalidCredentialsException()
    return user


def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if not current_user.is_staff:
        raise InactiveUserException()
    return current_user


def login_required(allow_roles: Tuple[Role]):
    def wrapper(current_user: Annotated[User, Depends(get_current_active_user)]):
        if current_user.role not in allow_roles:
            raise AuthorizationException()

        return current_user

    return wrapper


def president_required(current_user: Annotated[User, Depends(get_current_active_user)]):
    if current_user.role not in (Role.ADMIN, Role.PRESIDENT):
        raise AuthorizationException()

    return current_user
