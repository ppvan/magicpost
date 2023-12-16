from fastapi import Depends
from sqlmodel import Session, select

from magicpost.database import get_session
from magicpost.hub.exceptions import HubNotFound
from magicpost.hub.models import Hub
from magicpost.hub.schemas import HubCreate, HubUpdate


def create_hub(hub: HubCreate, db: Session = Depends(get_session)):
    db_hub = Hub.model_validate(hub)
    db.add(db_hub)
    db.commit()
    db.refresh(db_hub)
    return db_hub


def read_hubs(offset: int = 0, limit: int = 20, db: Session = Depends(get_session)):
    hubs = db.exec(select(Hub).offset(offset).limit(limit)).all()
    return hubs


def read_hub(hub_id: int, db: Session = Depends(get_session)):
    hub = db.get(Hub, hub_id)
    if not hub:
        raise HubNotFound()
    return hub


def update_hub(hub_id: int, hub: HubUpdate, db: Session = Depends(get_session)):
    hub_to_update = db.get(Hub, hub_id)
    if not hub_to_update:
        raise HubNotFound()

    team_data = hub.dict(exclude_unset=True)
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

    db.delete(hub)
    db.commit()
    return {"ok": True}
