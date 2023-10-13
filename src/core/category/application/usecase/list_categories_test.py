from unittest.mock import create_autospec
from uuid import uuid4

import pytest

from core.category.application.usecase.list_categories import (
    ListCategories,
    ListCategoriesInput,
)
from core.category.domain.entity.category import Category
from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface
from core.category.infrastructure.mocks.category_fake_repository import CategoryFakeRepository


@pytest.fixture
def category_drama() -> Category:
    return Category(id=uuid4(), name="Drama", description="Category for drama")


@pytest.fixture
def category_action() -> Category:
    return Category(id=uuid4(), name="Action", description="Category for action")


@pytest.fixture
def category_romance() -> Category:
    return Category(id=uuid4(), name="Romance", description="Category for romance")


@pytest.fixture
def repository(category_drama, category_action, category_romance) -> CategoryRepositoryInterface:
    repo = create_autospec(CategoryRepositoryInterface)
    repo.get_all.return_value = [
        category_drama,
        category_action,
        category_romance,
    ]
    return repo


def test_list_categories_ordered_by_name_page_one(
    repository,
    category_drama,
    category_action,
    category_romance,
):
    use_case = ListCategories(category_repository=repository)
    paginated_request = ListCategoriesInput(
        page=1,
        page_size=2,
    )
    response = use_case.execute(paginated_request)

    assert response.data == [
        category_action,
        category_drama,
    ]
    assert response.next_page == 2
    assert response.page == 1
    assert response.total_quantity == 3


def test_list_categories_ordered_by_name_page_two(
    repository,
    category_drama,
    category_action,
    category_romance,
):
    use_case = ListCategories(category_repository=repository)
    paginated_request = ListCategoriesInput(
        page=2,
        page_size=2,
    )
    response = use_case.execute(paginated_request)
    assert response.data == [
        category_romance,
    ]
    assert response.next_page is None
    assert response.page == 2
    assert response.total_quantity == 3


def test_list_all_categories_ordered_by_name_using_fake_repository():
    category_1 = Category(name="Drama", description="Category for drama")
    category_2 = Category(name="Action", description="Category for action")

    fake_repository = CategoryFakeRepository(categories={category_1, category_2})

    use_case = ListCategories(category_repository=fake_repository)
    response = use_case.execute(ListCategoriesInput())

    assert response.data == [
        category_2,
        category_1,
    ]
