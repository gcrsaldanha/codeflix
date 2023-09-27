from abc import ABC, abstractmethod
from uuid import UUID


class CategoryInterface(ABC):
    @abstractmethod
    def activate(self) -> None:
        pass

    @abstractmethod
    def deactivate(self) -> None:
        pass

    @abstractmethod
    def change_category(self, name: str, description: str) -> None:
        pass

    @abstractmethod
    def validate(self) -> None:
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
    def id(self) -> UUID:
        pass
