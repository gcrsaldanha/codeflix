from abc import ABC, abstractmethod
from typing import Iterable, Optional, Sequence, Dict
from uuid import UUID

from core._shared.pagination.paginator import Order
from core.category.domain.entity.category import Category
from django_project import settings


class CategoryRepositoryInterface(ABC):
    @abstractmethod
    def create(self, category: Category) -> None:
        pass

    @abstractmethod
    def get_by_id(self, category_id: UUID) -> Optional[Category]:
        pass

    @abstractmethod
    def get_all(
        self,
        filters: Optional[Dict] = None,
        order_by: Optional[Dict[str, Order]] = None,
        limit: int = settings.DEFAULT_PAGE_SIZE,
        offset: int = 0,
    ) -> Sequence[Category]:
        pass

    @abstractmethod
    def update(self, category: Category) -> None:
        pass

    @abstractmethod
    def delete(self, category_id: UUID) -> None:
        pass
