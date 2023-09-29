from dataclasses import dataclass
from uuid import UUID

from domain.category.entity.category import Category
from domain.category.repository.category_repository_interface import CategoryRepositoryInterface


@dataclass
class CreateCategoryRequest:
    name: str
    description: str = ""


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
