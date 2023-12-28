"""
Khởi tạo dữ liệu mẫu. File này cần được đọc kĩ trước khi chạy, nó ghi trực tiếp vào db hoặc xóa sạch db nếu cần
"""
import json
import random
from datetime import date, datetime, timedelta

from sqlmodel import Session, select

from magicpost.address import views as address
from magicpost.auth import views as auth
from magicpost.auth.crud import create_super_user, create_user
from magicpost.auth.dependencies import get_password_hash
from magicpost.auth.models import Role, User
from magicpost.database import create_db_and_tables, engine
from magicpost.hub import views as hub
from magicpost.hub.crud import create_hub
from magicpost.hub.models import Hub
from magicpost.item import views as item
from magicpost.item.models import Item, ItemPath, ItemType
from magicpost.office import views as office
from magicpost.office.models import Office


def seed():
    # create_db_and_tables()
    # seed_users()
    seed_item()
    pass


def seed_office_and_hub():
    with Session(engine) as session:
        hubs = []
        with open("magicpost/data/hubs.json") as f:
            hubs = json.load(f)

        for hub in hubs:
            db_hub = Hub(
                name=hub["name"],
                address=hub["address"],
                phone=hub["phone"],
                zipcode=hub["zipcode"],
            )
            session.add(db_hub)

            for office in hub["offices"]:
                db_office = Office(
                    name=office["name"],
                    address=office["address"],
                    phone=office["phone"],
                    zipcode=office["zipcode"],
                    hub=db_hub,
                )
                session.add(db_office)

        session.commit()


def random_date(start_year, end_year):
    start_date = date(start_year, 1, 1)
    end_date = date(end_year + 1, 1, 1) - timedelta(days=1)

    random_days = random.randint(0, (end_date - start_date).days)
    random_date = start_date + timedelta(days=random_days)

    return random_date


def seed_users():
    users = json.load(open("magicpost/data/users.json"))
    random.shuffle(users)

    with Session(engine) as session:
        president = User(
            username="president",
            role=Role.PRESIDENT,
            fullname="Phạm Văn Phúc",
            birth=date(2000, 1, 1),
            phone="0981272356",
        )
        president.hashed_password = get_password_hash("president")
        session.add(president)
        session.commit()

        stmt = select(Office)
        hub_stmt = select(Hub)
        offices = session.exec(stmt).all()
        hubs = session.exec(hub_stmt).all()

        for office in offices:
            s_user = users.pop()
            m1_user = users.pop()
            m2_user = users.pop()
            m3_user = users.pop()
            print(s_user["username"])
            office_manager = User(
                username=s_user["username"],
                role=Role.OFFICE_MANAGER,
                fullname=s_user["fullname"],
                birth=random_date(1970, 2000),
                phone=s_user["phone"],
                managed_by=president.id,
                office_id=office.id,
            )
            office_manager.hashed_password = get_password_hash(s_user["username"])
            session.add(office_manager)
            session.commit()

            for s in [m1_user, m2_user, m3_user]:
                office_staff = User(
                    username=s["username"],
                    role=Role.OFFICE_STAFF,
                    fullname=s["fullname"],
                    birth=random_date(1970, 2000),
                    phone=s["phone"],
                    managed_by=office_manager.id,
                    office_id=office.id,
                )
                office_staff.hashed_password = get_password_hash(s["username"])
                session.add(office_staff)

            session.commit()

        for hub in hubs:
            s_user = users.pop()
            m1_user = users.pop()
            m2_user = users.pop()
            m3_user = users.pop()

            print(s_user["username"])

            hub_manager = User(
                username=s_user["username"],
                role=Role.HUB_MANAGER,
                fullname=s_user["fullname"],
                birth=random_date(1970, 2000),
                phone=s_user["phone"],
                managed_by=president.id,
                hub_id=hub.id,
            )
            hub_manager.hashed_password = get_password_hash(s_user["username"])
            session.add(hub_manager)
            session.commit()

            for s in [m1_user, m2_user, m3_user]:
                hub_staff = User(
                    username=s["username"],
                    role=Role.HUB_STAFF,
                    fullname=s["fullname"],
                    birth=random_date(1970, 2000),
                    phone=s["phone"],
                    managed_by=hub_manager.id,
                    hub_id=hub.id,
                )
                hub_staff.hashed_password = get_password_hash(s["username"])
                session.add(hub_staff)

            session.commit()

    session.commit()

    print("done")


def seed_item():
    with Session(engine) as session:
        stmt = select(Office)
        offices = session.exec(stmt).all()
        users = json.load(open("magicpost/data/users.json"))

        random.shuffle(offices)
        random.shuffle(users)

        for _ in range(100):
            office1 = offices.pop()
            office2 = offices.pop()
            user1 = users.pop()
            user2 = users.pop()
            w = random.random() * 10

            item = Item(
                sender_name=user1["fullname"],
                sender_address=office1.address,
                sender_phone=user1["phone"],
                sender_zipcode=office1.zipcode,
                receiver_name=user2["fullname"],
                receiver_address=office2.address,
                receiver_phone=user2["phone"],
                receiver_zipcode=office2.zipcode,
                cod=0,
                weight=w,
                fee=5_000 + w * 10_000,
                type=random.choice([ItemType.DOCUMENT, ItemType.GOODS]),
            )

            session.add(item)

        session.commit()

        pass
    pass


if __name__ == "__main__":
    seed()
