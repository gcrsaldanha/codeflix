from typing import Set, Iterable, Optional

from domain.category.entity.category import Category
from domain.category.repository.category_repository_interface import CategoryRepositoryInterface


class FakeCategoryRepository(CategoryRepositoryInterface):
    def __init__(self, categories: Set[Category] = None):
        self._categories = categories or set()

    def create(self, category: Category) -> None:
        self._categories.add(category)

    def get_all(self) -> Iterable[Category]:
        return iter(self._categories)

    def get_by_id(self, category_id: int) -> Optional[Category]:
        return next(
            (category for category in self._categories if category.id == category_id),
            None,
        )
