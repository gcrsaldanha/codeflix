import pytest

from core.category.domain import Category
from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface
from core.category.infrastructure.django_app.repositories import CategoryDjangoRepository
from core.genre.domain import Genre
from core.genre.domain.repository.genre_repository_interface import GenreRepositoryInterface
from core.genre.infrastructure.genre_django_app.repositories import GenreDjangoRepository


@pytest.fixture(scope="function")
def category_1() -> Category:
    return Category(
        name="Drama",
        description="Category for drama",
    )


@pytest.fixture(scope="function")
def category_2() -> Category:
    return Category(
        name="Action",
        description="Category for action",
    )


@pytest.fixture(scope="function", autouse=True)
def category_repository(category_1: Category, category_2: Category) -> CategoryRepositoryInterface:
    repository = CategoryDjangoRepository()
    repository.create(category_1)
    repository.create(category_2)
    return repository


@pytest.fixture(scope="function")
def genre_romance(category_1) -> Genre:
    return Genre(
        name="Romance",
        description="Genre for romance",
        categories=[category_1],
    )


@pytest.fixture(scope="function")
def genre_comedy(category_1, category_2) -> Genre:
    return Genre(
        name="Comedy",
        description="Genre for comedy",
        categories=[category_1, category_2],
    )


@pytest.fixture(scope="function", autouse=True)
def genre_repository(genre_romance: Genre, genre_drama: Genre) -> GenreRepositoryInterface:
    repository = GenreDjangoRepository()
    repository.create(genre_romance)
    repository.create(genre_drama)
    return repository
