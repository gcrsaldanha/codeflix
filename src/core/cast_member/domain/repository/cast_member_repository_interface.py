from abc import ABC, abstractmethod
from typing import Optional, Sequence, Dict
from uuid import UUID

from django.conf import settings

from core._shared.listing.orderer import Order
from core.cast_member.domain.entity.cast_member import CastMember


class CastMemberRepositoryInterface(ABC):
    @abstractmethod
    def create(self, cast_member: CastMember) -> None:
        pass

    @abstractmethod
    def get_by_id(self, cast_member_id: UUID) -> Optional[CastMember]:
        pass

    @abstractmethod
    def get_all(
        self,
        filters: Optional[Dict] = None,
        order_by: Optional[Dict[str, Order]] = None,
        limit: int = settings.DEFAULT_PAGE_SIZE,
        offset: int = 0,
    ) -> Sequence[CastMember]:
        pass

    @abstractmethod
    def update(self, cast_member: CastMember) -> None:
        pass

    @abstractmethod
    def delete(self, cast_member_id: UUID) -> None:
        pass
