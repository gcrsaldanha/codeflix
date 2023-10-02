from typing import Iterable
from uuid import UUID

from domain.category.entity.category import Category
from domain.category.repository.category_repository_interface import CategoryRepositoryInterface


class CategoryRepository(CategoryRepositoryInterface):
    def get_by_id(self, category_id: UUID) -> Category:
        pass

    def get_all(self) -> Iterable[Category]:
        pass

    def create(self, category: Category) -> None:
        pass
