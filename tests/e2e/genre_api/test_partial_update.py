from uuid import uuid4

import pytest
from rest_framework.test import APIClient

from core.genre.domain import Genre


@pytest.mark.django_db
class TestPartiallyUpdateGenreView:
    def test_update_only_genre_name(self, genre_romance: Genre) -> None:
        response = APIClient().patch(
            f"/api/genres/{str(genre_romance.id)}/",
            {
                "name": "Another Genre",
            },
        )

        assert (response.status_code, response.data) == (200, {})

    def test_update_only_genre_description(self, genre_romance: Genre) -> None:
        response = APIClient().patch(
            f"/api/genres/{str(genre_romance.id)}/",
            {
                "description": "New description",
            },
        )

        assert (response.status_code, response.data) == (200, {})

    def test_update_name_and_description(self, genre_romance: Genre) -> None:
        response = APIClient().patch(
            f"/api/genres/{str(genre_romance.id)}/",
            data={
                "name": "Another Genre",
                "description": "New description",
            },
        )

        assert response.status_code == 200
        assert response.data == {}

    def test_when_genre_does_not_exist_then_return_404(self) -> None:
        genre_id = uuid4()

        response = APIClient().patch(
            f"/api/genres/{str(genre_id)}/",
            {
                "name": "Another Genre",
            },
        )

        assert response.status_code == 404
        assert response.data == {"message": f"Genre with id {genre_id} does not exist"}
