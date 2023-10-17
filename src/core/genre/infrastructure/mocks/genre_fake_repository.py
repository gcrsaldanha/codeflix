from typing import Set, Optional, Sequence, Dict, Any
from uuid import UUID

from core._shared.listing.orderer import Order
from core.genre.domain import Genre
from core.genre.domain.repository.genre_repository_interface import GenreRepositoryInterface
from django.conf import settings


class GenreFakeRepository(GenreRepositoryInterface):
    def __init__(self, genres: Set[Genre] = None):
        self._genres = genres or set()

    def create(self, genre: Genre) -> None:
        self._genres.add(genre)

    def get_all(
        self,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[Dict[str, Order]] = None,
        limit: int = settings.DEFAULT_PAGE_SIZE,
        offset: int = 0,
    ) -> Sequence[Genre]:
        filtered_genres = filter(
            lambda genre: all(getattr(genre, field) == value for field, value in filters.items()),
            self._genres,
        )
        ordered_genres = sorted(
            filtered_genres,
            key=lambda genre: [getattr(genre, field) for field, order in order_by.items()],
            reverse=False,
        )
        return ordered_genres[offset:(offset + limit)]

    def get_by_id(self, genre_id: UUID) -> Optional[Genre]:
        return next(
            (genre for genre in self._genres if genre.id == genre_id),
            None,
        )

    def update(self, genre: Genre) -> None:
        genre = self.get_by_id(genre.id)
        self._genres.add(genre)

    def delete(self, genre_id: UUID) -> None:
        genre = self.get_by_id(genre_id)
        self._genres.remove(genre)
