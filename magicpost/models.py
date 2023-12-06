from sqlmodel import SQLModel


class MyBaseModel(SQLModel):
    pass


PHONE_REGEX = r"(03|05|07|08|09|01[2|6|8|9])+([0-9]{8})"
