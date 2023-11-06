from uuid import uuid4

import pytest

from core.category.domain import Category
from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface
from core.category.infrastructure.django_app.repositories import CategoryDjangoRepository
from core.category.infrastructure.fastapi_app.category_sqlalchemy_repository import CategorySQLAlchemyRepository


@pytest.fixture(scope="function")
def category() -> Category:
    return Category(
        id=uuid4(),
        name="Category 1",
        description="Category 1 description",
        is_active=True,
    )


@pytest.fixture(scope="function")
def category_2() -> Category:
    return Category(
        id=uuid4(),
        name="Category 2",
        description="Category 2 description",
        is_active=True,
    )


@pytest.fixture(scope="function", autouse=True)
def category_repository(category: Category, category_2: Category) -> CategoryRepositoryInterface:
    category_repository = CategoryDjangoRepository()
    category_repository.create(category)
    category_repository.create(category_2)
    return category_repository
