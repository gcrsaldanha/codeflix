import pytest

from core._shared.notification.notification_error import NotificationException
from core.category.application.usecase.create_category import (
    CreateCategoryRequest,
    CreateCategory,
    CreateCategoryResponse,
)
from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface
from core.category.infrastructure.django_app.repositories import CategoryDjangoRepository


@pytest.fixture
def repository() -> CategoryRepositoryInterface:
    return CategoryDjangoRepository()


@pytest.mark.django_db
class TestCreateCategory:
    def test_create_category_with_name_and_description(self, repository: CategoryRepositoryInterface):
        request = CreateCategoryRequest(
            name="Drama",
            description="Category for drama",
        )

        use_case = CreateCategory(category_repository=repository)
        response = use_case.execute(request)

        assert response == CreateCategoryResponse(
            id=response.id,
        )
        assert repository.get_all()[0].id == response.id

    def test_when_category_is_created_with_invalid_arguments_then_raise_notification(self, repository):
        # TODO: should this be tested here as well? Should it be a request validation?
        request = CreateCategoryRequest(
            name="",
            description="a" * 1025,
        )

        use_case = CreateCategory(category_repository=repository)

        with pytest.raises(NotificationException, match="category: Category name cannot be empty") as err:
            use_case.execute(request)
