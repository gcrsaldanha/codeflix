from dataclasses import dataclass, field
from typing import List, Optional, Type, Dict, Any

from django.conf import settings
from django.core.paginator import Paginator as DjangoPaginator

from core._shared.pagination.paginator import Paginator, Order
from core.category.domain.entity.category import Category
from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface
from core.category.infrastructure.django_app.repositories import CategoryDjangoRepository


@dataclass
class ListCategoriesRequest:
    page: int = 1
    page_size: int = settings.DEFAULT_PAGE_SIZE
    filters: Dict[str, Any] = field(default_factory=dict)
    order_by: Dict[str, Order] = field(default_factory=dict)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


@dataclass
class ListCategoriesResponse:  # TODO: Add Presenter pattern
    data: List[Category]
    page: int = 1
    next_page: Optional[int] = None
    total_quantity: int = 0


class ListCategories:
    def __init__(
        self,
        category_repository: Optional[CategoryRepositoryInterface] = None,
        paginator_class: Type[Paginator] = DjangoPaginator,
    ):
        self._category_repository = category_repository or CategoryDjangoRepository()
        self._paginator_class = paginator_class

    def execute(self, request: ListCategoriesRequest) -> ListCategoriesResponse:

        # If sorting was done in application layer
        # categories = sorted(self._category_repository.get_all(request.filters), key=lambda c: c.name)

        # TODO: think about limit/offset with the database
        categories = self._category_repository.get_all(
            filters=request.filters,
            order_by=request.order_by or {"name": Order.ASC},
            # limit=request.page_size,
            # offset=request.offset,
        )

        # TODO: Keeping this here just for tests using a mock repository
        if not request.order_by:
            categories = sorted(categories, key=lambda c: c.name)

        # TODO: abstract this logic, it's repeated in all listing use cases.
        # TODO: if I do limit/offset in repository, do I need it here as well?
        paginator = self._paginator_class(object_list=categories, per_page=request.page_size)
        paginated_categories = paginator.get_page(number=request.page)
        next_page = paginated_categories.next_page_number() if paginated_categories.has_next() else None
        total_quantity = paginator.count

        return ListCategoriesResponse(
            data=list(paginated_categories.object_list),
            page=request.page,
            next_page=next_page,
            total_quantity=total_quantity,
        )

        # Below is an implementation not using Django Paginator
        # total_quantity = len(categories)
        # num_pages = math.ceil(total_quantity / request.page_size)
        #
        # initial_index = (request.page - 1) * request.page_size
        # final_index = initial_index + request.page_size  # it's ok final_index > total_quantity because we use slicing
        #
        # paginated_categories = categories[initial_index:final_index]
        # next_page = request.page + 1 if request.page < num_pages else None

        # return ListCategoriesResponse(
        #     data=paginated_categories,
        #     page=request.page,
        #     next_page=next_page,
        #     total_quantity=len(categories),
        # )
