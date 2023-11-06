import pytest

from core.category.domain import Category
from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface
from core.category.infrastructure.django_app.repositories import CategoryDjangoRepository
from core.genre.application.usecase.create_genre_use_case import CreateGenreUseCase, CreateGenreInput
from core.genre.domain.repository.genre_repository_interface import GenreRepositoryInterface
from core.genre.infrastructure.genre_django_app.repositories import GenreDjangoRepository


@pytest.fixture
def genre_repository() -> GenreRepositoryInterface:
    return GenreDjangoRepository()


@pytest.fixture
def category_repository() -> CategoryRepositoryInterface:
    return CategoryDjangoRepository()


@pytest.fixture
def category_documentary() -> Category:
    return Category(name="Documentary", description="Documentary category")


@pytest.fixture
def category_popular() -> Category:
    return Category(name="Popular", description="Popular category")


@pytest.mark.django_db
class TestCreateGenreWithCategories:
    def test_when_categories_exist_then_create_genre_with_categories(
        self,
        category_popular,
        category_documentary,
        category_repository,
        genre_repository,
    ) -> None:
        category_repository.create(category_popular)
        category_repository.create(category_documentary)

        use_case = CreateGenreUseCase()
        request = CreateGenreInput(
            name="Genre 1",
            description="Genre 1 description",
            categories={
                category_popular.id,
                category_documentary.id,
            },
        )
        output = use_case.execute(request)

        created_genre = genre_repository.get_by_id(output.id)
        assert output.id == created_genre.id
        assert created_genre.categories == {category_popular.id, category_documentary.id}

    def test_when_categories_do_not_exist_then_create_genre_without_categories(
        self,
        category_repository,
        genre_repository,
    ) -> None:
        use_case = CreateGenreUseCase()
        request = CreateGenreInput(
            name="Genre 1",
            description="Genre 1 description",
            categories=set(),
        )
        output = use_case.execute(request)

        created_genre = genre_repository.get_by_id(output.id)
        assert output.id == created_genre.id
        assert created_genre.categories == set()
