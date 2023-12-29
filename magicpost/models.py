from sqlmodel import SQLModel


class MyBaseModel(SQLModel):
    pass


PHONE_REGEX = r"^([0-9]{10})$"
ZIPCODE_REGEX = r"^[0-9]{5}$"
