import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from magicpost.app import app
from magicpost.database import get_session
from magicpost.item.models import ItemType

test_item = {
    "sender_name": "Phạm Văn Bách",
    "sender_address": "144 Xuân Thủy, Cầu Giấy, Hà Nội",
    "sender_phone": "0957507468",
    # Receiver
    "receiver_name": "Nguyễn Văn Toàn",
    "receiver_address": "1 Đại Cồ Việt, Bách Khoa, Hai Bà Trưng, Hà Nội",
    "receiver_phone": "0957507468",
    # Cash on delivery
    "cod": 10_000,
    "additional_cod": 5_500,
    # Delivery Fees
    "weight": 1,
    "base_fee": 12_000,
    "additional_fee": 0,
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

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_item(client: TestClient):
    response = client.post("/items/", json=test_item)
    data = response.json()

    assert response.status_code == 200
    assert data["sender_name"] == test_item["sender_name"]
    assert data["receiver_name"] == test_item["receiver_name"]


def test_create_item_incorrect_type(client: TestClient):
    test_item["type"] = "document"
    response = client.post("/items/", json=test_item)
    # data = response.json()

    assert response.status_code == 422


def test_create_item_negative_fees(client: TestClient):
    test_item["base_fee"] = -1
    test_item["additional_fee"] = -1
    response = client.post("/items/", json=test_item)
    # data = response.json()

    assert response.status_code == 422


def test_create_item_negative_cod(client: TestClient):
    test_item["cod"] = -1
    response = client.post("/items/", json=test_item)
    # data = response.json()

    assert response.status_code == 422


def test_create_item_negative_weight(client: TestClient):
    test_item["weight"] = -1
    response = client.post("/items/", json=test_item)
    # data = response.json()

    assert response.status_code == 422


def test_create_item_empty_address(client: TestClient):
    test_item["sender_address"] = ""
    response = client.post("/items/", json=test_item)
    # data = response.json()

    assert response.status_code == 422


def test_create_item_empty_phone(client: TestClient):
    test_item["sender_phone"] = ""
    response = client.post("/items/", json=test_item)
    # data = response.json()

    assert response.status_code == 422


def test_create_item_invalid_phone(client: TestClient):
    test_item["sender_phone"] = "00975662570000000000000"
    response = client.post("/items/", json=test_item)
    # data = response.json()

    assert response.status_code == 422


# def test_create_item_valid_phone(client: TestClient):
#     test_item["sender_phone"] = "0912419333"
#     response = client.post("/items/", json=test_item)
#     # data = response.json()

#     assert response.status_code == 200
