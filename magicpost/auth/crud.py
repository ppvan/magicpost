from datetime import date

from sqlmodel import Session, select

from magicpost.auth.dependencies import get_password_hash
from magicpost.auth.exceptions import AuthorizationException, InvalidRoleUserCreation
from magicpost.auth.models import Role, User
from magicpost.auth.schemas import UserCreate
from magicpost.config import get_settings


def read_users(role: Role, offset: int, limit: int, db: Session):
    stmt = select(User).order_by(User.id.desc()).offset(offset).limit(limit)
    if role:
        stmt = stmt.where(User.role == role)
    return db.exec(stmt).all()


def create_user(user: UserCreate, authorized_user: User, db: Session):
    db_user = None

    match user.role:
        case Role.PRESIDENT:
            db_user = create_president(user, authorized_user)
        case Role.HUB_MANAGER:
            db_user = create_hub_manager(user, authorized_user)
        case Role.OFFICE_MANAGER:
            db_user = create_office_manager(user, authorized_user)
        case Role.HUB_STAFF:
            db_user = create_hub_staff(user, authorized_user)
        case Role.OFFICE_STAFF:
            db_user = create_office_staff(user, authorized_user)
        case _:
            raise InvalidRoleUserCreation()

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def create_president(user: UserCreate, authorized_user: User):
    if authorized_user.role not in (Role.ADMIN):
        raise AuthorizationException()

    if user.role != Role.PRESIDENT:
        raise InvalidRoleUserCreation()

    db_user = User.model_validate(user)
    db_user.hashed_password = get_password_hash(user.password)

    return db_user


def create_hub_manager(user: UserCreate, authorized_user: User):
    if authorized_user.role not in (Role.ADMIN, Role.PRESIDENT):
        raise AuthorizationException()

    if user.role != Role.HUB_MANAGER:
        raise InvalidRoleUserCreation()

    db_user = User.model_validate(user)
    db_user.hashed_password = get_password_hash(user.password)
    db_user.managed_by = authorized_user.id
    # db_user.hub_id = user.department_id

    return db_user


def create_office_manager(user: UserCreate, authorized_user: User):
    if authorized_user.role not in (Role.ADMIN, Role.PRESIDENT):
        raise AuthorizationException()

    if user.role != Role.OFFICE_MANAGER:
        raise InvalidRoleUserCreation()

    db_user = User.model_validate(user)
    db_user.hashed_password = get_password_hash(user.password)
    db_user.managed_by = authorized_user.id
    # db_user.office_id = user.department_id

    return db_user


def create_hub_staff(user: UserCreate, authorized_user: User):
    if authorized_user.role not in (Role.ADMIN, Role.HUB_MANAGER):
        raise AuthorizationException()

    if user.role != Role.HUB_STAFF:
        raise InvalidRoleUserCreation()

    db_user = User.model_validate(user)
    db_user.hashed_password = get_password_hash(user.password)
    db_user.managed_by = authorized_user.id
    # db_user.hub_id = user.department_id

    return db_user


def create_office_staff(user: UserCreate, authorized_user: User):
    if authorized_user.role not in (Role.ADMIN, Role.OFFICE_MANAGER):
        raise AuthorizationException()

    if user.role != Role.OFFICE_STAFF:
        raise InvalidRoleUserCreation()

    db_user = User.model_validate(user)
    db_user.hashed_password = get_password_hash(user.password)
    db_user.managed_by = authorized_user.id
    # db_user.office_id = user.department_id

    return db_user


def create_super_user(db: Session):
    settings = get_settings()

    user = User(
        username=settings.admin_username,
        role=Role.ADMIN,
        fullname="admin",
        birth=date(2000, 1, 1),
        phone="0123456789",
        department_id=1,
    )
    user.hashed_password = get_password_hash(settings.admin_password)

    statement = select(User).where(User.username == user.username)
    db_user = db.exec(statement).one_or_none()

    if not db_user:
        db.add(user)
        db.commit()
        db.refresh(user)

    return user
