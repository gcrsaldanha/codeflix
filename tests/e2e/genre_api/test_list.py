import pytest
from rest_framework.test import APIClient

from core.genre.domain import Genre


@pytest.mark.django_db
class TestListGenresView:
    def test_list_genres(self, genre_comedy: Genre, genre_romance: Genre) -> None:
        api_client = APIClient()
        response = api_client.get("/api/genres/")

        assert response.status_code == 200
        assert response.data == {
            "data": [
                {
                    "id": str(genre_comedy.id),
                    "name": genre_comedy.name,
                    "description": genre_comedy.description,
                    "categories": [str(category.id) for category in genre_comedy.categories],
                },
                {
                    "id": str(genre_romance.id),
                    "name": genre_romance.name,
                    "description": genre_romance.description,
                    "categories": [str(category.id) for category in genre_romance.categories],
                }
            ],
            "meta": {
                "next_page": None,
                "page": 1,
                "page_size": 2,
                "total_quantity": 2,
            },
        }

    def test_list_genres_with_pagination(
        self,
        genre_comedy: Genre,
        genre_romance: Genre,
    ) -> None:
        api_client = APIClient()
        response = api_client.get("/api/genres/?page=1&page_size=1")

        assert response.data == {
            "data": [
                {
                    "id": str(genre_comedy.id),
                    "name": genre_comedy.name,
                    "description": genre_comedy.description,
                    "categories": [str(category.id) for category in genre_comedy.categories],
                },
            ],
            "meta": {
                "next_page": 2,
                "page": 1,
                "page_size": 1,
                "total_quantity": 2,
            },
        }
        assert response.status_code == 200
