from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from core.category.domain import Category
from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface


@dataclass
class UpdateCategoryRequest:  # TODO: Add validation so we do not even reach the domain layer
    category_id: UUID
    name: Optional[str] = None
    description: Optional[str] = None


@dataclass
class UpdateCategoryResponse:
    category: Category


class UpdateCategory:
    def __init__(self, category_repository: CategoryRepositoryInterface = None):
        self.category_repository = category_repository

    def execute(self, request: UpdateCategoryRequest) -> UpdateCategoryResponse:
        category = self.category_repository.get_by_id(request.category_id)
        if category is None:
            raise CategoryDoesNotExist(f"Category with id {request.category_id} does not exist")

        # Only update fields that are provided
        if request.name is None:
            request.name = category.name

        if request.description is None:
            request.description = category.description

        category.change_category(request.name, request.description)
        self.category_repository.update(category)

        return UpdateCategoryResponse(category)


class CategoryDoesNotExist(Exception):
    pass