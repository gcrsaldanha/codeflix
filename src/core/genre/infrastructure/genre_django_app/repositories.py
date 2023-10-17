from typing import Optional, Sequence, Dict, Any
from uuid import UUID

from django.db.models import QuerySet

from core._shared.listing.orderer import Order
from core.genre.domain import Genre
from core.genre.domain.repository.genre_repository_interface import GenreRepositoryInterface
from core.genre.infrastructure.genre_django_app.models import Genre as GenreModel
from django.conf import settings


class GenreDjangoRepository(GenreRepositoryInterface):
    def __init__(self, queryset: Optional[QuerySet[GenreModel]] = None):
        self._queryset = queryset or GenreModel.objects.all()

    def get_by_id(self, genre_id: UUID) -> Optional[Genre]:
        try:
            genre_model = self._queryset.get(id=genre_id)
        except GenreModel.DoesNotExist:
            return None
        else:
            return Genre(
                id=genre_model.id,
                name=genre_model.name,
                is_active=genre_model.is_active,
                categories=genre_model.categories,
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

        return [
            Genre(
                id=genre_model.id,
                name=genre_model.name,
                is_active=genre_model.is_active,
                categories=genre_model.categories,
            )
            for genre_model in (self._queryset.filter(**filters).order_by(*order_by))
        ]

    def create(self, genre: Genre) -> None:
        genre_model = GenreModel(
            id=genre.id,
            name=genre.name,
            is_active=genre.is_active,
            categories=genre.categories,
        )
        genre_model.save()

    def update(self, genre: Genre) -> None:
        genre_model = self._queryset.get(id=genre.id)
        genre_model.name = genre.name
        genre_model.is_active = genre.is_active
        # genre_model.categories = genre.categories  # TODO: fix this
        genre_model.save()

    def delete(self, genre_id: UUID) -> None:
        genre_model = self._queryset.get(id=genre_id)
        genre_model.delete()
