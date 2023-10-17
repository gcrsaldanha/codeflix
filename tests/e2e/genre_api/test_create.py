import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestCreateGenreView:
    def test_create_genre_with_post_payload_data(self, category_1) -> None:
        response = APIClient().post(
            "/api/genres/",
            data={
                "name": "Action",
                "description": "Genre for action",
                "categories": [str(category_1.id)],
            },
        )

        assert response.status_code == 201
        assert response.data == {"id": response.data["id"]}
