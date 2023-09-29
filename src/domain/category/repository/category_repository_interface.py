from abc import ABC, abstractmethod
from typing import Iterable
from uuid import UUID

from domain.category.entity.category import Category


class CategoryRepositoryInterface(ABC):
    @abstractmethod
    def create(self, category: Category) -> None:
        pass

    @abstractmethod
    def get_by_id(self, category_id: UUID) -> Category:
        pass

    @abstractmethod
    def get_all(self) -> Iterable[Category]:
        pass
