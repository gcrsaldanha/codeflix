from typing import Dict, List
from unittest.mock import create_autospec
from uuid import uuid4

import pytest

from core._shared.listing.orderer import Order
from core.category.domain.entity.category import Category
from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface
from core.category.application.usecase.list_categories import (
    ListCategories,
    ListCategoriesRequest,
    ListCategoriesResponse,
)
from core.category.infrastructure.django_app.repositories import CategoryDjangoRepository
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
    paginated_request = ListCategoriesRequest(
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
    paginated_request = ListCategoriesRequest(
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
    response = use_case.execute(ListCategoriesRequest())

    assert response.data == [
        category_2,
        category_1,
    ]


@pytest.mark.django_db
class TestListCategories:
    # TODO: This is an integration test, also this is mostly testing Paginator and Repository.
    @pytest.fixture
    def category_drama(self) -> Category:
        return Category(name="Drama", description="Category for drama")

    @pytest.fixture
    def category_action(self) -> Category:
        return Category(name="Action", description="Category for action")

    @pytest.fixture
    def category_romance(self) -> Category:
        return Category(name="Romance", description="Category for romance")

    @pytest.fixture(autouse=True)
    def repository(self, category_drama, category_action, category_romance) -> CategoryRepositoryInterface:
        repo = CategoryDjangoRepository()
        repo.create(category_drama)
        repo.create(category_action)
        repo.create(category_romance)
        return repo

    def test_order_by_name_asc(
        self,
        category_drama: Category,
        category_action: Category,
        category_romance: Category,
    ):
        request = ListCategoriesRequest(
            order_by={"name": Order.ASC},
        )

        use_case = ListCategories()
        response = use_case.execute(request)

        assert response == ListCategoriesResponse(
            data=[
                category_action,
                category_drama,
                category_romance,
            ],
            next_page=None,
            page=1,
            total_quantity=3,
        )

    def test_order_by_name_desc(
        self,
        category_drama: Category,
        category_action: Category,
        category_romance: Category,
    ) -> None:
        request = ListCategoriesRequest(
            order_by={"name": Order.DESC},
        )

        use_case = ListCategories()
        response = use_case.execute(request)

        assert response == ListCategoriesResponse(
            data=[
                category_romance,
                category_drama,
                category_action,
            ],
            next_page=None,
            page=1,
            total_quantity=3,
        )

    def test_filter_by_name(self, category_drama: Category) -> None:
        request = ListCategoriesRequest(
            filters={"name": category_drama.name},
        )
        use_case = ListCategories()

        response = use_case.execute(request)

        assert response == ListCategoriesResponse(
            data=[category_drama],
            next_page=None,
            page=1,
            total_quantity=1,
        )

    def test_filter_by_description(self, category_drama: Category) -> None:
        request = ListCategoriesRequest(
            filters={"description": category_drama.description},
        )
        use_case = ListCategories()

        response = use_case.execute(request)

        assert response == ListCategoriesResponse(
            data=[category_drama],
            next_page=None,
            page=1,
            total_quantity=1,
        )

    def test_paginate_very_large_request(self, repository: CategoryRepositoryInterface) -> None:
        for i in range(150):
            repository.create(Category(name=f"Category {i}", description=f"Category {i} description"))

        request = ListCategoriesRequest(
            page=1,
            page_size=1000,
        )
        use_case = ListCategories()

        response = use_case.execute(request)

        assert len(response.data) == 100
        assert response.next_page == 2
        assert response.page == 1
        assert response.total_quantity >= 150
