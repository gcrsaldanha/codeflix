from typing import Dict
from uuid import uuid4

import pytest
from rest_framework.test import APIClient

from core.genre.domain import Genre


@pytest.mark.django_db
class TestUpdateGenreView:
    def test_when_genre_exists_then_update_it(self, genre_romance: Genre) -> None:
        response = APIClient().put(
            f"/api/genres/{str(genre_romance.id)}/",
            {
                "name": "New Romance",
                "description": "New description",
                "is_active": False,
            }
        )

        assert response.status_code == 200
        assert response.data == {
            "data": {
                "id": str(genre_romance.id),
                "name": "New Romance",
                "description": "New description",
                "is_active": False,
                "categories": [str(category) for category in genre_romance.categories],
            }
        }

    def test_when_genre_does_not_exist_then_return_404(self) -> None:
        genre_id = uuid4()

        response = APIClient().put(
            f"/api/genres/{str(genre_id)}/",
            {
                "name": "Johnny Doe",
                "description": "New description",
                "is_active": False,
            },
        )

        assert response.status_code == 404
        assert response.data == {"message": f"Genre with id {genre_id} does not exist"}

    @pytest.mark.parametrize(
        "payload",
        [
            {"name": "New Romance"},
            {"description": "New description"},
            {"is_active": False},
        ],
    )
    def test_all_fields_keys_must_be_provided(self, payload: Dict[str, str], genre_romance: Genre) -> None:
        response = APIClient().put(
            f"/api/genres/{str(genre_romance.id)}/",
            payload,
        )

        assert response.status_code == 400
