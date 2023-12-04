from pydantic import BaseModel
from typing import Optional


class HeroBase(BaseModel):
    name: str
    secret_name: str
    age: Optional[int] = None


class HeroCreate(HeroBase):
    pass


class Hero(HeroBase):
    id: int

    class Config:
        orm_mode = True
