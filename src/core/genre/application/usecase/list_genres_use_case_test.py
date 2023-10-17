from uuid import uuid4

import pytest

from core.category.domain import Category
from core.genre.application.usecase.list_genres_use_case import (
    ListGenresInput,
    ListGenresUseCase,
)
from core.genre.domain.entity.genre import Genre
from core.genre.domain.repository.genre_repository_interface import GenreRepositoryInterface
from core.genre.infrastructure.mocks.genre_fake_repository import GenreFakeRepository


@pytest.fixture
def category_1() -> Category:
    return Category(id=uuid4(), name="Category 1", description="Category 1 description")


@pytest.fixture
def genre_drama(category_1: Category) -> Genre:
    return Genre(id=uuid4(), name="Drama", categories=[category_1])


@pytest.fixture
def genre_romance() -> Genre:
    return Genre(id=uuid4(), name="Romance")


@pytest.fixture
def repository(genre_drama, genre_romance) -> GenreRepositoryInterface:
    repo = GenreFakeRepository(
        genres={
            genre_drama,
            genre_romance,
        }
    )
    return repo


def test_list_genres_ordered_by_name_page_one(
    repository,
    genre_drama,
    genre_romance,
):
    use_case = ListGenresUseCase(repository=repository)
    paginated_request = ListGenresInput(
        page=1,
        page_size=2,
    )
    response = use_case.execute(paginated_request)

    assert response.data == [
        genre_drama,
        genre_romance,
    ]
    assert response.meta.next_page == None
    assert response.meta.page == 1
    assert response.meta.total_quantity == 2


def test_list_genres_ordered_by_name_page_two(
    repository,
    genre_drama,
    genre_romance,
):
    use_case = ListGenresUseCase(repository=repository)
    paginated_request = ListGenresInput(
        page=2,
        page_size=1,
    )
    response = use_case.execute(paginated_request)
    assert response.data == [
        genre_romance,
    ]
    assert response.meta.next_page is None
    assert response.meta.page == 2
    assert response.meta.total_quantity == 2


def test_list_romance_only(
    repository,
    genre_drama,
    genre_romance,
):
    use_case = ListGenresUseCase(repository=repository)
    paginated_request = ListGenresInput(
        page=1,
        page_size=2,
        filters={"name": "Romance"},
    )
    response = use_case.execute(paginated_request)
    assert response.data == [
        genre_romance,
    ]
    assert response.meta.next_page is None
    assert response.meta.page == 1
    assert response.meta.total_quantity == 1
