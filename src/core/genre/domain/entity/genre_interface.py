from abc import ABC, abstractmethod
from uuid import UUID


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

    @abstractmethod
    def add_category(self, category: UUID) -> None:
        pass

    @abstractmethod
    def remove_category(self, category: UUID) -> None:
        pass
