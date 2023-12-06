import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from magicpost.app import app
from magicpost.database import get_session
from magicpost.hub.models import Hub
from magicpost.office.models import Office

test_office = {
    "name": "Điểm tập kết Cầu Giấy",
    "phone": "098123543",
    "address": "Cầu Giấy, Hà Nội",
    "hud_id": 1,
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


@pytest.fixture(name="hub")
def hub_fixture(session: Session):
    hub = Hub(name="test", address="23 Chùa Láng, Hà Nội", phone="0981234567")
    session.add(hub)
    session.commit()
    yield hub


def test_get_offices(hub: Hub, session: Session, client: TestClient):
    office1 = Office(
        hub=hub,
        name="test1",
        address="23 Chùa Láng, Hà Nội",
        phone="0981234567",
    )
    office2 = Office(
        hub=hub,
        name="test2",
        address="23 Chùa Láng, Hà Nội",
        phone="0981234567",
    )
    office3 = Office(
        hub=hub,
        name="test3",
        address="23 Chùa Láng, Hà Nội",
        phone="0981234567",
    )

    session.add_all([office1, office2, office3])
    session.commit()

    response = client.get("/offices/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 3
    assert data[0]["name"] == office1.name
    assert data[1]["name"] == office2.name
    assert data[2]["name"] == office3.name


def test_get_a_office(hub: Hub, session: Session, client: TestClient):
    office1 = Office(
        hub=hub,
        name="test1",
        address="23 Chùa Láng, Hà Nội",
        phone="0981234567",
    )

    session.add(office1)
    session.commit()

    response = client.get("/offices/1")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == office1.name


def test_delete_office(hub: Hub, session: Session, client: TestClient):
    office1 = Office(
        hub=hub,
        name="test1",
        address="23 Chùa Láng, Hà Nội",
        phone="0981234567",
    )

    session.add(office1)
    session.commit()

    response = client.delete("/offices/1")
    data = response.json()

    assert response.status_code == 200
    assert data["ok"]


def test_get_office_not_found(session: Session, client: TestClient):
    response = client.get("/offices/10")

    assert response.status_code == 404


def test_create_office_ok(hub: Hub, client: TestClient):
    test_office["hub_id"] = hub.id

    response = client.post("/offices/", json=test_office)
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == test_office["name"]
    assert data["address"] == test_office["address"]


def test_create_office_hub_notfound(hub: Hub, client: TestClient):
    test_office["hub_id"] = 10
    response = client.post("/offices/", json=test_office)
    # data = response.json()

    assert response.status_code == 404


def test_create_office_blank_name(hub: Hub, client: TestClient):
    test_office["hub_id"] = hub.id
    test_office["name"] = ""
    response = client.post("/offices/", json=test_office)
    # data = response.json()

    assert response.status_code == 422


def test_create_office_empty_address(hub: Hub, client: TestClient):
    test_office["hub_id"] = hub.id
    test_office["address"] = ""
    response = client.post("/offices/", json=test_office)
    # data = response.json()

    assert response.status_code == 422


def test_create_office_invalid_phone(hub: Hub, client: TestClient):
    test_office["hub_id"] = hub.id
    test_office["phone"] = "+8417227"
    response = client.post("/offices/", json=test_office)
    # data = response.json()

    assert response.status_code == 422
