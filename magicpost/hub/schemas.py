from typing import Optional

from pydantic import BaseModel, Field, PositiveInt

from magicpost.models import PHONE_REGEX, ZIPCODE_REGEX


class HubCreate(BaseModel):
    name: str = Field(min_length=1)
    address: str = Field(min_length=1)
    phone: str = Field(pattern=PHONE_REGEX, min_length=1, max_length=10)
    zipcode: str = Field(pattern=ZIPCODE_REGEX, min_length=1, max_length=5)


class HubRead(BaseModel):
    id: PositiveInt
    name: str = Field(min_length=1)
    address: str = Field(min_length=1)
    phone: str = Field(pattern=PHONE_REGEX, min_length=1, max_length=10)
    zipcode: str = Field(pattern=ZIPCODE_REGEX, min_length=1, max_length=5)
    manager: str = None


class HubUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    zipcode: Optional[str] = None
    manager: str = None
