import pytest

from core.category.domain import Category
from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface
from core.category.infrastructure.django_app.repositories import CategoryDjangoRepository
from core.genre.domain import Genre
from core.genre.domain.repository.genre_repository_interface import GenreRepositoryInterface
from core.genre.infrastructure.genre_django_app.repositories import GenreDjangoRepository


@pytest.fixture(scope="function")
def category_drama() -> Category:
    return Category(
        name="Drama",
        description="Category for drama",
    )


@pytest.fixture(scope="function")
def category_action() -> Category:
    return Category(
        name="Action",
        description="Category for action",
    )


@pytest.fixture(scope="function", autouse=True)
def category_repository(category_drama: Category, category_action: Category) -> CategoryRepositoryInterface:
    repository = CategoryDjangoRepository()
    repository.create(category_drama)
    repository.create(category_action)
    return repository


@pytest.fixture(scope="function")
def genre_romance(category_drama) -> Genre:
    return Genre(
        name="Romance",
        description="Genre for romance",
        categories={category_drama.id},
    )


@pytest.fixture(scope="function")
def genre_comedy(category_drama, category_action) -> Genre:
    return Genre(
        name="Comedy",
        description="Genre for comedy",
        categories={category_drama.id, category_action.id},
    )


@pytest.fixture(scope="function", autouse=True)
def genre_repository(genre_romance: Genre, genre_comedy: Genre) -> GenreRepositoryInterface:
    repository = GenreDjangoRepository()
    repository.create(genre_romance)
    repository.create(genre_comedy)
    return repository
