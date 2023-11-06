from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from core.category.domain import Category
from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface

# from core.category.infrastructure.django_app.repositories import CategoryDjangoRepository


@dataclass
class GetCategoryRequest:
    category_id: UUID


@dataclass
class GetCategoryResponse:
    category: Optional[Category]


class GetCategory:
    def __init__(self, category_repository: CategoryRepositoryInterface):
        self._category_repository = category_repository

    def execute(self, request: GetCategoryRequest) -> GetCategoryResponse:
        category = self._category_repository.get_by_id(request.category_id)
        return GetCategoryResponse(category)
