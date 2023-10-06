from typing import Iterable, Optional
from uuid import UUID

from django.db.models import QuerySet

from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface
from core.category.domain import Category
from core.category.infrastructure.django_app.models import Category as CategoryModel


class CategoryDjangoRepository(CategoryRepositoryInterface):
    def __init__(self, queryset: Optional[QuerySet[CategoryModel]] = None):
        self._queryset = queryset or CategoryModel.objects.all()

    def get_by_id(self, category_id: UUID) -> Category:
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

    def get_all(self) -> Iterable[Category]:
        yield from (
            Category(
                id=category_model.id,
                name=category_model.name,
                description=category_model.description,
                is_active=category_model.is_active,
            )
            for category_model in self._queryset.all()
        )

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
