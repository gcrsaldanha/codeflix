from uuid import uuid4

from core.category.domain import Category
from core.genre.application.usecase.get_genre_use_case import GetGenreUseCase, GetGenreInput
from core.genre.domain import Genre
from core.genre.infrastructure.mocks.genre_fake_repository import GenreFakeRepository


def test_when_genre_does_not_exist_then_return_none():
    genre_repository = GenreFakeRepository(genres=set())

    use_case = GetGenreUseCase(repository=genre_repository)
    request = GetGenreInput(genre_id=uuid4())
    response = use_case.execute(request)

    assert response.genre is None


def test_get_genre_by_id():
    category = Category(id=uuid4(), name="Drama", description="Category for drama")
    genre = Genre(id=uuid4(), name="Drama", description="Genre for drama", categories=[])
    genre_2 = Genre(id=uuid4(), name="Action", description="Genre for action", categories=[category])
    genre_repository = GenreFakeRepository(genres={genre, genre_2})

    use_case = GetGenreUseCase(repository=genre_repository)
    request = GetGenreInput(genre_id=genre_2.id)
    response = use_case.execute(request)

    assert response.genre == genre_2
    assert response.genre.categories == [category]
