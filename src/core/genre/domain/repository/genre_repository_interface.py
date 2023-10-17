from abc import ABC, abstractmethod
from typing import Optional, Sequence, Dict
from uuid import UUID

from django.conf import settings

from core._shared.listing.orderer import Order
from core.genre.domain.entity.genre import Genre


class GenreRepositoryInterface(ABC):
    @abstractmethod
    def create(self, genre: Genre) -> None:
        pass

    @abstractmethod
    def get_by_id(self, genre_id: UUID) -> Optional[Genre]:
        pass

    @abstractmethod
    def get_all(
        self,
        filters: Optional[Dict] = None,
        order_by: Optional[Dict[str, Order]] = None,
        limit: int = settings.DEFAULT_PAGE_SIZE,
        offset: int = 0,
    ) -> Sequence[Genre]:
        pass

    @abstractmethod
    def update(self, genre: Genre) -> None:
        pass

    @abstractmethod
    def delete(self, genre_id: UUID) -> None:
        pass
