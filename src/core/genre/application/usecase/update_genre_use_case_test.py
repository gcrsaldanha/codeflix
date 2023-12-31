from uuid import uuid4

import pytest

from core.genre.application.usecase.update_genre_use_case import (
    UpdateGenreUseCase,
    UpdateGenreInput,
)
from core.genre.application.usecase.exceptions import GenreDoesNotExist
from core.genre.domain import Genre
from core.genre.infrastructure.mocks.genre_fake_repository import GenreFakeRepository


def test_when_genre_does_not_exist_then_raises_exception():
    request = UpdateGenreInput(genre_id=uuid4(), name="Romance")
    repository = GenreFakeRepository(genres=set())

    use_case = UpdateGenreUseCase(repository=repository)

    with pytest.raises(GenreDoesNotExist, match=f"Genre with id {request.genre_id} does not exist"):
        use_case.execute(request)


def test_update_genre_name_only():
    existing_genre = Genre(id=uuid4(), name="Romance")
    repository = GenreFakeRepository(genres={existing_genre})

    request = UpdateGenreInput(genre_id=existing_genre.id, name="Drama")
    use_case = UpdateGenreUseCase(repository=repository)
    response = use_case.execute(request)

    assert response.genre.id == existing_genre.id
    assert response.genre.name == "Drama"


def test_update_genre_description_only():
    existing_genre = Genre(id=uuid4(), name="Romance", description="Romance description")
    repository = GenreFakeRepository(genres={existing_genre})

    request = UpdateGenreInput(genre_id=existing_genre.id, description="Drama description")
    use_case = UpdateGenreUseCase(repository=repository)
    response = use_case.execute(request)

    assert response.genre.id == existing_genre.id
    assert response.genre.name == "Romance"
    assert response.genre.description == "Drama description"


def test_update_genre_name_and_description():
    existing_genre = Genre(id=uuid4(), name="Romance", description="Romance description")
    repository = GenreFakeRepository(genres={existing_genre})

    request = UpdateGenreInput(
        genre_id=existing_genre.id,
        name="Drama",
        description="Drama description",
    )
    use_case = UpdateGenreUseCase(repository=repository)
    response = use_case.execute(request)

    assert response.genre.id == existing_genre.id
    assert response.genre.name == "Drama"
    assert response.genre.description == "Drama description"


def test_activate_genre():
    existing_genre = Genre(id=uuid4(), name="Romance", description="Romance description", is_active=False)
    repository = GenreFakeRepository(genres={existing_genre})

    request = UpdateGenreInput(genre_id=existing_genre.id, is_active=True)
    use_case = UpdateGenreUseCase(repository=repository)
    response = use_case.execute(request)

    assert response.genre.id == existing_genre.id
    assert response.genre.is_active is True


def test_deactivate_genre():
    existing_genre = Genre(id=uuid4(), name="Romance", description="Romance description", is_active=True)
    repository = GenreFakeRepository(genres={existing_genre})

    request = UpdateGenreInput(genre_id=existing_genre.id, is_active=False)
    use_case = UpdateGenreUseCase(repository=repository)
    response = use_case.execute(request)

    assert response.genre.id == existing_genre.id
    assert response.genre.is_active is False
