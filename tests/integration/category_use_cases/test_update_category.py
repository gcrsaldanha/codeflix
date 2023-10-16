from uuid import uuid4

import pytest

from core.category.application.usecase.exceptions import CategoryDoesNotExist
from core.category.application.usecase.update_category import (
    UpdateCategory,
    UpdateCategoryRequest,
    UpdateCategoryResponse,
)
from core.category.domain import Category
from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface
from core.category.infrastructure.django_app.repositories import CategoryDjangoRepository


@pytest.fixture
def repository() -> CategoryRepositoryInterface:
    return CategoryDjangoRepository()


@pytest.mark.django_db
class TestUpdateCategory:
    def test_when_category_does_not_exist_then_raise_error(self):
        request = UpdateCategoryRequest(category_id=uuid4())
        use_case = UpdateCategory()

        with pytest.raises(CategoryDoesNotExist):
            use_case.execute(request)

    def test_when_category_exists_then_update_it(self, repository: CategoryRepositoryInterface):
        category_id = uuid4()
        repository.create(Category(id=category_id, name="Drama", description="Category for drama"))

        request = UpdateCategoryRequest(category_id=category_id, name="Comedy")
        use_case = UpdateCategory(category_repository=repository)

        response = use_case.execute(request)
        assert response == UpdateCategoryResponse(
            category=Category(id=category_id, name="Comedy", description="Category for drama")
        )
        db_category = repository.get_by_id(category_id)
        assert db_category == Category(id=category_id, name="Comedy", description="Category for drama")
