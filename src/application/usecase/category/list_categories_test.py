from unittest.mock import create_autospec
from uuid import uuid4

import pytest

from domain.category.entity.category import Category
from domain.category.repository.category_repository_interface import CategoryRepositoryInterface
from application.usecase.category.list_categories import ListCategories, ListCategoriesRequest
from infrastructure.db.repository.fake_category_repository import FakeCategoryRepository


@pytest.fixture
def repository() -> CategoryRepositoryInterface:
    return create_autospec(CategoryRepositoryInterface)


# Just demonstrating that we do not need to make classes for tests
def test_list_all_categories_ordered_by_name(repository: CategoryRepositoryInterface):
    category_id_1 = uuid4()
    category_id_2 = uuid4()

    category_1 = Category(id=category_id_1, name="Drama", description="Category for drama")
    category_2 = Category(id=category_id_2, name="Action", description="Category for action")

    repository.get_all.return_value = iter([
        category_1,
        category_2,
    ])

    use_case = ListCategories(category_repository=repository)
    response = use_case.execute(ListCategoriesRequest())

    assert response.categories == [
        category_2,
        category_1,
    ]


def test_list_all_categories_ordered_by_name_using_fake_repository():
    category_1 = Category(name="Drama", description="Category for drama")
    category_2 = Category(name="Action", description="Category for action")

    fake_repository = FakeCategoryRepository(categories={category_1, category_2})

    use_case = ListCategories(category_repository=fake_repository)
    response = use_case.execute(ListCategoriesRequest())

    assert response.categories == [
        category_2,
        category_1,
    ]
