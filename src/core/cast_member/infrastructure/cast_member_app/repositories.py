from typing import Optional, Sequence, Dict, Any
from uuid import UUID

from django.db.models import QuerySet

from core._shared.listing.orderer import Order
from core.cast_member.domain import CastMember
from core.cast_member.domain.repository.cast_member_repository_interface import CastMemberRepositoryInterface
from core.cast_member.infrastructure.cast_member_app.models import CastMember as CastMemberModel
from django.conf import settings


class CastMemberDjangoRepository(CastMemberRepositoryInterface):
    def __init__(self, queryset: Optional[QuerySet[CastMemberModel]] = None):
        self._queryset = queryset or CastMemberModel.objects.all()

    def get_by_id(self, cast_member_id: UUID) -> Optional[CastMember]:
        try:
            cast_member_model = self._queryset.get(id=cast_member_id)
        except CastMemberModel.DoesNotExist:
            return None
        else:
            return CastMember(
                id=cast_member_model.id,
                name=cast_member_model.name,
                cast_member_type=cast_member_model.cast_member_type,
            )

    def get_all(
        self,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[Dict[str, Order]] = None,
        limit: int = settings.DEFAULT_PAGE_SIZE,
        offset: int = 0,
    ) -> Sequence[CastMember]:
        filters = filters or {}
        order_by = order_by or {}
        order_by = (f"{'-' if order == Order.DESC else ''}{field}" for field, order in order_by.items())

        return [
            CastMember(
                id=cast_member_model.id,
                name=cast_member_model.name,
                cast_member_type=cast_member_model.cast_member_type,
            )
            for cast_member_model in (self._queryset.filter(**filters).order_by(*order_by))
        ]

    def create(self, cast_member: CastMember) -> None:
        cast_member_model = CastMemberModel(
            id=cast_member.id,
            name=cast_member.name,
            cast_member_type=cast_member.cast_member_type.name,
        )
        cast_member_model.save()

    def update(self, cast_member: CastMember) -> None:
        cast_member_model = self._queryset.get(id=cast_member.id)
        cast_member_model.name = cast_member.name
        cast_member_model.cast_member_type = cast_member.cast_member_type
        cast_member_model.save()

    def delete(self, cast_member_id: UUID) -> None:
        cast_member_model = self._queryset.get(id=cast_member_id)
        cast_member_model.delete()
