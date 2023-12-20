import json

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool

from magicpost.app import app
from magicpost.auth.dependencies import president_required
from magicpost.database import get_session
from magicpost.hub.models import Hub
from magicpost.item.models import Item, ItemPath, ItemStatus, ItemType
from magicpost.item.schemas import ItemPathState, ItemRead, OrderCreate, OrderUpdate
from magicpost.office.models import Office

g_test_item = {
    "sender_name": "Phạm Văn Bách",
    "sender_address": "144 Xuân Thủy, Cầu Giấy, Hà Nội",
    "sender_phone": "0957507468",
    "sender_zipcode": "12011",
    # Receiver
    "receiver_name": "Nguyễn Văn Toàn",
    "receiver_address": "1 Đại Cồ Việt, Bách Khoa, Hai Bà Trưng, Hà Nội",
    "receiver_phone": "0957507468",
    "receiver_zipcode": "98811",
    # Cash on delivery
    "cod": 10_000,
    # Delivery Fees
    "weight": 1,
    "fee": 12_000,
    "type": ItemType.DOCUMENT,
}


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    def president_required_override():
        return None

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[president_required] = president_required_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="hub1")
def hub1_fixture(session: Session):
    hub = Hub(
        name="Điểm tập kết Ba Đình",
        address="Phường Trúc Bạch quận Ba Đình thành phố Hà Nội",
        zipcode="11117",
        phone="0981234567",
    )
    session.add(hub)
    session.commit()
    yield hub


@pytest.fixture(name="hub2")
def hub2_fixture(session: Session):
    hub = Hub(
        name="Điểm tập kết Tam Giang",
        address="Điểm Tam Giang huyện Năm Căn tỉnh Cà Mau",
        zipcode="98812",
        phone="0981234567",
    )
    session.add(hub)
    session.commit()
    yield hub


@pytest.fixture(name="office1")
def office1_fixture(session: Session, hub1: Hub):
    office = Office(
        hub=hub1,
        name="Điểm giao dịch Trung Văn",
        address="Phường Trung Văn quận Nam Từ Liém, Hà Nội",
        zipcode="12011",
        phone="0981234567",
    )
    session.add(office)
    session.commit()
    yield office


@pytest.fixture(name="office2")
def office2_fixture(session: Session, hub2: Hub):
    office = Office(
        hub=hub2,
        name="Điểm giao dịch Lâm Hải",
        address="Điểm Lâm Hải huyện Năm Căn tỉnh Cà Mau",
        zipcode="98811",
        phone="0981234567",
    )
    session.add(office)
    session.commit()
    yield office


def test_flow_item_ok(client: TestClient, session: Session):
    test_item = g_test_item.copy()

    # Create item & send to office1
    response = client.post("/api/v1/items/", json=test_item)
    data = response.json()

    assert response.status_code == 200
    assert data["sender_name"] == test_item["sender_name"]
    assert data["receiver_name"] == test_item["receiver_name"]
    assert session.get(ItemPath, 1).zipcode == data["sender_zipcode"]

    # Send that item to hub1

    item2 = ItemRead(**data)
    order2 = OrderCreate(status=ItemStatus.ON_DELIVERY, items=[item2], zipcode="11117")
    order2_json = json.loads(order2.model_dump_json())
    response2 = client.post("/api/v1/items/move", json=order2_json)

    data2 = response2.json()
    print(data2)
    path2: ItemPath = session.get(ItemPath, 2)

    assert response2.status_code == 200
    assert session.get(Item, data["id"]).status == ItemStatus.ON_DELIVERY
    assert path2.zipcode == "11117"
    assert path2.state == ItemPathState.PENDDING

    # Hub1 confirm arrival
    order3 = OrderUpdate(items=[item2], zipcode="11117")
    order3_json = json.loads(order3.model_dump_json())
    response3 = client.post("/api/v1/items/confirm", json=order3_json)
    # data3 = response3.json()
    session.refresh(path2)

    assert response3.status_code == 200
    assert path2.zipcode == "11117"
    assert path2.state == ItemPathState.DONE

    # Send that item to hub2

    order4 = OrderCreate(status=ItemStatus.ON_DELIVERY, items=[item2], zipcode="98812")
    order4_json = json.loads(order4.model_dump_json())
    response4 = client.post("/api/v1/items/move", json=order4_json)

    data4 = response2.json()
    print(data4)
    path4: ItemPath = session.get(ItemPath, 3)

    assert response4.status_code == 200
    assert session.get(Item, data["id"]).status == ItemStatus.ON_DELIVERY
    assert path4.zipcode == "98812"
    assert path4.state == ItemPathState.PENDDING

    # Hub2 confirm arrival

    order5 = OrderUpdate(items=[item2], zipcode="98812")
    order5_json = json.loads(order5.model_dump_json())
    response3 = client.post("/api/v1/items/confirm", json=order5_json)
    session.refresh(path4)

    assert response3.status_code == 200
    assert path4.zipcode == "98812"
    assert path4.state == ItemPathState.DONE

    # Send that item to office2
    order6 = OrderCreate(status=ItemStatus.ON_DELIVERY, items=[item2], zipcode="98811")
    order6_json = json.loads(order6.model_dump_json())
    response6 = client.post("/api/v1/items/move", json=order6_json)

    data6 = response6.json()
    print(data6)
    path6: ItemPath = session.get(ItemPath, 4)

    assert response6.status_code == 200
    assert session.get(Item, data["id"]).status == ItemStatus.ON_DELIVERY
    assert path6.zipcode == "98811"
    assert path6.state == ItemPathState.PENDDING

    # Office2 confirm arrival
    order7 = OrderUpdate(items=[item2], zipcode="98811")
    order7_json = json.loads(order7.model_dump_json())
    response7 = client.post("/api/v1/items/confirm", json=order7_json)
    session.refresh(path6)

    assert response7.status_code == 200
    assert path6.zipcode == "98811"
    assert path6.state == ItemPathState.DONE

    # Check the item path

    stmt = select(ItemPath).filter_by(item_id=data["id"])
    paths = session.exec(stmt).all()
    zipcodes = [p.zipcode for p in paths]

    assert len(paths) == 4
    assert "11117" in zipcodes
    assert "98812" in zipcodes
    assert "98811" in zipcodes
    assert "12011" in zipcodes
