from typing import Set, Optional, Sequence, Dict, Any
from uuid import UUID

from core._shared.listing.orderer import Order
from core.cast_member.domain import CastMember
from core.cast_member.domain.repository.cast_member_repository_interface import CastMemberRepositoryInterface
from django.conf import settings


class CastMemberFakeRepository(CastMemberRepositoryInterface):
    def __init__(self, cast_members: Set[CastMember] = None):
        self._cast_members = cast_members or set()

    def create(self, cast_member: CastMember) -> None:
        self._cast_members.add(cast_member)

    def get_all(
        self,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[Dict[str, Order]] = None,
        limit: int = settings.DEFAULT_PAGE_SIZE,
        offset: int = 0,
    ) -> Sequence[CastMember]:
        filtered_cast_members = filter(
            lambda cast_member: all(getattr(cast_member, field) == value for field, value in filters.items()),
            self._cast_members,
        )
        ordered_cast_members = sorted(
            filtered_cast_members,
            key=lambda cast_member: [getattr(cast_member, field) for field, order in order_by.items()],
            reverse=False,
        )
        return ordered_cast_members[offset:(offset + limit)]

    def get_by_id(self, cast_member_id: UUID) -> Optional[CastMember]:
        return next(
            (cast_member for cast_member in self._cast_members if cast_member.id == cast_member_id),
            None,
        )

    def update(self, cast_member: CastMember) -> None:
        cast_member = self.get_by_id(cast_member.id)
        self._cast_members.add(cast_member)

    def delete(self, cast_member_id: UUID) -> None:
        cast_member = self.get_by_id(cast_member_id)
        self._cast_members.remove(cast_member)
