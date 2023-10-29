from uuid import uuid4

import pytest
from rest_framework.test import APIClient

from core.genre.domain import Genre


@pytest.mark.django_db
class TestGetGenreView:
    def test_return_genre(self, genre_romance: Genre) -> None:
        response = APIClient().get(f"/api/genres/{str(genre_romance.id)}/")

        assert response.status_code == 200
        assert response.data == {
            "data": {
                "id": str(genre_romance.id),
                "name": genre_romance.name,
                "description": genre_romance.description,
                "is_active": genre_romance.is_active,
                "categories": [str(category) for category in genre_romance.categories],
            },
        }

    def test_return_404_if_genre_does_not_exist(self) -> None:
        genre_id = uuid4()

        response = APIClient().get(f"/api/genres/{str(genre_id)}/")

        assert response.status_code == 404
        assert response.data == {"message": "Genre not found"}

    def test_return_400_if_request_is_malformed(self) -> None:
        response = APIClient().get("/api/genres/invalid/")

        assert response.status_code == 400
        assert response.data == {"genre_id": ["Must be a valid UUID."]}
