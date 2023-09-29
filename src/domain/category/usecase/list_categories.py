from dataclasses import dataclass
from typing import Iterable, List
from uuid import UUID

from src.domain.category.entity.category import Category
from src.domain.category.repository.category_repository_interface import CategoryRepositoryInterface


@dataclass
class ListCategoriesRequest:
    """
    An empty request, but could have filters, pagination, etc.
    """
    pass


@dataclass
class ListCategoriesResponse:
    categories: List[Category]


class ListCategories:
    def __init__(self, category_repository: CategoryRepositoryInterface):
        self.category_repository = category_repository

    def execute(self, request: ListCategoriesRequest) -> ListCategoriesResponse:
        categories = list(self.category_repository.get_all())

        return ListCategoriesResponse(categories=categories)
