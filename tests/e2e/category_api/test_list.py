import pytest
from django.conf import settings
from rest_framework.test import APIClient

from core.category.domain import Category


@pytest.mark.django_db
class TestListCategoriesView:
    def test_list_categories(self, category: Category, category_2: Category) -> None:
        api_client = APIClient()
        response = api_client.get("/api/categories/")

        assert response.status_code == 200
        assert response.data == {
            "data": [
                {
                    "id": str(category.id),
                    "name": "Category 1",
                    "description": "Category 1 description",
                    "is_active": True,
                },
                {
                    "id": str(category_2.id),
                    "name": "Category 2",
                    "description": "Category 2 description",
                    "is_active": True,
                },
            ],
            "next_page": None,
            "page": 1,
            "page_size": settings.DEFAULT_PAGE_SIZE,
            "total_quantity": 2,
        }

    def test_list_categories_with_pagination(
        self,
        category: Category,
        category_2: Category,
    ) -> None:
        api_client = APIClient()
        response = api_client.get("/api/categories/?page=1&page_size=1")

        assert response.data == {
            "data": [
                {
                    "id": str(category.id),
                    "name": "Category 1",
                    "description": "Category 1 description",
                    "is_active": True,
                },
            ],
            "next_page": 2,
            "page": 1,
            "page_size": 1,
            "total_quantity": 2,
        }
        assert response.status_code == 200
