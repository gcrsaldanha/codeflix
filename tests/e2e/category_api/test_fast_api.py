import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from core.category.infrastructure.fastapi_app.orm import metadata, start_mappers
from fastapi_project.main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite://"


def override_get_db():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    start_mappers()
    metadata.create_all(bind=engine)

    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# TODO: only because of conftest for now
# @pytest.mark.django_db
# def test_create_category():
#     # Arrange
#     payload = {"name": "Electronics", "description": "Category for electronics"}
#
#     # Act
#     response = client.post("/api/categories/", json=payload)
#
#     # Assert
#     assert response.status_code == 200
#     assert "id" in response.json()
#     created_id = response.json()["id"]
#     assert isinstance(created_id, str)  # UUIDs are serialized as strings


@pytest.mark.django_db
def test_get_category():
    # Arrange - First, we need a category to retrieve
    payload = {"name": "Electronics", "description": "Category for electronics"}
    create_response = client.post("/api/categories/", json=payload)
    created_id = create_response.json()["id"]

    # Act
    response = client.get(f"/api/categories/{created_id}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "id": created_id,
        "name": "Electronics",
        "description": "Category for electronics",
        "is_active": True
    }

# def test_get_category_not_found():
#     # Arrange - An arbitrary UUID that doesn't exist
#     non_existent_id = "12345678-1234-5678-1234-567812345678"
#
#     # Act
#     response = client.get(f"/api/categories/{non_existent_id}")
#
#     # Assert
#     assert response.status_code == 404
