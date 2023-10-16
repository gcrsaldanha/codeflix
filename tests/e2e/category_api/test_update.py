from typing import Dict
from uuid import uuid4

import pytest
from rest_framework.test import APIClient

from core.category.domain import Category


@pytest.mark.django_db
class TestUpdateCategoryView:
    def test_when_category_exists_then_update_it(self, category: Category) -> None:
        response = APIClient().put(
            f"/api/categories/{str(category.id)}/",
            {
                "name": "Category 2",
                "description": "Category 2 description",
                "is_active": "true",
            },
        )

        assert response.status_code == 200
        assert response.data == {
            "data": {
                "id": str(category.id),
                "name": "Category 2",
                "description": "Category 2 description",
                "is_active": True,
            }
        }

    def test_when_category_does_not_exist_then_return_404(self) -> None:
        category_id = uuid4()

        response = APIClient().put(
            f"/api/categories/{str(category_id)}/",
            {
                "name": "Category 2",
                "description": "Category 2 description",
                "is_active": "true",
            },
        )

        assert response.status_code == 404
        assert response.data == {"message": f"Category with id {category_id} does not exist"}

    def test_update_name_and_empty_description(self, category: Category) -> None:
        response = APIClient().put(
            f"/api/categories/{str(category.id)}/",
            {
                "name": "Category 2",
                "description": "",
                "is_active": "true",
            },
        )

        assert response.status_code == 200
        assert response.data == {
            "data": {
                "id": str(category.id),
                "name": "Category 2",
                "description": "",
                "is_active": True,
            }
        }

    def test_deactivate_category(self, category: Category) -> None:
        response = APIClient().put(
            f"/api/categories/{str(category.id)}/",
            {
                "name": "Category 2",
                "description": "",
                "is_active": "false",
            },
        )

        assert response.status_code == 200
        assert response.data == {
            "data": {
                "id": str(category.id),
                "name": "Category 2",
                "description": "",
                "is_active": False,
            }
        }


    @pytest.mark.parametrize(
        "payload",
        [
            {"name": "Category 2"},
            {"description": "Category 2 description"},
            {"is_active": "true"},
        ],
    )
    def test_all_fields_keys_must_be_provided(self, payload: Dict[str, str], category: Category) -> None:
        response = APIClient().put(
            f"/api/categories/{str(category.id)}/",
            payload,
        )

        assert response.status_code == 400
