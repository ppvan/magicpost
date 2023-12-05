from datetime import datetime

from sqlmodel import Field, SQLModel


class MyBaseModel(SQLModel):
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default_factory=datetime.utcnow)
