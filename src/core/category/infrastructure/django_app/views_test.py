from uuid import uuid4

import pytest
from rest_framework.test import APIClient

from core.category.domain import Category
from core.category.infrastructure.django_app.repositories import CategoryDjangoRepository


@pytest.mark.django_db
class TestListCategoryView:
    def test_get(self):
        api_client = APIClient()

        # TODO: repository or use case?
        category_id = uuid4()
        categories_repository = CategoryDjangoRepository()
        categories_repository.create(
            Category(
                id=category_id,
                name="Category 1",
                description="Category 1 description",
                is_active=True,
            )
        )

        response = api_client.get("/api/categories/")

        assert response.status_code == 200
        assert response.data == [
            {
                "id": str(category_id),
                "name": "Category 1",
                "description": "Category 1 description",
                "is_active": True,
            }
        ]
