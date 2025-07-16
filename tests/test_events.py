import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
import sys
sys.path.append("src")

from api.db.session import get_session
from main import app


DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def override_get_session():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(scope="function", autouse=True)
def create_test_db():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


client = TestClient(app)


def test_create_event():
    response = client.post(
        "/api/events/",
        json={"page": "test_page", "description": "test_description"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == "test_page"
    assert data["description"] == "test_description"
    assert data["id"] is not None


def test_update_event():
    response = client.post(
        "/api/events/",
        json={"page": "test_page", "description": "test_description"},
    )
    event_id = response.json()["id"]

    response = client.put(
        f"/api/events/{event_id}",
        json={"description": "updated_description"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "updated_description"
