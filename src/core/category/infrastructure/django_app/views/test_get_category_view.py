from uuid import uuid4

import pytest
from rest_framework.test import APIClient

from core.category.domain import Category
from core.category.infrastructure.django_app.repositories import CategoryDjangoRepository


@pytest.mark.django_db
class TestGetCategoryView:
    def test_return_category(self) -> None:
        category_repository = CategoryDjangoRepository()
        category_id = uuid4()
        category_repository.create(
            Category(
                id=category_id,
                name="Category 1",
                description="Category 1 description",
                is_active=True,
            )
        )

        response = APIClient().get(f"/api/categories/{str(category_id)}/")

        assert response.status_code == 200
        assert response.data == {
            "id": str(category_id),
            "name": "Category 1",
            "description": "Category 1 description",
            "is_active": True,
        }

    def test_return_404_if_category_does_not_exist(self) -> None:
        category_id = uuid4()

        response = APIClient().get(f"/api/categories/{str(category_id)}/")

        assert response.status_code == 404
        assert response.data == {"message": "Category not found"}

    def test_return_400_if_request_is_malformed(self) -> None:
        response = APIClient().get("/api/categories/invalid/")

        assert response.status_code == 400
        assert response.data == {"category_id": ["Must be a valid UUID."]}
