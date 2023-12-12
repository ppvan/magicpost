import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from magicpost.app import app
from magicpost.database import get_session
from magicpost.hub.models import Hub
from magicpost.order.models import Hub2HubOrder, OrderStatus, OrderType


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


@pytest.fixture(name="receiver_hub")
def hub_fixture1(session: Session):
    hub = Hub(name="test", address="23 Chùa Láng, Hà Nội", phone="0981234567")
    session.add(hub)
    session.commit()
    yield hub


@pytest.fixture(name="sender_hub")
def hub_fixture2(session: Session):
    hub = Hub(name="test", address="23 Chùa Láng, Hà Nội", phone="0981234567")
    session.add(hub)
    session.commit()
    yield hub


def test_create_order_ok(
    sender_hub: Hub, receiver_hub: Hub, session: Session, client: TestClient
):
    order = {
        "sender_id": sender_hub.id,
        "receiver_id": receiver_hub.id,
        "status": OrderStatus.PENDING,
    }

    params = {"type": OrderType.HUB2HUB.value}
    response = client.post("/orders/", params=params, json=order)
    data = response.json()

    print(data)

    assert response.status_code == 200
    assert data["sender_id"] == order["sender_id"]
    assert data["receiver_id"] == order["receiver_id"]


def test_create_order_not_exist_sender(
    sender_hub: Hub, receiver_hub: Hub, session: Session, client: TestClient
):
    order = {
        "sender_id": 100,
        "receiver_id": receiver_hub.id,
        "status": OrderStatus.PENDING,
    }

    params = {"type": OrderType.HUB2HUB.value}
    response = client.post("/orders/", params=params, json=order)
    # data = response.json()

    assert response.status_code == 404


def test_create_order_not_exist_receiver(
    sender_hub: Hub, receiver_hub: Hub, session: Session, client: TestClient
):
    order = {
        "sender_id": sender_hub.id,
        "receiver_id": 100,
        "status": OrderStatus.PENDING,
    }

    params = {"type": OrderType.HUB2HUB.value}
    response = client.post("/orders/", params=params, json=order)
    # data = response.json()

    assert response.status_code == 404


# def test_create_order_invalid_type(
#     sender_hub: Hub, receiver_hub: Hub, session: Session, client: TestClient
# ):
#     order = {
#         "sender_id": sender_hub.id,
#         "receiver_id": receiver_hub.id,
#         "status": OrderStatus.PENDING,
#     }

#     params = {"type": "invalid"}
#     response = client.post("/orders/", params=params, json=order)
#     # data = response.json()

#     assert response.status_code == 422


def test_create_order_invalid_status(
    sender_hub: Hub, receiver_hub: Hub, session: Session, client: TestClient
):
    order = {
        "sender_id": sender_hub.id,
        "receiver_id": receiver_hub.id,
        "status": "invalid",
    }

    params = {"type": OrderType.HUB2HUB.value}
    response = client.post("/orders/", params=params, json=order)
    # data = response.json()

    assert response.status_code == 422


def test_update_order_ok(
    sender_hub: Hub, receiver_hub: Hub, session: Session, client: TestClient
):
    order = {
        "sender_id": sender_hub.id,
        "receiver_id": receiver_hub.id,
        "status": OrderStatus.PENDING,
    }
    db_order = Hub2HubOrder.model_validate(order)

    session.add(db_order)
    session.commit()
    session.refresh(db_order)

    assert db_order.status == OrderStatus.PENDING

    params = {"type": OrderType.HUB2HUB.value}
    payload = {"status": OrderStatus.COMPLETED.value}
    response = client.patch(f"/orders/{db_order.id}", params=params, json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["sender_id"] == order["sender_id"]
    assert data["receiver_id"] == order["receiver_id"]
    assert data["status"] == OrderStatus.COMPLETED.value


def test_update_order_invalid_status(
    sender_hub: Hub, receiver_hub: Hub, session: Session, client: TestClient
):
    order = {
        "sender_id": sender_hub.id,
        "receiver_id": receiver_hub.id,
        "status": OrderStatus.PENDING,
    }
    db_order = Hub2HubOrder.model_validate(order)

    session.add(db_order)
    session.commit()
    session.refresh(db_order)

    assert db_order.status == OrderStatus.PENDING

    params = {"type": OrderType.HUB2HUB.value}
    payload = {"status": "invalid"}
    response = client.patch(f"/orders/{db_order.id}", params=params, json=payload)

    assert response.status_code == 422
