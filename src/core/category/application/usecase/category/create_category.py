from dataclasses import dataclass
from uuid import UUID

from core.category.domain.entity.category import Category
from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface


@dataclass
class CreateCategoryRequest:
    name: str
    description: str = ""

    def validate(self):
        pass


@dataclass
class CreateCategoryResponse:
    id: UUID


class CreateCategory:
    def __init__(self, category_repository: CategoryRepositoryInterface):
        self.category_repository = category_repository

    def execute(self, request: CreateCategoryRequest) -> CreateCategoryResponse:
        category = Category(name=request.name, description=request.description)

        self.category_repository.create(category)

        return CreateCategoryResponse(id=category.id)
