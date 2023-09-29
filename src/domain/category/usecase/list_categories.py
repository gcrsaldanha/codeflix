from dataclasses import dataclass
from typing import Iterable, List
from uuid import UUID

from domain.category.entity.category import Category
from domain.category.repository.category_repository_interface import CategoryRepositoryInterface


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
        categories = sorted(self.category_repository.get_all(), key=lambda c: c.name)

        return ListCategoriesResponse(categories=categories)
