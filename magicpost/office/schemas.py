from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from magicpost.models import PHONE_REGEX, ZIPCODE_REGEX


class OfficeCreate(BaseModel):
    name: str = Field(min_length=1)
    address: str = Field(min_length=1)
    phone: str = Field(pattern=PHONE_REGEX)
    zipcode: str = Field(pattern=ZIPCODE_REGEX, min_length=1, max_length=5)
    manager: str = Field(default=None)
    hub_id: PositiveInt

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Điểm tập kết Cầu Giấy",
                "phone": "098123543",
                "address": "Cầu Giấy, Hà Nội",
                "hub_id": 1,
            }
        }
    )


class OfficeRead(BaseModel):
    id: int
    name: str = Field(min_length=1)
    address: str = Field(min_length=1)
    phone: str = Field(pattern=PHONE_REGEX)
    zipcode: str = Field(pattern=ZIPCODE_REGEX, min_length=1, max_length=5)
    hub_id: PositiveInt
    manager: str = Field(default=None)
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class OfficeUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    zipcode: Optional[str] = None
    manager: str = Field(default=None)
    hub_id: int = Field(default=None)
