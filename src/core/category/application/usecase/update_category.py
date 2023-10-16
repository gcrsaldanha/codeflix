from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from core.category.application.usecase.exceptions import CategoryDoesNotExist, UpdateCategoryException
from core.category.domain import Category
from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface
from core.category.infrastructure.django_app.repositories import CategoryDjangoRepository


@dataclass
class UpdateCategoryRequest:  # TODO: Add validation so we do not even reach the domain layer
    category_id: UUID
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


@dataclass
class UpdateCategoryResponse:
    category: Category


class UpdateCategory:
    def __init__(self, category_repository: Optional[CategoryRepositoryInterface] = None):
        self.category_repository = category_repository or CategoryDjangoRepository()

    def execute(self, request: UpdateCategoryRequest) -> UpdateCategoryResponse:
        category = self.category_repository.get_by_id(request.category_id)
        if category is None:
            raise CategoryDoesNotExist(f"Category with id {request.category_id} does not exist")

        # Only update fields that are provided
        if request.name is None:
            request.name = category.name

        if request.description is None:
            request.description = category.description

        # Activating/deactivating category as a "separate" action on the domain object
        # If we want, we could extract this to another usecaes
        if request.is_active is None:
            request.is_active = category.is_active
        else:
            if request.is_active:
                category.activate()
            else:
                category.deactivate()

        category.change_category(request.name, request.description)  # TODO: monads / result
        if category.notification.has_errors():
            raise UpdateCategoryException(category.notification.errors)

        self.category_repository.update(category)

        return UpdateCategoryResponse(category)
