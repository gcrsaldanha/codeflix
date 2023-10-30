from typing import Set, Optional, Sequence, Dict, Any
from uuid import UUID

from core._shared.listing.orderer import Order
from core.category.domain import Category
from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface
from django.conf import settings


class CategoryFakeRepository(CategoryRepositoryInterface):
    def __init__(self, categories: Set[Category] = None):
        self._categories = categories or set()

    def create(self, category: Category) -> None:
        self._categories.add(category)

    def get_all(
        self,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[Dict[str, Order]] = None,
        limit: int = settings.DEFAULT_PAGE_SIZE,
        offset: int = 0,
    ) -> Sequence[Category]:
        filtered_entities = filter(
            lambda entity: all(getattr(entity, field) == value for field, value in filters.items()),
            self._categories,
        )
        ordered_entities = sorted(
            filtered_entities,
            key=lambda entity: [getattr(entity, field) for field, order in order_by.items()],
        )
        return ordered_entities[offset:(offset + limit)]

    def get_by_id(self, category_id: UUID) -> Optional[Category]:
        return next(
            (category for category in self._categories if category.id == category_id),
            None,
        )

    def update(self, category: Category) -> None:
        category = self.get_by_id(category.id)
        self._categories.add(category)

    def delete(self, category_id: UUID) -> None:
        category = self.get_by_id(category_id)
        self._categories.remove(category)

    def count(self, filters: Optional[Dict] = None) -> int:
        return len(self._categories)
