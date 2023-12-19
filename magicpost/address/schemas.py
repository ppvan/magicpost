from pydantic import BaseModel, Field

from magicpost.models import ZIPCODE_REGEX


class Address(BaseModel):
    zipcode: str = Field(pattern=ZIPCODE_REGEX, min_length=1, max_length=5)
    address: str
