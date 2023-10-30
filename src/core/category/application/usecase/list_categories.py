from dataclasses import dataclass
from typing import Optional, Type

from django.conf import settings
from django.core.paginator import Paginator as DjangoPaginator

from core._shared.application.use_case import UseCase, ListInput, ListOutput, ListOutputMeta
from core._shared.listing.orderer import Order
from core._shared.listing.paginator import Paginator
from core.category.domain.entity.category import Category
from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface
from core.category.infrastructure.django_app.repositories import CategoryDjangoRepository


@dataclass
class ListCategoriesInput(ListInput):
    pass


@dataclass
class ListCategoriesOutput(ListOutput[Category]):
    pass


class ListCategories(UseCase[ListCategoriesInput, ListCategoriesOutput]):
    def __init__(
        self,
        category_repository: Optional[CategoryRepositoryInterface] = None,
        paginator_class: Type[Paginator] = DjangoPaginator,
    ):
        self._category_repository = category_repository or CategoryDjangoRepository()
        self._paginator_class = paginator_class

    def execute(self, request: ListCategoriesInput) -> ListCategoriesOutput:
        per_page = min(request.page_size, settings.MAX_PAGE_SIZE)
        offset = (request.page - 1) * per_page

        categories = self._category_repository.get_all(
            filters=request.filters,
            order_by=request.order_by or {"name": Order.ASC},
            limit=per_page,
            offset=offset
        )
        total_quantity = self._category_repository.count(filters=request.filters)

        next_page = request.page + 1 if total_quantity > offset + per_page else None

        return ListCategoriesOutput(
            data=list(categories),
            meta=ListOutputMeta(
                page=request.page,
                page_size=len(categories),
                next_page=next_page,
                total_quantity=total_quantity,
            ),
        )
