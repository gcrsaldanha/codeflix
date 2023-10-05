from abc import ABC, abstractmethod
from typing import Iterable, Optional
from uuid import UUID

from core.category.domain.entity.category import Category


class CategoryRepositoryInterface(ABC):
    @abstractmethod
    def create(self, category: Category) -> None:
        pass

    @abstractmethod
    def get_by_id(self, category_id: UUID) -> Optional[Category]:
        pass

    @abstractmethod
    def get_all(self) -> Iterable[Category]:
        pass

    @abstractmethod
    def update(self, category: Category) -> None:
        pass
