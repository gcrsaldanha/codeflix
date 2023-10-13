from __future__ import annotations

from abc import abstractmethod, ABC
from collections.abc import Sequence
from typing import TypeVar, Generic

from django.conf import settings

T = TypeVar("T")


class Paginator(Generic[T], ABC):
    def __init__(self, object_list: Sequence[T], per_page=settings.DEFAULT_PAGE_SIZE) -> None:
        """
        :param object_list: The list of objects to paginate.
        :param per_page: The maximum number of objects per page.
        """
        self.object_list = object_list
        self.per_page = per_page

    @abstractmethod
    def get_page(self, number: int) -> Page[T]:
        """
        :param number: 1-indexed page number.
        :return: The requested page.
        """
        pass

    @property
    @abstractmethod
    def count(self) -> int:
        """
        :return: The total number of objects, across all pages.
        """
        pass


class Page(Generic[T], Sequence[T], ABC):
    def __init__(self, object_list: Sequence[T], number: int, paginator: Paginator[T]) -> None:
        self.object_list = object_list
        self.number = number
        self.paginator = paginator

    @abstractmethod
    def __len__(self) -> int:
        """
        :return: The number of objects in this page.
        """
        pass

    @abstractmethod
    def __getitem__(self, index: int) -> T:
        """
        :param index: 0-indexed object index.
        :return: The requested object.
        """
        pass

    @abstractmethod
    def has_next(self) -> bool:
        """
        :return: Whether there is a next page.
        """
        pass

    @abstractmethod
    def next_page_number(self) -> int:
        """
        :return: The 1-indexed number of the next page.
        """
        pass
