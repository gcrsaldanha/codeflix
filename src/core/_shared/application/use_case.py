from abc import abstractmethod, ABC
from dataclasses import field, dataclass
from typing import Dict, Any, List, Optional, Type, Sequence
from typing import TypeVar, Generic

from django.core.paginator import Paginator as DjangoPaginator
from django.conf import settings

from core._shared.listing.orderer import Order
from core._shared.listing.paginator import Paginator

T = TypeVar("T")


@dataclass
class Input(ABC):
    pass


@dataclass
class ListInput(Input, ABC):
    page: int = 1
    page_size: int = settings.DEFAULT_PAGE_SIZE
    filters: Dict[str, Any] = field(default_factory=dict)
    order_by: Dict[str, Order] = field(default_factory=dict)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


@dataclass
class Output(ABC):
    pass


@dataclass
class ListOutputMeta:
    page: int = 1
    page_size: int = settings.DEFAULT_PAGE_SIZE
    next_page: Optional[int] = None
    total_quantity: int = 0


@dataclass
class ListOutput(Output, Generic[T], ABC):
    data: List[T] = field(default_factory=list)
    meta: ListOutputMeta = field(default_factory=ListOutputMeta)


InputType = TypeVar("InputType", bound=Input)
OutputType = TypeVar("OutputType", bound=Output)


@dataclass
class UseCase(Generic[InputType, OutputType], ABC):
    @abstractmethod
    def execute(self, request: InputType) -> OutputType:
        pass
