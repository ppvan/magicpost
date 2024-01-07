from fastapi import Depends
from sqlmodel import Session, select

from magicpost.auth.models import Role, User
from magicpost.database import get_session
from magicpost.hub.exceptions import HubNotFound
from magicpost.hub.models import Hub
from magicpost.hub.schemas import HubCreate, HubRead, HubUpdate


def create_hub(hub: HubCreate, db: Session = Depends(get_session)):
    db_hub = Hub.model_validate(hub)
    db.add(db_hub)
    db.commit()
    db.refresh(db_hub)

    r_hub = HubRead.model_validate(db_hub.model_dump(exclude={"offices"}))

    if hub.manager:
        stmt = select(User).where(User.username == hub.manager)
        user = db.exec(stmt).one()
        if not user:
            raise HubNotFound()

        user.hub_id = db_hub.id
        r_hub.manager = user.username
        db.add(user)
        db.commit()

    return r_hub


def read_hubs(offset: int = 0, limit: int = 20, db: Session = Depends(get_session)):
    stmt = (
        select(Hub, User)
        .join(User, isouter=True)
        .where(User.role == Role.HUB_MANAGER)
        .offset(offset)
        .limit(limit)
        .order_by(Hub.id.desc())
    )

    r_hubs = []
    for hub, user in db.exec(stmt):
        r_hub = HubRead.model_validate(hub.model_dump(exclude={"offices"}))
        r_hub.manager = user.username if user else None

        r_hubs.append(r_hub)

    return r_hubs


def read_hub(hub_id: int, db: Session = Depends(get_session)):
    hub = db.get(Hub, hub_id)
    if not hub:
        raise HubNotFound()
    return hub


def update_hub(hub_id: int, hub: HubUpdate, db: Session = Depends(get_session)):
    hub_to_update = db.get(Hub, hub_id)
    if not hub_to_update:
        raise HubNotFound()

    if hub.manager:
        stmt = select(User).where(User.username == hub.manager)
        user = db.exec(stmt).one()
        if not user:
            raise HubNotFound()

        user.hub_id = hub_id
        db.add(user)

    team_data = hub.dict(exclude_unset=True, exclude={"manager"})
    for key, value in team_data.items():
        setattr(hub_to_update, key, value)

    db.add(hub_to_update)
    db.commit()
    db.refresh(hub_to_update)
    return hub_to_update


def delete_hub(hub_id: int, db: Session = Depends(get_session)):
    hub = db.get(Hub, hub_id)
    if not hub:
        raise HubNotFound()

    stmt = select(User).where(User.hub_id == hub_id)
    user = db.exec(stmt).one_or_none()

    if user:
        user.hub_id = None
        db.add(user)

    db.delete(hub)
    db.commit()
    return {"ok": True}
