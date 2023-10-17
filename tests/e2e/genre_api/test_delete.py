from uuid import uuid4

import pytest
from rest_framework.test import APIClient

from core.genre.domain import Genre


@pytest.mark.django_db
class TestDeleteGenreView:
    def test_delete_genre(self, genre_romance: Genre) -> None:
        response = APIClient().delete(f"/api/genres/{str(genre_romance.id)}/")

        assert response.status_code == 204

    def test_when_genre_does_not_exist_then_return_404(self) -> None:
        genre_id = uuid4()

        response = APIClient().delete(f"/api/genres/{str(genre_id)}/")

        assert response.status_code == 404
        assert response.data == {"message": f"Genre with id {genre_id} does not exist"}
