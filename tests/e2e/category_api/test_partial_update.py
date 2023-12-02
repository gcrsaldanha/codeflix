from uuid import uuid4

import pytest
from rest_framework.test import APIClient

from core.category.domain import Category


@pytest.mark.django_db
class TestPartiallyUpdateCategoryView:
    def test_update_only_category_name(self, category: Category) -> None:
        response = APIClient().patch(
            f"/api/categories/{str(category.id)}/",
            {
                "name": "Category 2",
            },
        )

        assert (response.status_code, response.data) == (200, {})

    def test_update_only_category_description(self, category: Category) -> None:
        response = APIClient().patch(
            f"/api/categories/{str(category.id)}/",
            {
                "description": "Category 2 description",
            },
        )

        assert (response.status_code, response.data) == (200, {})

    def test_update_name_and_description(self, category: Category) -> None:
        response = APIClient().patch(
            f"/api/categories/{str(category.id)}/",
            {
                "name": "Category 2",
                "description": "Category 2 description",
            },
        )

        assert response.status_code == 200
        assert response.data == {}

    def test_when_category_does_not_exist_then_return_404(self) -> None:
        category_id = uuid4()

        response = APIClient().patch(
            f"/api/categories/{str(category_id)}/",
            {
                "name": "Category 2",
                "description": "Category 2 description",
            },
        )

        assert response.status_code == 404
        assert response.data == {"message": f"Category with id {category_id} does not exist"}
