from unittest.mock import create_autospec

import pytest

from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface
from core.category.application.usecase.category.create_category import CreateCategory, CreateCategoryRequest


class TestCreateCategory:
    @pytest.fixture
    def category_repository(self) -> CategoryRepositoryInterface:
        return create_autospec(CategoryRepositoryInterface)

    def test_create_category_with_valid_data(self, category_repository: CategoryRepositoryInterface):
        request = CreateCategoryRequest(name="Drama", description="Category for drama")
        use_case = CreateCategory(category_repository=category_repository)

        response = use_case.execute(request)

        assert response.id
        assert category_repository.create.called  # Ensure it's being persisted
        assert category_repository.get_by_id(response.id)
