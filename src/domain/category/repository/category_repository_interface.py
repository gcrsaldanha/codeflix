from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.category.entity.category import Category


class CategoryRepositoryInterface(ABC):
    @abstractmethod
    def create(self, category: Category) -> None:
        pass

    @abstractmethod
    def get_by_id(self, category_id: UUID) -> Category:
        pass
