from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from core.category.domain.entity.category import Category


class GenreInterface(ABC):
    @abstractmethod
    def activate(self) -> None:
        pass

    @abstractmethod
    def deactivate(self) -> None:
        pass

    @abstractmethod
    def change_genre(self, name: str, description: str) -> None:
        pass

    @property
    @abstractmethod
    def is_active(self) -> bool:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def categories(self) -> List[Category]:
        pass

    @property
    @abstractmethod
    def id(self) -> UUID:
        pass

    @abstractmethod
    def add_category(self, category: Category) -> None:
        pass

    @abstractmethod
    def remove_category(self, category: Category) -> None:
        pass
