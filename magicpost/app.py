# flake8: noqa
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import Session, SQLModel, select

from magicpost.database import create_db_and_tables, engine
from magicpost.hub import views as hub
from magicpost.office import views as office


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(hub.router)
app.include_router(office.router)

if __name__ == "__main__":
    create_db_and_tables()