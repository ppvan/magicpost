from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from magicpost.app import app
from magicpost.auth.dependencies import get_password_hash
from magicpost.auth.models import Role, User
from magicpost.database import get_session


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="president")
def president_fixture(session: Session):
    president = User(
        username="president",
        role=Role.PRESIDENT,
        fullname="president",
        birth=date(2000, 1, 1),
        phone="0981272356",
    )
    president.hashed_password = get_password_hash("president")
    session.add(president)
    session.commit()
    session.refresh(president)

    yield president


@pytest.fixture(name="admin")
def admin_fixture(session: Session):
    admin = User(
        username="admin",
        role=Role.ADMIN,
        fullname="admin",
        birth=date(2000, 1, 1),
        phone="0981272356",
    )
    admin.hashed_password = get_password_hash("admin")
    session.add(admin)
    session.commit()
    session.refresh(admin)

    yield admin


@pytest.fixture(name="hub_manager")
def hub_manager_fixture(session: Session):
    hub_manager = User(
        username="hub_manager",
        role=Role.HUB_MANAGER,
        fullname="hub_manager",
        birth=date(2000, 1, 1),
        phone="0981272356",
    )
    hub_manager.hashed_password = get_password_hash("hub_manager")
    session.add(hub_manager)
    session.commit()
    session.refresh(hub_manager)

    yield hub_manager


@pytest.fixture(name="office_manager")
def office_manager_fixture(session: Session):
    office_manager = User(
        username="office_manager",
        role=Role.OFFICE_MANAGER,
        fullname="office_manager",
        birth=date(2000, 1, 1),
        phone="0981272356",
    )
    office_manager.hashed_password = get_password_hash("office_manager")
    session.add(office_manager)
    session.commit()
    session.refresh(office_manager)

    yield office_manager


@pytest.fixture(name="hub_staff")
def hub_staff_fixture(session: Session):
    hub_staff = User(
        username="hub_staff",
        role=Role.HUB_STAFF,
        fullname="hub_staff",
        birth=date(2000, 1, 1),
        phone="0981272356",
    )
    hub_staff.hashed_password = get_password_hash("hub_staff")
    session.add(hub_staff)
    session.commit()
    session.refresh(hub_staff)

    yield hub_staff


@pytest.fixture(name="office_staff")
def office_staff_fixture(session: Session):
    office_staff = User(
        username="office_staff",
        role=Role.OFFICE_STAFF,
        fullname="office_staff",
        birth=date(2000, 1, 1),
        phone="0981272356",
    )
    office_staff.hashed_password = get_password_hash("office_staff")
    session.add(office_staff)
    session.commit()
    session.refresh(office_staff)

    yield office_staff


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="admin_token")
def token_fixture(admin: User, client: TestClient):
    response = client.post(
        "/api/v1/auth/token", data={"username": "admin", "password": "admin"}
    )
    token = response.json().get("access_token", None)

    assert token
    assert response.status_code == 200

    return token


@pytest.fixture(name="president_token")
def president_token_fixture(president: User, client: TestClient):
    response = client.post(
        "/api/v1/auth/token",
        data={"username": president.username, "password": "president"},
    )
    token = response.json().get("access_token", None)

    assert token
    assert response.status_code == 200

    return token


@pytest.fixture(name="hub_manager_token")
def hub_manager_token_fixture(hub_manager: User, client: TestClient):
    response = client.post(
        "/api/v1/auth/token",
        data={"username": hub_manager.username, "password": "hub_manager"},
    )
    token = response.json().get("access_token", None)

    assert token
    assert response.status_code == 200

    return token


@pytest.fixture(name="office_manager_token")
def office_manager_token_fixture(office_manager: User, client: TestClient):
    response = client.post(
        "/api/v1/auth/token",
        data={"username": office_manager.username, "password": "office_manager"},
    )
    token = response.json().get("access_token", None)

    assert token
    assert response.status_code == 200

    return token


@pytest.fixture(name="hub_staff_token")
def hub_staff_token_fixture(hub_staff: User, client: TestClient):
    response = client.post(
        "/api/v1/auth/token",
        data={"username": hub_staff.username, "password": "hub_staff"},
    )
    token = response.json().get("access_token", None)

    assert token
    assert response.status_code == 200

    return token


@pytest.fixture(name="office_staff_token")
def office_staff_token_fixture(office_staff: User, client: TestClient):
    response = client.post(
        "/api/v1/auth/token",
        data={"username": office_staff.username, "password": "office_staff"},
    )
    token = response.json().get("access_token", None)

    assert token
    assert response.status_code == 200

    return token


def test_login_admin_ok(admin: User, client: TestClient):
    response = client.post(
        "/api/v1/auth/token", data={"username": "admin", "password": "admin"}
    )
    token = response.json().get("access_token", None)

    assert token
    assert response.status_code == 200


def test_create_president_ok(admin_token: str, client: TestClient):
    user_data = {
        "username": "president",
        "password": "president",
        "fullname": "president",
        "birth": "2000-01-01",
        "phone": "0981272356",
        "role": Role.PRESIDENT.value,
        "department_id": 1,
    }

    response = client.post(
        "/api/v1/auth/register",
        json=user_data,
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    data = response.json()

    print(data)

    assert response.status_code == 200


def test_create_president_not_admin(president_token: str, client: TestClient):
    user_data = {
        "username": "president-test",
        "password": "president",
        "fullname": "president",
        "birth": "2000-01-01",
        "phone": "0981272356",
        "role": Role.PRESIDENT.value,
        "department_id": 1,
    }

    response = client.post(
        "/api/v1/auth/register",
        json=user_data,
        headers={"Authorization": f"Bearer {president_token}"},
    )
    assert response.status_code == 403


def test_create_hub_manager_not_president(hub_manager_token: str, client: TestClient):
    user_data = {
        "username": "hub_manager-test",
        "password": "hub_manager",
        "fullname": "hub_manager",
        "birth": "2000-01-01",
        "phone": "0981272356",
        "role": Role.HUB_MANAGER.value,
        "department_id": 1,
    }

    response = client.post(
        "/api/v1/auth/register",
        json=user_data,
        headers={"Authorization": f"Bearer {hub_manager_token}"},
    )
    assert response.status_code == 403


def test_create_hub_staff_not_manager(hub_staff_token: str, client: TestClient):
    user_data = {
        "username": "hub_staff-test",
        "password": "hub_staff",
        "fullname": "hub_staff",
        "birth": "2000-01-01",
        "phone": "0981272356",
        "role": Role.HUB_STAFF.value,
        "department_id": 1,
    }

    response = client.post(
        "/api/v1/auth/register",
        json=user_data,
        headers={"Authorization": f"Bearer {hub_staff_token}"},
    )
    assert response.status_code == 403


def test_create_office_staff_not_manager(office_staff_token: str, client: TestClient):
    user_data = {
        "username": "office_staff-test",
        "password": "office_staff",
        "fullname": "office_staff",
        "birth": "2000-01-01",
        "phone": "0981272356",
        "role": Role.OFFICE_STAFF.value,
        "department_id": 1,
    }

    response = client.post(
        "/api/v1/auth/register",
        json=user_data,
        headers={"Authorization": f"Bearer {office_staff_token}"},
    )
    assert response.status_code == 403


def test_create_office_manager_not_president(
    hub_manager_token: str, client: TestClient
):
    user_data = {
        "username": "office_manager-test",
        "password": "office_manager",
        "fullname": "office_manager",
        "birth": "2000-01-01",
        "phone": "0981272356",
        "role": Role.OFFICE_MANAGER.value,
        "department_id": 1,
    }

    response = client.post(
        "/api/v1/auth/register",
        json=user_data,
        headers={"Authorization": f"Bearer {hub_manager_token}"},
    )
    assert response.status_code == 403


def test_create_hub_manager_admin_ok(admin_token: str, client: TestClient):
    user_data = {
        "username": "hub_manager",
        "password": "hub_manager",
        "fullname": "hub_manager",
        "birth": "2000-01-01",
        "phone": "0981272356",
        "role": Role.HUB_MANAGER.value,
        "department_id": 1,
    }

    response = client.post(
        "/api/v1/auth/register",
        json=user_data,
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    data = response.json()

    assert response.status_code == 200
    assert data["role"] == Role.HUB_MANAGER.value
    assert data["username"] == "hub_manager"


def test_create_hub_manager_president_ok(president_token: str, client: TestClient):
    user_data = {
        "username": "hub_manager",
        "password": "hub_manager",
        "fullname": "hub_manager",
        "birth": "2000-01-01",
        "phone": "0981272356",
        "role": Role.HUB_MANAGER.value,
        "department_id": 1,
    }

    response = client.post(
        "/api/v1/auth/register",
        json=user_data,
        headers={"Authorization": f"Bearer {president_token}"},
    )

    data = response.json()

    assert response.status_code == 200
    assert data["role"] == Role.HUB_MANAGER.value
    assert data["username"] == "hub_manager"


def test_create_office_manager_ok(admin_token: str, client: TestClient):
    user_data = {
        "username": "office_manager",
        "password": "office_manager",
        "fullname": "office_manager",
        "birth": "2000-01-01",
        "phone": "0981272356",
        "role": Role.OFFICE_MANAGER.value,
        "department_id": 1,
    }

    response = client.post(
        "/api/v1/auth/register",
        json=user_data,
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    data = response.json()

    assert response.status_code == 200
    assert data["role"] == Role.OFFICE_MANAGER.value
    assert data["username"] == "office_manager"


def test_create_hub_staff_ok(admin_token: str, client: TestClient):
    user_data = {
        "username": "hub_staff",
        "password": "hub_staff",
        "fullname": "hub_staff",
        "birth": "2000-01-01",
        "phone": "0981272356",
        "role": Role.HUB_STAFF.value,
        "department_id": 1,
    }

    response = client.post(
        "/api/v1/auth/register",
        json=user_data,
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    data = response.json()

    assert response.status_code == 200
    assert data["role"] == Role.HUB_STAFF.value
    assert data["username"] == "hub_staff"


def test_create_office_staff_ok(admin_token: str, client: TestClient):
    user_data = {
        "username": "office_staff",
        "password": "office_staff",
        "fullname": "office_staff",
        "birth": "2000-01-01",
        "phone": "0981272356",
        "role": Role.OFFICE_STAFF.value,
        "department_id": 1,
    }

    response = client.post(
        "/api/v1/auth/register",
        json=user_data,
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    data = response.json()

    assert response.status_code == 200
    assert data["role"] == Role.OFFICE_STAFF.value
    assert data["username"] == "office_staff"


def test_register_not_login(client: TestClient):
    user_data = {
        "username": "president",
        "password": "president",
        "fullname": "president",
        "birth": "2000-01-01",
        "phone": "0981272356",
        "role": Role.PRESIDENT.value,
        "department_id": 1,
    }

    response = client.post("/api/v1/auth/register", json=user_data)

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
