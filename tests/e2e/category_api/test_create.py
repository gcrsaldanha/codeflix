import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestCreateCategoryView:
    def test_create_category_with_post_payload_data(self) -> None:
        response = APIClient().post(
            "/api/categories/",
            data={
                "name": "Category 1",
                "description": "Category 1 description",
            },
        )

        assert response.status_code == 201
        assert response.data == {"id": response.data["id"]}
