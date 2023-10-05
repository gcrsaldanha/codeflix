from dataclasses import dataclass
from uuid import UUID

from core.category.application.usecase.category.update_category import CategoryDoesNotExist
from core.category.domain import Category
from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface


@dataclass
class DeleteCategoryRequest:
    category_id: UUID


@dataclass
class DeleteCategoryResponse:
    category: Category


class DeleteCategory:
    def __init__(self, category_repository: CategoryRepositoryInterface):
        self.category_repository = category_repository

    def execute(self, request: DeleteCategoryRequest) -> DeleteCategoryResponse:
        category = self.category_repository.get_by_id(request.category_id)
        if category is None:
            raise CategoryDoesNotExist(f"Category with id {request.category_id} does not exist")

        self.category_repository.delete(category.id)

        return DeleteCategoryResponse(category)
