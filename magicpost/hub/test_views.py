import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from magicpost.app import app
from magicpost.database import get_session
from magicpost.hub.models import Hub

test_hub = {
    "name": "Bưu điện Chùa Láng",
    "phone": "0981235431",
    "address": "23 Chùa Láng, Hà Nội",
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


def test_get_hubs(session: Session, client: TestClient):
    hub1 = Hub(name="test1", address="23 Chùa Láng, Hà Nội", phone="0981234567")
    hub2 = Hub(name="test2", address="23 Chùa Láng, Hà Nội", phone="0981234567")
    hub3 = Hub(name="test3", address="23 Chùa Láng, Hà Nội", phone="0981234567")

    session.add_all([hub1, hub2, hub3])
    session.commit()

    response = client.get("/hubs/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 3
    assert data[0]["name"] == hub1.name


def test_get_one_hub(session: Session, client: TestClient):
    hub1 = Hub(name="test1", address="23 Chùa Láng, Hà Nội", phone="0981234567")

    session.add(hub1)
    session.commit()

    response = client.get("/hubs/1")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == hub1.name


def test_get_hub_not_found(client: TestClient):
    response = client.get("/hubs/100")

    assert response.status_code == 404


def test_delete_hub(session: Session, client: TestClient):
    hub1 = Hub(name="test1", address="23 Chùa Láng, Hà Nội", phone="0981234567")

    session.add(hub1)
    session.commit()

    response = client.delete("/hubs/1")
    data = response.json()

    assert response.status_code == 200
    assert data["ok"]


def test_create_hub(client: TestClient):
    response = client.post("/hubs/", json=test_hub)
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == test_hub["name"]
    assert data["address"] == test_hub["address"]


def test_create_hub_blank_name(client: TestClient):
    test_hub["name"] = ""
    response = client.post("/hubs/", json=test_hub)
    # data = response.json()

    assert response.status_code == 422


def test_create_hub_empty_address(client: TestClient):
    test_hub["address"] = ""
    response = client.post("/hubs/", json=test_hub)
    # data = response.json()

    assert response.status_code == 422


def test_create_hub_invalid_phone(client: TestClient):
    test_hub["phone"] = "+8417227"
    response = client.post("/hubs/", json=test_hub)
    # data = response.json()

    assert response.status_code == 422
