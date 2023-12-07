# flake8: noqa
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import Session, SQLModel, select

from magicpost.database import create_db_and_tables, engine
from magicpost.hub import views as hub
from magicpost.item import views as item
from magicpost.office import views as office
from magicpost.order import views as order


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(hub.router)
app.include_router(office.router)
app.include_router(item.router)
app.include_router(order.router)

if __name__ == "__main__":
    create_db_and_tables()
