from uuid import uuid4

import pytest

from core.category.application.usecase.delete_category import (
    DeleteCategoryRequest,
    DeleteCategory,
    DeleteCategoryResponse,
)
from core.category.application.usecase.exceptions import CategoryDoesNotExist
from core.category.domain import Category
from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface
from core.category.infrastructure.django_app.repositories import CategoryDjangoRepository


@pytest.fixture
def repository() -> CategoryRepositoryInterface:
    return CategoryDjangoRepository()


@pytest.mark.django_db
class TestDeleteCategory:
    def test_when_category_does_not_exist_then_raise_error(self):
        request = DeleteCategoryRequest(category_id=uuid4())
        use_case = DeleteCategory()

        with pytest.raises(CategoryDoesNotExist):
            use_case.execute(request)

    def test_when_category_exists_then_delete_it(self, repository: CategoryRepositoryInterface):
        category_id = uuid4()
        repository.create(Category(id=category_id, name="Drama", description="Category for drama"))

        request = DeleteCategoryRequest(category_id=category_id)
        use_case = DeleteCategory(category_repository=repository)

        response = use_case.execute(request)
        assert response == DeleteCategoryResponse(
            category=Category(id=category_id, name="Drama", description="Category for drama")
        )
        assert repository.get_by_id(category_id) is None
