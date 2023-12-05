# flake8: noqa
from sqlmodel import Session, SQLModel, select
from fastapi import FastAPI
from contextlib import asynccontextmanager

from . import models
from .database import engine


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    create_db_and_tables()
