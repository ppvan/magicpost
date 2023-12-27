# flake8: noqa
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, SQLModel, select

from magicpost.address import views as address
from magicpost.auth import views as auth
from magicpost.auth.crud import create_super_user
from magicpost.database import create_db_and_tables, engine
from magicpost.hub import views as hub
from magicpost.item import views as item
from magicpost.office import views as office


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()

    with Session(engine) as session:
        create_super_user(session)

    yield


app = FastAPI(lifespan=lifespan, title="MagicPost")

origins = [
    "http://localhost:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(item.router)
app.include_router(hub.router)
app.include_router(office.router)
app.include_router(address.router)

if __name__ == "__main__":
    create_db_and_tables()
