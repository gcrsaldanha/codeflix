from typing import Optional, Sequence, Dict, Any
from uuid import UUID

from django.db.models import QuerySet

from core._shared.listing.orderer import Order
from core.category.domain import Category
from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface
from core.category.infrastructure.django_app.models import Category as CategoryModel
from django.conf import settings


class CategoryDjangoRepository(CategoryRepositoryInterface):
    def __init__(self, queryset: Optional[QuerySet[CategoryModel]] = None):
        self._queryset = queryset or CategoryModel.objects.all()

    def get_by_id(self, category_id: UUID) -> Optional[Category]:
        try:
            category_model = self._queryset.get(id=category_id)
        except CategoryModel.DoesNotExist:
            return None
        else:
            return Category(
                id=category_model.id,
                name=category_model.name,
                description=category_model.description,
                is_active=category_model.is_active,
            )

    def get_all(
        self,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[Dict[str, Order]] = None,
        limit: int = settings.DEFAULT_PAGE_SIZE,
        offset: int = 0,
    ) -> Sequence[Category]:
        filters = filters or {}
        order_by = order_by or {"name": Order.ASC}
        # Convert the order_by dict to a format suitable for Django's ORM.
        order_by_converted = [f"{'-' if order == Order.DESC else ''}{field}" for field, order in order_by.items()]

        queryset = self._queryset.filter(**filters).order_by(*order_by_converted)[offset:offset + limit]

        return [
            Category(
                id=category_model.id,
                name=category_model.name,
                description=category_model.description,
                is_active=category_model.is_active,
            )
            for category_model in queryset
        ]

    def create(self, category: Category) -> None:
        category_model = CategoryModel(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )
        category_model.save()

    def update(self, category: Category) -> None:
        category_model = self._queryset.get(id=category.id)
        category_model.name = category.name
        category_model.description = category.description
        category_model.is_active = category.is_active
        category_model.save()

    def delete(self, category_id: UUID) -> None:
        category_model = self._queryset.get(id=category_id)
        category_model.delete()

    def count(self, filters: Optional[Dict] = None) -> int:
        filters = filters or {}
        return self._queryset.filter(**filters).count()
