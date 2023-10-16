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
        categories = self._category_repository.get_all(
            filters=request.filters,
            order_by=request.order_by or {"name": Order.ASC},
        )

        per_page = min(request.page_size, settings.MAX_PAGE_SIZE)
        paginator = self._paginator_class(object_list=categories, per_page=per_page)
        page = paginator.get_page(number=request.page)
        next_page = page.next_page_number() if page.has_next() else None
        total_quantity = paginator.count

        return ListCategoriesOutput(
            data=list(page.object_list),
            meta=ListOutputMeta(
                page=page.number,
                page_size=len(page.object_list),
                next_page=next_page,
                total_quantity=total_quantity,
            ),
        )
