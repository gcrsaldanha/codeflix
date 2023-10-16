from uuid import uuid4

import pytest

from core.category.application.usecase.get_category import GetCategoryRequest, GetCategory, GetCategoryResponse
from core.category.domain import Category
from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface
from core.category.infrastructure.django_app.repositories import CategoryDjangoRepository


@pytest.fixture
def repository() -> CategoryRepositoryInterface:
    return CategoryDjangoRepository()


@pytest.mark.django_db
class TestGetCategory:
    def test_when_category_exists_then_return_it(self, repository: CategoryRepositoryInterface):
        repository.create(Category(name="Drama", description="Category for drama"))
        existing_category_id = repository.get_all()[0].id

        request = GetCategoryRequest(category_id=existing_category_id)
        use_case = GetCategory().execute(request)

        assert use_case == GetCategoryResponse(
            category=Category(id=existing_category_id, name="Drama", description="Category for drama")
        )

    def test_when_category_does_not_exist_then_return_none(self):
        request = GetCategoryRequest(category_id=uuid4())
        use_case = GetCategory().execute(request)

        assert use_case == GetCategoryResponse(category=None)
