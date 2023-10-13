from dataclasses import dataclass
from dataclasses import dataclass
from typing import List, Optional, Type

from django.conf import settings
from django.core.paginator import Paginator as DjangoPaginator

from core._shared.application.use_case import UseCase, ListInput, ListOutput
from core._shared.listing.orderer import Order
from core._shared.listing.paginator import Paginator
from core.category.domain.entity.category import Category
from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface
from core.category.infrastructure.django_app.repositories import CategoryDjangoRepository


@dataclass
class ListCategoriesInput(ListInput):
    pass
    # page: int = 1
    # page_size: int = settings.DEFAULT_PAGE_SIZE
    # filters: Dict[str, Any] = field(default_factory=dict)
    # order_by: Dict[str, Order] = field(default_factory=dict)
    #
    # @property
    # def offset(self) -> int:
    #     return (self.page - 1) * self.page_size


@dataclass
class ListCategoriesOutput(ListOutput[Category]):
    pass
    # data: List[Category]
    # page: int = 1
    # page_size: int = settings.DEFAULT_PAGE_SIZE
    # next_page: Optional[int] = None
    # total_quantity: int = 0


class ListCategories(UseCase[ListCategoriesInput, ListCategoriesOutput]):
    def __init__(
        self,
        category_repository: Optional[CategoryRepositoryInterface] = None,
        paginator_class: Type[Paginator] = DjangoPaginator,
    ):
        self._category_repository = category_repository or CategoryDjangoRepository()
        self._paginator_class = paginator_class

    def execute(self, request: ListCategoriesInput) -> ListCategoriesOutput:
        # If sorting was done in application layer
        # categories = sorted(self._category_repository.get_all(request.filters), key=lambda c: c.name)

        categories = self._category_repository.get_all(
            filters=request.filters,
            order_by=request.order_by or {"name": Order.ASC},
            # limit=request.page_size,
            # offset=request.offset,
        )

        # TODO: Keeping this here just for tests using a mock repository
        if not request.order_by:
            categories = sorted(categories, key=lambda c: c.name)

        # TODO: abstract this logic, it's repeated in all listing use cases. Will this use the Presenter pattern?
        # Maybe paginator could be aware of the ListOutput class and do this automatically?
        # Or the OutputList could define a method for it, being aware of the paginator?
        per_page = min(request.page_size, settings.MAX_PAGE_SIZE)
        paginator = self._paginator_class(object_list=categories, per_page=per_page)
        page = paginator.get_page(number=request.page)
        next_page = page.next_page_number() if page.has_next() else None
        total_quantity = paginator.count

        return ListCategoriesOutput(
            data=list(page.object_list),
            page=page.number,
            page_size=per_page,
            next_page=next_page,
            total_quantity=total_quantity,
        )

        # Below is an implementation not using Django Paginator

        # total_quantity = len(categories)
        # per_page = min(request.page_size, settings.MAX_PAGE_SIZE)
        # num_pages = math.ceil(total_quantity / per_page)
        # initial_index = (request.page - 1) * per_page
        # final_index = initial_index + per_page  # it's ok final_index > total_quantity because we use slicing
        #
        # paginated_categories = categories[initial_index:final_index]
        # next_page = request.page + 1 if request.page < num_pages else None
        #
        # return ListCategoriesResponse(
        #     data=paginated_categories,
        #     page=request.page,
        #     page_size=per_page,
        #     next_page=next_page,
        #     total_quantity=len(categories),
        # )
