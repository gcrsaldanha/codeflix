from uuid import uuid4

import pytest

from core.genre.application.usecase.delete_genre_use_case import (
    DeleteGenreInput,
    DeleteGenreUseCase,
)
from core.genre.application.usecase.exceptions import GenreDoesNotExist
from core.genre.domain import Genre
from core.genre.infrastructure.mocks.genre_fake_repository import GenreFakeRepository


def test_when_genre_does_not_exist_then_raise_error():
    repository = GenreFakeRepository(genres=set())

    delete_genre = DeleteGenreUseCase(repository)
    request = DeleteGenreInput(genre_id=uuid4())

    with pytest.raises(GenreDoesNotExist, match=f"Genre with id {request.genre_id} does not exist"):
        delete_genre.execute(request)


def test_delete_existing_genre():
    genre = Genre(id=uuid4(), name="Drama", description="Genre for drama")
    repository = GenreFakeRepository(genres={genre})
    assert repository.get_by_id(genre.id) is not None

    delete_genre = DeleteGenreUseCase(repository)
    request = DeleteGenreInput(genre_id=genre.id)
    response = delete_genre.execute(request)

    assert response.genre == genre
    assert repository.get_by_id(genre.id) is None
