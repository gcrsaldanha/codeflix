from dataclasses import dataclass
from typing import List, Optional

from core.category.domain.entity.category import Category
from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface
from core.category.infrastructure.django_app.repositories import CategoryDjangoRepository


@dataclass
class ListCategoriesRequest:
    """
    An empty request, but could have filters, pagination, etc.
    """
    pass


@dataclass
class ListCategoriesResponse:  # TODO: Add Presenter pattern
    categories: List[Category]


class ListCategories:
    def __init__(self, category_repository: Optional[CategoryRepositoryInterface] = None):
        self.category_repository = category_repository or CategoryDjangoRepository()  # TODO: dependency on Django ORM

    def execute(self, request: ListCategoriesRequest) -> ListCategoriesResponse:
        # TODO: Paginator / Ordering / Filtering
        categories = sorted(self.category_repository.get_all(), key=lambda c: c.name)

        return ListCategoriesResponse(categories=categories)
