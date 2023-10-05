from typing import Set, Iterable, Optional
from uuid import UUID

from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface
from core.category.domain import Category


class CategoryFakeRepository(CategoryRepositoryInterface):
    def __init__(self, categories: Set[Category] = None):
        self._categories = categories or set()

    def create(self, category: Category) -> None:
        self._categories.add(category)

    def get_all(self) -> Iterable[Category]:
        return iter(self._categories)

    def get_by_id(self, category_id: UUID) -> Optional[Category]:
        return next(
            (category for category in self._categories if category.id == category_id),
            None,
        )

    def update(self, category: Category) -> None:
        category = self.get_by_id(category.id)
        self._categories.add(category)
