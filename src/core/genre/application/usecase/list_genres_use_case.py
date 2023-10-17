from dataclasses import dataclass
from typing import Optional, Type

from django.conf import settings
from django.core.paginator import Paginator as DjangoPaginator

from core._shared.application.use_case import UseCase, ListInput, ListOutput, ListOutputMeta
from core._shared.listing.orderer import Order
from core._shared.listing.paginator import Paginator
from core.genre.domain.entity.genre import Genre
from core.genre.domain.repository.genre_repository_interface import GenreRepositoryInterface
from core.genre.infrastructure.genre_django_app.repositories import GenreDjangoRepository


@dataclass
class ListGenresInput(ListInput):
    pass


@dataclass
class ListGenresOutput(ListOutput[Genre]):
    pass


class ListGenresUseCase(UseCase[ListGenresInput, ListGenresOutput]):
    def __init__(
        self,
        repository: Optional[GenreRepositoryInterface] = None,
        paginator_class: Type[Paginator] = DjangoPaginator,
    ):
        self._repository = repository or GenreDjangoRepository()
        self._paginator_class = paginator_class

    def execute(self, request: ListGenresInput) -> ListGenresOutput:
        genres = self._repository.get_all(
            filters=request.filters,
            order_by=request.order_by or {"name": Order.ASC},
        )

        per_page = min(request.page_size, settings.MAX_PAGE_SIZE)
        paginator = self._paginator_class(object_list=genres, per_page=per_page)
        page = paginator.get_page(number=request.page)
        next_page = page.next_page_number() if page.has_next() else None
        total_quantity = paginator.count

        return ListGenresOutput(
            data=list(page.object_list),
            meta=ListOutputMeta(
                page=page.number,
                page_size=len(page.object_list),
                next_page=next_page,
                total_quantity=total_quantity,
            ),
        )
