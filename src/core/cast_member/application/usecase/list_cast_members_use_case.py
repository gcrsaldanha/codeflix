from dataclasses import dataclass
from typing import Optional, Type

from django.conf import settings
from django.core.paginator import Paginator as DjangoPaginator

from core._shared.application.use_case import UseCase, ListInput, ListOutput, ListOutputMeta
from core._shared.listing.orderer import Order
from core._shared.listing.paginator import Paginator
from core.cast_member.domain.entity.cast_member import CastMember
from core.cast_member.domain.repository.cast_member_repository_interface import CastMemberRepositoryInterface
from core.cast_member.infrastructure.cast_member_app.repositories import CastMemberDjangoRepository


@dataclass
class ListCastMembersInput(ListInput):
    pass


@dataclass
class ListCastMembersOutput(ListOutput[CastMember]):
    pass


class ListCastMembersUseCase(UseCase[ListCastMembersInput, ListCastMembersOutput]):
    def __init__(
        self,
        repository: Optional[CastMemberRepositoryInterface] = None,
        paginator_class: Type[Paginator] = DjangoPaginator,
    ):
        self._repository = repository or CastMemberDjangoRepository()
        self._paginator_class = paginator_class

    def execute(self, request: ListCastMembersInput) -> ListCastMembersOutput:
        cast_members = self._repository.get_all(
            filters=request.filters,
            order_by=request.order_by or {"name": Order.ASC},
        )

        per_page = min(request.page_size, settings.MAX_PAGE_SIZE)
        paginator = self._paginator_class(object_list=cast_members, per_page=per_page)
        page = paginator.get_page(number=request.page)
        next_page = page.next_page_number() if page.has_next() else None
        total_quantity = paginator.count

        return ListCastMembersOutput(
            data=list(page.object_list),
            meta=ListOutputMeta(
                page=page.number,
                page_size=len(page.object_list),
                next_page=next_page,
                total_quantity=total_quantity,
            ),
        )
