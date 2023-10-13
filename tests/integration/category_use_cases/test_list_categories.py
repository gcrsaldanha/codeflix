import pytest

from core._shared.listing.orderer import Order
from core.category.application.usecase.list_categories import ListCategoriesInput, ListCategories, ListCategoriesOutput
from core.category.domain import Category
from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface
from core.category.infrastructure.django_app.repositories import CategoryDjangoRepository


@pytest.mark.django_db
class TestListCategories:
    # TODO: this is mostly testing the pagination/ordering/filtering using a real database.
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
        request = ListCategoriesInput(
            order_by={"name": Order.ASC},
        )

        use_case = ListCategories()
        response = use_case.execute(request)

        assert response == ListCategoriesOutput(
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
        request = ListCategoriesInput(
            order_by={"name": Order.DESC},
        )

        use_case = ListCategories()
        response = use_case.execute(request)

        assert response == ListCategoriesOutput(
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
        request = ListCategoriesInput(
            filters={"name": category_drama.name},
        )
        use_case = ListCategories()

        response = use_case.execute(request)

        assert response == ListCategoriesOutput(
            data=[category_drama],
            next_page=None,
            page=1,
            total_quantity=1,
        )

    def test_filter_by_description(self, category_drama: Category) -> None:
        request = ListCategoriesInput(
            filters={"description": category_drama.description},
        )
        use_case = ListCategories()

        response = use_case.execute(request)

        assert response == ListCategoriesOutput(
            data=[category_drama],
            next_page=None,
            page=1,
            total_quantity=1,
        )

    def test_paginate_very_large_request(self, repository: CategoryRepositoryInterface) -> None:
        for i in range(150):
            repository.create(Category(name=f"Category {i}", description=f"Category {i} description"))

        request = ListCategoriesInput(
            page=1,
            page_size=1000,
        )
        use_case = ListCategories()

        response = use_case.execute(request)

        assert len(response.data) == 100
        assert response.next_page == 2
        assert response.page == 1
        assert response.total_quantity >= 150
