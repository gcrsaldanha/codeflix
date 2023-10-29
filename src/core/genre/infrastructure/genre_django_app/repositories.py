from typing import Optional, Sequence, Dict, Any, List
from uuid import UUID

from django.db import transaction
from django.db.models import QuerySet

from core._shared.listing.orderer import Order
from core.genre.domain import Genre
from core.genre.domain.repository.genre_repository_interface import GenreRepositoryInterface
from core.genre.infrastructure.genre_django_app.models import (
    Genre as GenreModel,
    GenreCategory as GenreCategoryModel,
)
from django.conf import settings


class GenreDjangoRepository(GenreRepositoryInterface):
    def __init__(self, queryset: Optional[QuerySet[GenreModel]] = None):
        self._queryset = queryset or GenreModel.objects.all()

    def get_by_id(self, genre_id: UUID) -> Optional[Genre]:
        try:
            genre = GenreModel.objects.prefetch_related("related_categories").get(id=genre_id)
        except GenreModel.DoesNotExist:
            return None

        category_ids = {gc.category_id for gc in genre.related_categories.all()}

        return Genre(
            id=genre.id,
            name=genre.name,
            description=genre.description,
            is_active=genre.is_active,
            categories=category_ids,
        )

    def get_all(
        self,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[Dict[str, Order]] = None,
        limit: int = settings.DEFAULT_PAGE_SIZE,
        offset: int = 0,
    ) -> Sequence[Genre]:
        filters = filters or {}
        order_by = order_by or {}
        order_by = (f"{'-' if order == Order.DESC else ''}{field}" for field, order in order_by.items())

        genres = (
            self._queryset.filter(**filters)
            .order_by(*order_by)
            .prefetch_related("related_categories")  # [offset : offset + limit] - not adding limit yet to repo
        )

        return [
            Genre(
                id=genre_model.id,
                name=genre_model.name,
                description=genre_model.description,
                is_active=genre_model.is_active,
                categories={gc.category_id for gc in genre_model.related_categories.all()},
            )
            for genre_model in genres
        ]

    def create(self, genre: Genre) -> None:
        with transaction.atomic():
            genre_model = GenreModel(
                id=genre.id,
                name=genre.name,
                description=genre.description,
                is_active=genre.is_active,
            )
            genre_model.save()

            genre_categories: List[GenreCategoryModel] = [
                GenreCategoryModel(genre=genre_model, category_id=category_id) for category_id in genre.categories
            ]
            GenreCategoryModel.objects.bulk_create(genre_categories)

    def update(self, genre: Genre) -> None:
        genre_model = self._queryset.get(id=genre.id)
        genre_model.name = genre.name
        genre_model.description = genre.description
        genre_model.is_active = genre.is_active
        genre_model.save()

    def delete(self, genre_id: UUID) -> None:
        genre_model = self._queryset.get(id=genre_id)
        genre_model.delete()
